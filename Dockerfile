FROM --platform=linux/amd64 pytorch/pytorch:2.2.0-cuda12.1-cudnn8-runtime
LABEL authors="YOUR_NAME"

RUN apt-get update -y

COPY requirements.txt .
RUN pip3 install --upgrade pip && \
   pip3 install -r requirements.txt

# Other necessary instructions 
COPY tools tools/
COPY checkpoints checkpoints/
COPY main.py .

CMD ["python", "main.py", "-i", "/input", "-o", "/output"]