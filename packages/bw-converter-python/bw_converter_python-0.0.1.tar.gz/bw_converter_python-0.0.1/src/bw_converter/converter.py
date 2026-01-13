from PIL import Image
import os

def process_image(input_path: str, output_path: str):
    """
    Converts a color image to black and white.

    Args:
        input_path (str): Path to the input image.
        output_path (str): Path to save the black and white image.
    """
    try:
        with Image.open(input_path) as img:
            bw_img = img.convert("L")
            bw_img.save(output_path)
            print(f"Successfully converted '{input_path}' to '{output_path}'")
    except FileNotFoundError:
        print(f"Error: The file '{input_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
