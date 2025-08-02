""" main.py """

import sys
root_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(root_dir, 'nnUNet'))

import os
import torch
import shutil

from nnunetv2.inference.predict_from_raw_data import nnUNetPredictor
print(f"root_dir: {root_dir}")

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def process_brats_to_nnunet(input_dir: str, dest_dir: str):
    """
    Converts BraTS filenames to nnU-Net format and copies to the destination directory.
    """
    print("Converting BraTS filenames to nnU-Net format...")
    replacements = {"-t1c": "_0000", "-t1n": "_0001", "-t2f": "_0002", "-t2w": "_0003"}

    os.makedirs(dest_dir, exist_ok=True)
    for root, _, files in os.walk(input_dir):
        for filename in files:
            new_filename = filename
            for old, new in replacements.items():
                new_filename = new_filename.replace(old, new)
            src = os.path.join(root, filename)
            dst = os.path.join(dest_dir, new_filename)
            shutil.copy(src, dst)
    print("Conversion complete.")

def list_files(input_path: str):
    print(f"Files in {input_path}:")
    for root, _, files in os.walk(input_path):
        for f in files:
            print(os.path.join(root, f))

def make_nnUNet_inference_list(data_dir: str):
    """
    Returns a list of lists (each inner list contains a path to a single image file).
    nnU-Net expects a list of lists for each case.
    """
    nnunet_images = []
    for root, _, items in os.walk(data_dir):
        for item in items:
            if item.endswith('.nii.gz'):
                img_path = os.path.join(root, item)
                nnunet_images.append([img_path])
    return nnunet_images

def run_nnunet_inference(model_folder: str, dataset_dir: str, output_dir: str, folds=(0, 1, 2, 3, 4), checkpoint_name='checkpoint_final.pth'):
    predictor = nnUNetPredictor(
        tile_step_size=0.5,
        use_gaussian=True,
        use_mirroring=True,
        perform_everything_on_device=True,
        device=device,
        verbose=True,
        verbose_preprocessing=True,
        allow_tqdm=True
    )

    predictor.initialize_from_trained_model_folder(
        model_folder,
        use_folds=folds,
        checkpoint_name=checkpoint_name
    )

    os.makedirs(output_dir, exist_ok=True)

    files_list = make_nnUNet_inference_list(dataset_dir)
    predictor.predict_from_files_sequential(
        files_list,
        output_dir,
        overwrite=True,
        save_probabilities=False,
        folder_with_segs_from_prev_stage=None
    )

    print("Predictions saved to:", output_dir)
    print("Files:")
    list_files(output_dir)

model_dir = os.path.join(root_dir, "nnunet_model")   

def main(input_dir: str, output_dir: str, model_dir = model_dir):

    # 1. Convert BraTS to nnU-Net naming if needed
    imagesTs_dir = os.path.join(os.path.dirname(__file__), "imagesTs")
    process_brats_to_nnunet(input_dir, imagesTs_dir)
    list_files(imagesTs_dir)

    # 2. Run nnU-Net inference
    run_nnunet_inference(
        model_folder=model_dir,
        dataset_dir=imagesTs_dir,
        output_dir=output_dir
    )