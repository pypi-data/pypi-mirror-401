import argparse
from bw_converter.converter import process_image

def main():
    parser = argparse.ArgumentParser(description="Convert a color image to black and white.")
    parser.add_argument("input", help="Path to the input image")
    parser.add_argument("output", help="Path to save the output image")

    args = parser.parse_args()

    process_image(args.input, args.output)

if __name__ == "__main__":
    main()
