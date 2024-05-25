import numpy as np
import cv2
from PIL import Image
from scipy.spatial import KDTree


def load_image(image_path):
    try:
        pil_image = Image.open(image_path)
        image = np.array(pil_image)
        if image is None:
            raise ValueError(f"Image at path '{image_path}' could not be loaded.")
        if len(image.shape) == 2:  # Grayscale image
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        elif image.shape[2] == 4:  # Image with alpha channel
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
        return image
    except Exception as e:
        raise FileNotFoundError(f"Image file could not be loaded: {e}")


def create_mosaic(image, wall_width, wall_height, chip_width, chip_height, chip_colors):
    image_height, image_width, _ = image.shape

    # Calculate the number of chips needed
    num_chips_x = wall_width // chip_width
    num_chips_y = wall_height // chip_height

    # Resize image to match the number of chips
    resized_image = cv2.resize(image, (num_chips_x, num_chips_y))

    # Create the mosaic image
    mosaic_image = np.zeros((wall_height, wall_width, 3), dtype=np.uint8)

    # Create KDTree for fast nearest-neighbor search
    chip_tree = KDTree(chip_colors)

    for y in range(num_chips_y):
        for x in range(num_chips_x):
            # Extract the block of pixels corresponding to the current chip
            block = resized_image[y:y + 1, x:x + 1]

            # Calculate the mean color of the block
            mean_color = np.mean(block, axis=(0, 1))

            # Find the nearest color from chip_colors
            _, idx = chip_tree.query(mean_color)
            chip_color = chip_colors[idx]

            # Fill the corresponding area in the mosaic image
            mosaic_image[
            y * chip_height: (y + 1) * chip_height,
            x * chip_width: (x + 1) * chip_width
            ] = chip_color

    return mosaic_image
