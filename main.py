import argparse
import os

def main(input_dir: str, output_dir: str):
    '''
    Placeholder, fill this in with your inference logic!
    '''
    print(f"Input directory: {input_dir}")
    print(f"Output directory: {output_dir}")

    for subject_path in os.listdir(input_dir):
        print(f'Subject Path: {subject_path}')


def parse_args():
    parser = argparse.ArgumentParser(description="Run the main processing pipeline.")
    parser.add_argument("-i", "--input", required=True, help="Path to input directory")
    parser.add_argument("-o", "--output", required=True, help="Path to output directory")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(input_dir=args.input, output_dir=args.output)
