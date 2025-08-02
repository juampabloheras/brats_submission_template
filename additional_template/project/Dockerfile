# FROM python:3.9.16-slim
FROM pytorch/pytorch:1.12.0-cuda11.3-cudnn8-runtime
USER root

COPY ./requirements.txt /spark/requirements.txt 

RUN pip3 install -r /spark/requirements.txt

ENV LANG=C.UTF-8

COPY . /spark

# Set permissions for the /spark directory
RUN chmod -R 777 /spark

# RUN mkdir -p /spark/imagesTs && chmod -R 777 /spark/imagesTs

WORKDIR /spark

ENTRYPOINT ["python3", "/spark/mlcube.py"]