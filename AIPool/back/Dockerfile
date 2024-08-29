FROM python:3.10.9

COPY requirements.txt requirements.txt

RUN apt update ;\
    apt install -y \
    ffmpeg \
    libsm6 \
    libxext6

RUN python -m pip install --upgrade pip ;\
    pip install /dist/*/* ;\
    pip install -r requirements.txt

