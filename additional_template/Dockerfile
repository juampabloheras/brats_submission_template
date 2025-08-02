FROM --platform=linux/amd64 pytorch/pytorch:2.2.0-cuda12.1-cudnn8-runtime

LABEL authors="YOUR_NAME"

RUN apt-get update -y && apt-get install -y --no-install-recommends \
    libglib2.0-0 libsm6 libxrender1 libxext6 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy source code and model files into the container
COPY main.py .
COPY nnUNet ./nnUNet
COPY nnunet_model ./nnunet_model

WORKDIR /

CMD ["python", "main.py", "/input",  "/output"]
