import os
import cv2


def resize_labels_in_directory(base_dir, label_size):
    """
    Resizes the labels of all images within a dataset directory to a consistent size and replaces the original images.

    Args:
        base_dir (str): The base directory containing the label folders.
        label_size (tuple): The desired size for the labels (width, height).
    """
    # Iterate through each label folder
    for label_folder in os.listdir(base_dir):
        try:
            label_dir = os.path.join(base_dir, label_folder)

            # Iterate through each image in the label folder
            for filename in os.listdir(label_dir):
                # Check if the file is an image
                if filename.endswith('.jpg') or filename.endswith('.png'):
                    # Load the image
                    image_path = os.path.join(label_dir, filename)
                    try:
                        image = cv2.imread(image_path)
                    except cv2.error as e:
                        print(f"Error reading image {filename}: {e}")
                        continue

                    # Resize the label
                    try:
                        label = cv2.resize(image, label_size, interpolation=cv2.INTER_AREA)
                        # Save the resized image to the same location
                        cv2.imwrite(image_path, label)
                    except cv2.error as e:
                        print(f"Error resizing or writing image {filename}: {e}")
                        continue
        except Exception as e:
            print(f"Error processing label folder {label_folder}: {e}")

        print(f'Label resizing complete for folder: {label_folder}')

    print('All label resizing complete.')


#resize_labels_in_directory("train", (500, 500))