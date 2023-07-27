ARG version=3.11
FROM python:${version}

WORKDIR /workspace
RUN pip install --upgrade pip \
    && apt-get update \
    && apt-get install -y \
        freetds-dev \
    && rm -rf /var/lib/apt/lists/*
ARG version=3.11
COPY requirements/${version}.txt requirements.txt
COPY setup.py README.rst ./
RUN pip install -r requirements.txt
COPY . .
