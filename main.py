import argparse
import os
from tools.read_write import save_nii, load_nii



def main(input_dir: str, output_dir: str):
    '''
    Placeholder, fill this in with your inference logic!
    '''
    print(f"Input directory: {input_dir}")
    print(f"Output directory: {output_dir}")

    for subject_path in os.listdir(input_dir):
        img_paths = {
            't1n':f'{subject_path}-t1n.nii.gz',
            't1c':f'{subject_path}-t1c.nii.gz',
            't2w':f'{subject_path}-t2w.nii.gz',
            't2f':f'{subject_path}-t2f.nii.gz',
        }
        img_paths = {contrast: os.path.join(input_dir, pth) for contrast, pth in img_paths.items()}
        predicted_seg = infer_one_subject(img_paths=img_paths)
        
        
        # Save prediction
        _, affine, header = load_nii(img_paths['t1n'])
        save_path = os.path.join(output_dir, f'{subject_path}.nii.gz')
        save_nii(predicted_seg, save_path, affine, header)
        print(f"Saved prediction to {save_path}")



def infer_one_subject(img_paths: dict):
    print(f'Running inference using: {img_paths}')
    ## Load images
    # images = {contrast:load_nii(pth)[0] for contrast, pth in img_paths.items()}

    ## Preprocess, Model Inference, Postprocessing Code here...
    return None


def parse_args():
    parser = argparse.ArgumentParser(description="Run the main processing pipeline.")
    parser.add_argument("-i", "--input", required=True, help="Path to input directory")
    parser.add_argument("-o", "--output", required=True, help="Path to output directory")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(input_dir=args.input, output_dir=args.output)
