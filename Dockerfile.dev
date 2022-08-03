FROM python:3.10.4

ENV SRCDIR=./
ENV WORKDIR=/code/

WORKDIR ${WORKDIR}
COPY ${SRCDIR}requirements.txt ${WORKDIR}requirements.txt
RUN pip install -r requirements.txt
