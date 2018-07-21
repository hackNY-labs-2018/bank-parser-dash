FROM ubuntu:16.04
ADD . parser
WORKDIR parser
RUN apt-get update && apt-get install -y \
	ghostscript \
	imagemagick \
	libmagickwand-dev \
	libtesseract-dev \
	python3 \
	python3-pip \
	tesseract-ocr
RUN pip3 install -r requirements.txt
ENV LANG C.UTF-8

