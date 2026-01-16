import math
import numpy as np
import cv2
from typing import Tuple, List, Optional
from skimage.morphology import skeletonize
from scipy.interpolate import splprep, splev
import torch

FEATURE_TO_KEY = {
    "start_x": 0,
    "start_y": 1,
    "end_x": 2,
    "end_y": 3,
    "num_spurs": 4,
    "curvature": 5,
    "cos_angle": 6,
    "sin_angle": 7,
}
KEY_TO_FEATURE = {v: k for k, v in FEATURE_TO_KEY.items()}


def get_curvature(mask: np.ndarray) -> float:
    """
    Compute the average curvature of the skeletonized binary mask.

    Args:
        mask: (H, W) binary mask

    Returns:
        Average curvature value
    """
    skeleton = skeletonize(mask > 0).astype(np.uint8)
    ys, xs = np.nonzero(skeleton)

    if len(xs) < 10:
        return 0

    # Curvature proxy: angle changes
    coords = np.stack([xs, ys], axis=1)
    diffs = np.diff(coords, axis=0)
    norms = np.linalg.norm(diffs, axis=1, keepdims=True) + 1e-6
    directions = diffs / norms

    angles = np.arccos(
        np.clip(
            np.sum(directions[:-1] * directions[1:], axis=1),
            -1.0,
            1.0,
        )
    )

    return np.mean(angles)


def get_endpoints_and_spurs(mask: np.ndarray) -> Tuple[List[Tuple[int, int]], int]:
    """
    Get endpoints of a skeletonized binary mask.

    Args:
        mask: (H, W) binary mask

    Returns:
        List of (x, y) coordinates of endpoints
        Number of spurs (extra endpoints beyond two)
    """
    # Skeletonize the mask
    skeleton = skeletonize(mask > 0).astype(np.uint8)

    # Define a kernel to find endpoints
    kernel = np.array([[1, 1, 1], [1, 10, 1], [1, 1, 1]], dtype=np.uint8)

    # Convolve to find endpoints
    filtered = cv2.filter2D(skeleton, -1, kernel, borderType=0)

    # Endpoints will have a value of 11 in the filtered image
    endpoints = np.argwhere(filtered == 11)

    # Get the endpoints with the greatest distance between them
    if len(endpoints) >= 2:
        max_dist = 0
        pt1, pt2 = endpoints[0], endpoints[1]
        for i in range(len(endpoints) - 1):
            for j in range(i + 1, len(endpoints)):
                dist = np.linalg.norm(endpoints[i] - endpoints[j])
                if dist > max_dist:
                    max_dist = dist
                    pt1, pt2 = endpoints[i], endpoints[j]

                    # Ensure pt1 is the topmost point
                    if pt1[0] > pt2[0]:
                        pt1, pt2 = pt2, pt1
    else:
        pt1 = np.unravel_index(skeleton.argmax(), skeleton.shape)

        if pt1[0] == skeleton.shape[0] - 1:
            pt2 = pt1
            pt1 = (pt2[0] - 1, pt2[1])
        else:
            pt2 = (pt1[0] + 1, pt1[1])

    # Normalize to [-1, 1]
    pt1 = (pt1 / np.array(mask.shape)) * 2 - 1
    pt2 = (pt2 / np.array(mask.shape)) * 2 - 1

    return [(pt1[1], pt1[0]), (pt2[1], pt2[0])], max(
        len(endpoints) - 2, 0
    )  # Return as (x, y) tuples, number of spurs


def is_rgb_annotation(mask: np.ndarray) -> bool:
    """
    Detect if annotation is RGB (H, W, 3) or indexed (H, W).

    Args:
        mask: Annotation array

    Returns:
        True if RGB, False if indexed
    """
    return len(mask.shape) == 3 and mask.shape[2] == 3


def rgb_to_indexed(
    rgb_mask: np.ndarray, colour_map: dict[tuple[int, int, int], int]
) -> np.ndarray:
    """
    Convert an RGB segmentation mask to an index mask.

    Args:
        rgb_mask: (H, W, 3) uint8 array
        colour_map: dict mapping (R, G, B) -> class index

    Returns:
        index_mask: (H, W) int64 array
    """
    if rgb_mask.ndim != 3 or rgb_mask.shape[-1] != 3:
        raise ValueError("mask_rgb must have shape (H, W, 3)")

    h, w, _ = rgb_mask.shape
    index_mask = np.zeros((h, w), dtype=np.int64)

    # Vectorized comparison per class
    for rgb, idx in colour_map.items():
        rgb = np.array(rgb, dtype=rgb_mask.dtype)
        matches = np.all(rgb_mask == rgb, axis=-1)
        index_mask[matches] = idx

    return index_mask


def indexed_to_rgb(
    indexed_mask: np.ndarray, colour_map: dict[tuple[int, int, int], int]
) -> np.ndarray:
    """
    Convert indexed annotation back to RGB using color palette.

    Args:
        indexed_mask: (H, W) array with class indices
        colour_map: dict mapping (R, G, B) -> class index

    Returns:
        (H, W, 3) RGB annotation
    """
    palette = np.zeros((max(colour_map.values()) + 1, 3), dtype=np.uint8)
    for rgb, idx in colour_map.items():
        palette[idx] = np.array(rgb, dtype=np.uint8)

    rgb_mask = palette[indexed_mask]
    return rgb_mask.astype(np.uint8)


def extract_class_masks(indexed_mask: np.ndarray) -> dict[int, np.ndarray]:
    """
    Extract individual binary masks for each class.

    Args:
        indexed_mask: (H, W) indexed annotation

    Returns:
        List of (class_id, binary_mask) tuples
    """
    unique_classes = np.unique(indexed_mask)
    class_masks = {}

    for class_id in unique_classes:
        if class_id == 0:  # Skip background
            continue
        binary_mask = (indexed_mask == class_id).astype(np.uint8)
        class_masks[class_id] = binary_mask

    return class_masks


def count_objects(mask: np.ndarray) -> int:
    """
    Count the number of connected components (objects) in a binary mask.

    Args:
        mask: (H, W) binary mask

    Returns:
        Number of separate objects (connected components)
    """
    if mask.max() == 0:
        return 0

    # Use OpenCV to find connected components
    num_labels, _ = cv2.connectedComponents(mask.astype(np.uint8))
    # Subtract 1 to exclude background
    return max(0, num_labels - 1)


def get_objects(mask: np.ndarray) -> List[np.ndarray]:
    """
    Extract individual object masks from a binary mask.

    Args:
        mask: (H, W) binary mask

    Returns:
        List of (H, W) binary masks for each object
    """
    if mask.max() == 0:
        return []

    # Use OpenCV to find connected components
    num_labels, labels = cv2.connectedComponents(mask.astype(np.uint8))

    object_masks = []
    for label in range(1, num_labels):  # Skip background label 0
        object_mask = (labels == label).astype(np.uint8)
        object_masks.append(object_mask)

    return object_masks


def extract_object_features(mask: np.ndarray) -> np.ndarray:
    """
    Extract features of a single object in a binary mask.

    Args:
        mask: (H, W) binary mask of a single object

    Returns:
        Feature vector as a numpy array
    """

    endpoints, num_spurs = get_endpoints_and_spurs(mask)
    (x1, y1), (x2, y2) = endpoints if len(endpoints) >= 2 else ((0, 0), (0, 0))
    vector = np.array([x2 - x1, y2 - y1], dtype=np.float32)
    angle = np.arctan2(vector[1], vector[0]) if np.linalg.norm(vector) > 0 else 0.0
    curvature = get_curvature(mask)

    # Normalize curvature to [-1, 1]
    normalized_curvature = min(curvature, 0.5) * 4 - 1

    features = {
        "start_x": x1,
        "start_y": y1,
        "end_x": x2,
        "end_y": y2,
        "num_spurs": num_spurs,
        "curvature": normalized_curvature,
        "cos_angle": math.cos(angle),
        "sin_angle": math.sin(angle),
    }

    return pack_feature_vector(features)


def create_spline(
    image_shape: Tuple[int, int],
    start: Tuple[int, int],
    end: Tuple[int, int],
    num_ctrl: int = 5,
    curvature_scale: float = 0.2,
) -> np.ndarray:
    """
    Generate a smooth random spline curve.

    Args:
        image_shape: Tuple (H, W) for the target image size
        start: Tuple (x, y) for the starting point
        end: Tuple (x, y) for the ending point
        num_ctrl: Number of control points for the spline
        curvature_scale: Scale factor for curvature randomness

    Returns:
        Array of shape (N, 2) containing the spline points [x, y]
    """

    H, W = image_shape

    # Random control points between start and end
    ctrl_x = (
        np.linspace(start[0], end[0], num_ctrl)
        + np.random.randn(num_ctrl) * curvature_scale
    )
    ctrl_y = (
        np.linspace(start[1], end[1], num_ctrl)
        + np.random.randn(num_ctrl) * curvature_scale
    )
    num_samples = max(int(300 * curvature_scale), 10)

    try:
        tck, _ = splprep([ctrl_x, ctrl_y], s=0)
        u = np.linspace(0, 1, num_samples)
        x, y = splev(u, tck)
    except ValueError:
        # Fallback to linear if spline fails
        x = np.linspace(start[0], end[0], num_samples)
        y = np.linspace(start[1], end[1], num_samples)

    return np.stack([x, y], axis=1)


def add_branch(points, angle_std=0.5, length_scale=0.5):
    """
    Add a branch to an existing spline.

    Args:
        points: Main spline points array of shape (N, 2)
        angle_std: Standard deviation for branch angle variation
        length_scale: Scale factor for branch length

    Returns:
        Array of branch points
    """
    idx = np.random.randint(len(points) // 4, len(points) * 3 // 4)
    base = points[idx]

    direction = points[idx + 1] - points[idx]
    theta = np.arctan2(direction[1], direction[0])
    theta += np.random.randn() * angle_std

    length = np.linalg.norm(direction) * 50 * length_scale
    branch_end = base + length * np.array([np.cos(theta), np.sin(theta)])

    return np.linspace(base, branch_end, 50)


def draw_polyline(
    image_shape,
    points,
    thickness=10,
):
    """
    Rasterize a polyline (spline) to an image.

    Args:
        image_shape: Tuple (H, W) for the canvas size
        points: Array of shape (N, 2) containing points [x, y]
        thickness: Line thickness in pixels

    Returns:
        Binary image with the drawn polyline
    """
    canvas = np.zeros(image_shape, dtype=np.uint8)

    pts = points.astype(np.int32)
    for i in range(len(pts) - 1):
        cv2.line(
            canvas,
            tuple(pts[i]),
            tuple(pts[i + 1]),
            color=1,
            thickness=thickness,
        )
    return canvas


def generate_scribble(
    image_shape,
    features: dict,
    class_id: int = 1,
):
    """
    Generate a synthetic scribble annotation based on dataset statistics.

    Args:
        image_shape: Tuple (H, W) for the output size
        features: Dictionary with scribble features
        class_id: Class index to assign to the generated scribble (default: 1)

    Returns:
        Binary scribble mask of shape (H, W) with values 0 (background) and class_id
    """
    start = (features["start_x"], features["start_y"])
    end = (features["end_x"], features["end_y"])

    main = create_spline(
        image_shape,
        start=start,
        end=end,
        num_ctrl=10,
        curvature_scale=min(features["curvature"], 0.5) * 20,
    )

    canvas = draw_polyline(image_shape, main)

    # Branching
    for _ in range(int(features["num_spurs"])):
        branch = add_branch(main)
        canvas |= draw_polyline(image_shape, branch)

    # Apply class_id
    canvas = canvas * class_id

    return canvas


def generate_multiclass_scribble(
    image_shape,
    objects: list[dict],
    classes: np.ndarray | torch.Tensor,
    colour_map: Optional[dict[tuple[int, int, int], int]] = None,
) -> np.ndarray:
    """
    Generate multi-class synthetic scribble annotation.

    Args:
        image_shape: Tuple (H, W) for the output size
        stats_per_class: Dictionary mapping class_id to stats dict
        colour_map: Optional dict mapping (R, G, B) -> class index. If provided, returns RGB output.

    Returns:
        Either indexed (H, W) or RGB (H, W, 3) scribble annotation
    """
    if type(classes) is torch.Tensor:
        classes = classes.cpu().numpy()

    # Denormalize
    for obj in objects:
        obj["curvature"] = (obj["curvature"] / 4.0) + 0.25
        obj["start_x"] = int((obj["start_x"] + 1) * image_shape[1] / 2)
        obj["start_y"] = int((obj["start_y"] + 1) * image_shape[0] / 2)
        obj["end_x"] = int((obj["end_x"] + 1) * image_shape[1] / 2)
        obj["end_y"] = int((obj["end_y"] + 1) * image_shape[0] / 2)

    # Create empty canvas
    indexed_output = np.zeros(image_shape, dtype=np.uint8)

    # Generate scribble for each class
    for class_id, features in zip(classes, objects):
        if class_id == 0:  # Skip background
            continue

        class_scribble = generate_scribble(
            image_shape=image_shape,
            features=features,
            class_id=class_id,
        )

        # Add to canvas (later classes can overwrite earlier ones at overlaps)
        indexed_output = np.where(class_scribble > 0, class_scribble, indexed_output)

    # Convert to RGB if colour_map provided
    if colour_map is not None:
        return indexed_to_rgb(indexed_output, colour_map)

    return indexed_output


def pack_feature_vector(features: dict) -> torch.Tensor:
    """
    Pack a feature vector into a Tensor from a dict.

    Args:
        features: dictionary of feature names to values

    Returns:
        feature vector as a torch Tensor
    """
    vector = torch.zeros(len(FEATURE_TO_KEY), dtype=torch.float32)
    for key, value in features.items():
        if key in FEATURE_TO_KEY:
            vector[FEATURE_TO_KEY[key]] = value
    return vector


def unpack_feature_vector(vector: torch.Tensor) -> dict:
    """
    Unpack a feature vector Tensor into a dict.

    Args:
        vector: feature vector as a torch Tensor

    Returns:
        dictionary of feature names to values
    """
    features = {}
    for i in range(len(vector)):
        key = KEY_TO_FEATURE[i]
        features[key] = vector[i].item()
    return features
