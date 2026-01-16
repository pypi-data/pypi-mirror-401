import cv2

from scribble_annotation_generator.nn.nn import ScribbleDataset
from scribble_annotation_generator.nn.utils import (
    generate_multiclass_scribble,
    unpack_feature_vector,
)


def parameterize_and_unparameterize():
    colour_map = {
        (0, 0, 0): 0,
        (0, 128, 255): 1,
        (124, 255, 121): 2,
        (127, 0, 0): 3,
        (255, 148, 0): 4,
        (0, 0, 127): 5,
    }
    dataset = ScribbleDataset(
        num_classes=3, data_dir="./local/soybean1", colour_map=colour_map
    )

    for i in range(len(dataset)):
        sample = dataset[i]

        objects = sample["objects"]
        classes = sample["classes"]

        objects = [unpack_feature_vector(obj) for obj in objects.numpy()]

        synthetic = generate_multiclass_scribble(
            image_shape=(512, 512),
            objects=objects,
            classes=classes,
            colour_map=colour_map,
        )

        # Save the synthetic scribble
        output_path = f"./local/nn-out/synthetic_{i:04d}.png"

        # Convert RGB to BGR for saving with OpenCV
        synthetic_bgr = cv2.cvtColor(synthetic, cv2.COLOR_RGB2BGR)
        cv2.imwrite(str(output_path), synthetic_bgr)
