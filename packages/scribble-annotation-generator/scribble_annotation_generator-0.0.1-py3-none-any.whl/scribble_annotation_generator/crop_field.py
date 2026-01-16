import cv2
import math
import numpy as np
import os
import random

from scribble_annotation_generator.utils import generate_multiclass_scribble


NUM_SAMPLES_TO_GENERATE = 200
ROW_STD = 0.02
ROW_CURVATURE_MEAN = -0.8
ROW_CURVATURE_STD = 0.05
ROW_MIN_LENGTH = 0.1
ROW_SPARSITY_DISTANCE_MEAN = 0.4
ROW_SPARSITY_DISTANCE_STD = 0.2
WEED_MAX_LENGTH = 0.5
WEED_MIN_LENGTH = 0.001
WEED_DIRECTIONAL_STD = math.pi / 6
WEED_CURVATURE_SHIFT_FACTOR = 0.3
WEED_CURVATURE_SCALE_CONSTANT = 0.2
WEED_CURVATURE_MIN_STD = 0.4


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def ccw(A, B, C):
    return (C.y - A.y) * (B.x - A.x) > (B.y - A.y) * (C.x - A.x)


# Return true if line segments AB and CD intersect
def intersect(A, B, C, D):
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)


def x_at_y(p1, p2, y):
    x1, y1 = p1
    x2, y2 = p2

    t = (y - y1) / (y2 - y1)
    return x1 + t * (x2 - x1)


def split_row(row_object, sparsity):
    num_splits = np.random.poisson(lam=((1 - sparsity) ** 2) * 5)
    if num_splits == 0:
        return [row_object]

    distance_between_splits = np.random.normal(
        loc=ROW_SPARSITY_DISTANCE_MEAN,
        scale=ROW_SPARSITY_DISTANCE_STD,
        size=num_splits,
    )

    distance_between_splits = list(np.clip(distance_between_splits, 0.05, None))

    # Split the line into num_splits + 1 segments
    split_ys = np.random.uniform(
        row_object["start_y"], row_object["end_y"], size=num_splits
    )
    split_ys = list(np.sort(split_ys))

    # If split points are too close to each other or to the boundary, remove one
    i = 1
    while i < len(split_ys):
        if (
            split_ys[i - 1] - (distance_between_splits[i - 1] / 2.0)
            < row_object["start_y"]
        ):
            split_ys.pop(i - 1)
            distance_between_splits.pop(i - 1)
        elif split_ys[i] + (distance_between_splits[i] / 2.0) > row_object["end_y"]:
            split_ys.pop(i)
            distance_between_splits.pop(i)
        elif split_ys[i] - split_ys[i - 1] < distance_between_splits[i - 1]:
            split_ys.pop(i)
            distance_between_splits.pop(i)
        else:
            i += 1

    line_segment_ys = []
    for i in range(len(split_ys) + 1):
        if i == 0:
            segment_start_y = row_object["start_y"]
        else:
            segment_start_y = split_ys[i - 1] + (distance_between_splits[i - 1] / 2.0)

        if i == len(split_ys):
            segment_end_y = row_object["end_y"]
        else:
            segment_end_y = split_ys[i] - (distance_between_splits[i] / 2.0)

        line_segment_ys.append((segment_start_y, segment_end_y))

    line_segment_xs = [
        (
            x_at_y(
                (row_object["start_x"], row_object["start_y"]),
                (row_object["end_x"], row_object["end_y"]),
                y[0],
            ),
            x_at_y(
                (row_object["start_x"], row_object["start_y"]),
                (row_object["end_x"], row_object["end_y"]),
                y[1],
            ),
        )
        for y in line_segment_ys
    ]

    objects = []
    for i in range(len(line_segment_ys)):
        split_row_object = {
            "start_x": line_segment_xs[i][0],
            "start_y": line_segment_ys[i][0],
            "end_x": line_segment_xs[i][1],
            "end_y": line_segment_ys[i][1],
            "num_spurs": row_object["num_spurs"],
            "curvature": row_object["curvature"],
            "cos_angle": row_object["cos_angle"],
            "sin_angle": row_object["sin_angle"],
        }
        objects.append(split_row_object)

    return objects


def generate_row_object(
    row_starting_x: float,
    row_class: int,
    row_sparsity: float = 1.0,
):
    row_x0 = np.clip(
        np.random.normal(loc=row_starting_x, scale=ROW_STD),
        -1.0,
        1.0,
    )
    row_x1 = np.clip(
        np.random.normal(loc=row_starting_x, scale=ROW_STD),
        -1.0,
        1.0,
    )

    row_y0 = np.clip(
        np.random.normal(loc=-1.0, scale=ROW_STD),
        -1.0,
        1.0,
    )
    row_y1 = np.clip(
        np.random.normal(loc=1.0, scale=ROW_STD),
        -1.0,
        1.0,
    )

    curvature = np.clip(
        np.random.normal(
            loc=ROW_CURVATURE_MEAN,
            scale=ROW_CURVATURE_STD,
        ),
        -1.0,
        1.0,
    )
    num_spurs = 0

    angle = math.atan2(row_y1 - row_y0, row_x1 - row_x0)
    cos_angle = math.cos(angle)
    sin_angle = math.sin(angle)

    row_object = {
        "start_x": row_x0,
        "start_y": row_y0,
        "end_x": row_x1,
        "end_y": row_y1,
        "num_spurs": num_spurs,
        "curvature": curvature,
        "cos_angle": cos_angle,
        "sin_angle": sin_angle,
    }

    if row_sparsity < 1.0:
        objects = split_row(row_object, row_sparsity)
        classes = [row_class] * len(objects)
    else:
        objects = [row_object]
        classes = [row_class]

    return objects, classes


def generate_weed_object():
    weed_x0 = random.uniform(-1.0, 1.0)
    weed_y0 = random.uniform(-1.0, 1.0)

    weed_length = random.uniform(WEED_MIN_LENGTH, WEED_MAX_LENGTH)
    weed_angle = np.random.normal(
        loc=3 * math.pi / 2,
        scale=WEED_DIRECTIONAL_STD,
    )

    weed_x1 = np.clip(weed_x0 + weed_length * math.cos(weed_angle), -1.0, 1.0)
    weed_y1 = np.clip(weed_y0 + weed_length * math.sin(weed_angle), -1.0, 1.0)

    num_spurs = 0
    weed_length_factor = (weed_length - WEED_MIN_LENGTH + 1e-6) / (
        WEED_MAX_LENGTH - WEED_MIN_LENGTH
    )
    curvature = np.clip(
        np.random.normal(
            loc=((((1 - weed_length_factor) * 2) - 1))
            * (1 - WEED_CURVATURE_SHIFT_FACTOR)
            - WEED_CURVATURE_SHIFT_FACTOR,
            scale=max(
                (1 - weed_length_factor) * WEED_CURVATURE_SCALE_CONSTANT,
                WEED_CURVATURE_MIN_STD,
            ),
        ),
        -1.0,
        1.0,
    )

    return {
        "start_x": weed_x0,
        "start_y": weed_y0,
        "end_x": weed_x1,
        "end_y": weed_y1,
        "num_spurs": num_spurs,
        "curvature": curvature,
        "cos_angle": math.cos(weed_angle),
        "sin_angle": math.sin(weed_angle),
    }


def generate_sample(
    colour_map: dict[tuple[int, int, int], int],
    num_rows: int = 5,
    row_class: int = 1,
    interspersed: bool = False,
    interspersed_num_rows: int = 0,
    interspersed_class: int = 2,
    row_sparsity: float = 1.0,
    num_weeds: dict[int, int] = {},
):
    objects = []
    classes = []

    row_offset = 2.0 / (num_rows + 1)
    initial_row_starting_x = random.uniform(-1.0, -1.0 + row_offset)
    row_starting_x = initial_row_starting_x
    for _ in range(num_rows):
        row_objects, row_classes = generate_row_object(
            row_starting_x=row_starting_x,
            row_class=row_class,
            row_sparsity=row_sparsity,
        )

        objects.extend(row_objects)
        classes.extend(row_classes)

        row_starting_x += row_offset

    if interspersed:
        interspersed_row_starting_x = initial_row_starting_x - (row_offset / 2.0)

        # Ensure interspersed row at index 0 is within bounds
        if interspersed_row_starting_x < -1.0:
            interspersed_row_starting_x += row_offset

        # Get maximum number of interspersed rows that fit
        num_interspersed_row_positions = num_rows
        half_offset = row_offset / 2.0
        if initial_row_starting_x - half_offset > -1.0:
            num_interspersed_row_positions += 1
        if initial_row_starting_x + (num_rows * row_offset) + half_offset < 1.0:
            num_interspersed_row_positions += 1

        # Select the starting position for interspersed rows
        interspersed_row_starting_index = random.randint(
            0, max(num_interspersed_row_positions - num_interspersed_row_positions, 0)
        )
        interspersed_row_starting_x += interspersed_row_starting_index * row_offset

        for _ in range(interspersed_num_rows):
            row_objects, row_classes = generate_row_object(
                row_starting_x=interspersed_row_starting_x,
                row_class=interspersed_class,
                row_sparsity=row_sparsity,
            )

            objects.extend(row_objects)
            classes.extend(row_classes)

            interspersed_row_starting_x += row_offset

    for weed_class, num_weed in num_weeds.items():

        for _ in range(num_weed):
            intersects = True
            while intersects:
                intersects = False

                weed_object = generate_weed_object()
                weed_start = Point(weed_object["start_x"], weed_object["start_y"])
                weed_end = Point(weed_object["end_x"], weed_object["end_y"])

                for obj in objects:
                    obj_start = Point(obj["start_x"], obj["start_y"])
                    obj_end = Point(obj["end_x"], obj["end_y"])
                    if intersect(weed_start, weed_end, obj_start, obj_end):
                        intersects = True
                        break

            objects.append(weed_object)
            classes.append(weed_class)

    synthetic = generate_multiclass_scribble(
        image_shape=(512, 512),
        objects=objects,
        classes=classes,
        colour_map=colour_map,
    )

    return synthetic


def generate_crop_field_dataset(
    output_dir: str,
    colour_map: dict,
    num_samples: int = NUM_SAMPLES_TO_GENERATE,
    min_rows: int = 4,
    max_rows: int = 6,
):
    os.makedirs(output_dir, exist_ok=True)

    for i in range(num_samples):
        num_rows = random.randint(min_rows, max_rows)
        row_class = random.randint(1, 3)
        interspersed = random.choice([True, False])
        interspersed_num_rows = random.randint(1, num_rows + 1)
        interspersed_class = random.choice([c for c in [1, 2, 3] if c != row_class])
        row_sparsity = random.uniform(0.1, 1.0)
        num_weeds = {
            2: random.randint(0, 5),
            3: random.randint(0, 10),
            4: random.randint(0, 10),
        }

        sample = generate_sample(
            colour_map=colour_map,
            num_rows=num_rows,
            row_class=row_class,
            interspersed=interspersed,
            interspersed_num_rows=interspersed_num_rows,
            interspersed_class=interspersed_class,
            row_sparsity=row_sparsity,
            num_weeds=num_weeds,
        )

        if random.random() < 0.5:
            sample = cv2.flip(sample, 1)

        output_path = os.path.join(output_dir, f"synthetic_{i:04d}.png")
        cv2.imwrite(output_path, cv2.cvtColor(sample, cv2.COLOR_RGB2BGR))
