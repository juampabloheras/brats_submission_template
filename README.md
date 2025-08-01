# BraTS 2025 Submission Template

This repository is a template for packaging your BraTS submission in a reproducible Docker container. 
Follow the steps below to build, test, and push your image to the Synapse Docker registry.

Reference: https://www.synapse.org/Synapse:syn64153130/wiki/633742

---
##  Quick start- clone this template

```bash
$ git clone https://github.com/juampabloheras/brats_submission_template.git && cd brats_submission_template
```
---

##  Repository template layout

```text
.
├── Dockerfile                # Runtime image (PyTorch + CUDA 12.1)
├── build_and_run_commands.sh # Helper script to build / test / push
├── requirements.txt          # Python dependencies
├── checkpoints/
│   └── final_epoch.pth       # Example model weights
├── main.py                   # Entry‑point according to BraTS specification
├── tools/                    # Pipeline utilities
│   ├── inference.py
│   ├── postprocessing.py
│   ├── preprocessing.py
│   ├── read_write.py
│   ├── sitk_stuff.py
│   └── torch_stuff.py
└── data/
    ├── example_input/        # Tiny sample case for local tests
    └── example_output/       # Populated after a local run
```

---

The following steps are included in the build_and_run_commands.sh file as well.

## Log into Synapse:

   ```bash
   docker login docker.synapse.org -u "$SYNAPSE_USERNAME" 
   ```

> When prompted for a password, use your Synapse **Personal Access Tokens (PAT)**. Instructions for creating a PAT can be found here: https://python-docs.synapse.org/en/stable/tutorials/authentication/#:~:text=Create%20a-,Personal%20Access%20Token,-(aka%3A%20Synapse

## Define your specific variables
```bash
PROJECT_ID="synXXXXXXXX" #  (**) Change to your Project Synapse Project ID (same as the one in the val)
IMAGE_NAME="brats-ssa-spark" # (**) The name you would like to give your Docker image 
TAG="latest"  # Tag for the Docker image (e.g., "latest", "v1", etc.)
DOCKERFILE_DIR="." # Directory containing the Dockerfile

INPUT_DIR="$(pwd)/data/example_input" # Absolute path to the input directory 
OUTPUT_DIR="$(pwd)/data/example_output" # Absolute path to the output directory

SYNAPSE_USERNAME="your_username" # (**) Replace with your Synapse username 
```
> If you need to create a new project to get the PROJECT_ID, instructions can be found here: https://www.synapse.org/Synapse:syn64153130/wiki/632674#:~:text=to%20the%20Challenge.-,Create,-a%20Synapse%20Project

##  Building the image manually

```bash
docker build -t docker.synapse.org/$PROJECT_ID/$IMAGE_NAME:$TAG .
```


---

##  Local test run

Runs the image with no GPU and no network. This is useful for testing before submitting to Synapse.
```bash
# CPU‑only test (no network)
docker run \
  --rm \
  --network none \
  --env NVIDIA_VISIBLE_DEVICES=0 \
  --volume "$INPUT_DIR":/input:ro \
  --volume "$OUTPUT_DIR":/output:rw \
  --memory 16G --shm-size 4G \
  docker.synapse.org/$PROJECT_ID/$IMAGE_NAME:$TAG
```

Inspect `/data/example_output` to confirm the pipeline produced results.

### GPU test (Linux + CUDA host)
This is how evaluation will be done in Synapse. Only run this if you have a GPU available and want to test the full functionality.
```bash
docker run \
  --rm \
  --network none \
  --gpus all \
  --volume "$INPUT_DIR":/input:ro \
  --volume "$OUTPUT_DIR":/output:rw \
  --memory 16G --shm-size 4G \
  docker.synapse.org/$PROJECT_ID/$IMAGE_NAME:$TAG
```

---

