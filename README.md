# BraTS 2025 Submission Template

This repository is a minimal template for packaging your BraTS submission inside a Docker container.  Follow the steps below to build, test, and push your image to the Synapse container registry.

> 📄 **Official submission guide:** [https://www.synapse.org/Synapse\:syn64153130/wiki/633742](https://www.synapse.org/Synapse:syn64153130/wiki/633742)

---

## 1  Quick Start – Clone the template

```bash
# Clone the repository and enter the directory
git clone https://github.com/juampabloheras/brats_submission_template.git
cd brats_submission_template
```

---

## 2  Repository layout

```text
.
├── Dockerfile                  # Runtime base (PyTorch + CUDA 12.1)
├── build_and_run_commands.sh   # Helper script: build / test / push
├── requirements.txt            # Python dependencies
├── checkpoints/                # Example weights
│   └── final_epoch.pth
├── main.py                     # BraTS‑spec entry‑point
├── tools/                      # Pipeline utilities
│   ├── inference.py
│   ├── postprocessing.py
│   ├── preprocessing.py
│   ├── read_write.py
│   ├── sitk_stuff.py
│   └── torch_stuff.py
└── data/                       # Example I/O for local tests
    ├── example_input/
    └── example_output/         # Populated after a test run
```

---

## 3  Authenticate with Synapse

```bash
# Log in to the Synapse Docker registry
# Use your **Personal Access Token (PAT)** when prompted for a password
export SYNAPSE_USERNAME="<your‑synapse‑username>"

docker login docker.synapse.org -u "$SYNAPSE_USERNAME"
```

*Create a PAT*: [https://python-docs.synapse.org/en/stable/tutorials/authentication/#personal-access-tokens](https://python-docs.synapse.org/en/stable/tutorials/authentication/#personal-access-tokens)

---

## 4  Define environment variables

```bash
# Mandatory
PROJECT_ID="synXXXXXXXX"      # ← Your Synapse project ID
IMAGE_NAME="brats-ssa-spark-thebest"  # ← Your desired Docker image name
TAG="latest"                 # ← Image tag (e.g. latest, v1)


DOCKERFILE_DIR="."            # Directory containing the Dockerfile

# Local test paths (these should be absolute paths!) 
INPUT_DIR="$(pwd)/data/example_input"
OUTPUT_DIR="$(pwd)/data/example_output"
```

*Need a new project for a PROJECT_ID?* [https://www.synapse.org/Synapse\:syn64153130/wiki/632674#Create-a-Synapse-Project](https://www.synapse.org/Synapse:syn64153130/wiki/632674#Create-a-Synapse-Project)

---

## 5  Build the Docker image

```bash
docker build -t docker.synapse.org/$PROJECT_ID/$IMAGE_NAME:$TAG "$DOCKERFILE_DIR"
```

---

## 6  Local test run

### CPU‑only (no network)

```bash
docker run \
  --rm \
  --network none \
  --env NVIDIA_VISIBLE_DEVICES=0 \
  --volume "$INPUT_DIR":/input:ro \
  --volume "$OUTPUT_DIR":/output:rw \
  --memory 16G --shm-size 4G \
  docker.synapse.org/$PROJECT_ID/$IMAGE_NAME:$TAG
```

Check `data/example_output` for the generated results.

### GPU (Linux + CUDA host)

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

*Note*: This is the same configuration the Synapse evaluation system uses.

---

## 7  Push the image to Synapse 

```bash
docker push docker.synapse.org/$PROJECT_ID/$IMAGE_NAME:$TAG
```

Ensure you have **Docker Push/Pull** permissions for your PAT and that the Docker repository has been created under your project.

---

