#!/bin/bash
# ------------------------------------------------------------------------------
# Instructions for building, running, and submitting a Docker image to Synapse
# for BraTS25 submission.
#
# Reference: https://www.synapse.org/Synapse:syn64153130/wiki/633742
#
# This script is split into several steps:
#   1. Log in to the Synapse Docker registry
#   2. Build the Docker image
#   3. Run the Docker image (with or without GPU)
#   4. Push the Docker image to Synapse
#
# Replace the variables below with your own values before running the script.
# Variables that need to be changed have a (**).
# Be sure to uncomment the lines for the steps you want to execute, and comment again after running them.
# ------------------------------------------------------------------------------



# Replace the variables below with your own values before running the script. Variables that need to be changed have a (**). Keep this section uncommented.

PROJECT_ID="synXXXXXXXX" #  (**) Change to your Project Synapse Project ID (same as the one in the val stage)
IMAGE_NAME="brats-ssa-spark" # (**) The name you would like to give your Docker image 
TAG="latest"  # Tag for the Docker image (e.g., "latest", "v1", etc.)
DOCKERFILE_DIR="." # Directory containing the Dockerfile

INPUT_DIR="$(pwd)/data/example_input" # Absolute path to the input directory 
OUTPUT_DIR="$(pwd)/data/example_output" # Absolute path to the output directory

SYNAPSE_USERNAME="your_username" # (**) Replace with your Synapse username 



# Step 1) #
# First, log in to the Synapse Docker registry
# ** You will need to create a Personal Access Token (PAT) in Synapse and use it as your password. **
# Instructions for creating a PAT can be found here:
# https://python-docs.synapse.org/en/stable/tutorials/authentication/#:~:text=Create%20a-,Personal%20Access%20Token,-(aka%3A%20Synapse

# docker login docker.synapse.org --username $SYNAPSE_USERNAME



# Step 2) # Build the image

# echo "Building Docker image: docker.synapse.org/$PROJECT_ID/$IMAGE_NAME:$TAG"
# docker build -t docker.synapse.org/$PROJECT_ID/$IMAGE_NAME:$TAG $DOCKERFILE_DIR



# Step 3) # Run the image (no GPU, no network)- Useful for testing before submitting to Synapse

# echo "Running container (no GPU, no network)..."
docker run \
    --rm \
    --network none \
    --env NVIDIA_VISIBLE_DEVICES=0 \
    --volume $INPUT_DIR:/input:ro \
    --volume $OUTPUT_DIR:/output:rw \
    --memory=16G --shm-size 4G \
    docker.synapse.org/$PROJECT_ID/$IMAGE_NAME:$TAG



# Step 3b) (optional) # Run the image (with GPU, no network) - This is how evaluation will be done in Synapse. Only uncomment this if you have a GPU available and want to test the full functionality.

# echo "Running container (GPU, no network)..."
# docker run \
#     --rm \
#     --network none \
#     --gpus=all \
#     --volume INPUT_DIR:/input:ro \
#     --volume OUTPUT_DIR:/output:rw \
#     --memory=16G --shm-size 4G \
#     docker.synapse.org/$PROJECT_ID/$IMAGE_NAME:$TAG



# Step 4) # Once the container has been successfully run, you can push the image to Synapse. This takes a while since it uploads the entire image to the registry.

# echo "Pushing Docker image to Synapse..."
# docker push docker.synapse.org/$PROJECT_ID/$IMAGE_NAME:$TAG
