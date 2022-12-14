FROM python:3.10.4

ENV SRCDIR=./
ENV WORKDIR=/code/

WORKDIR ${WORKDIR}
COPY ${SRCDIR} ${WORKDIR}
RUN pip install -r requirements.txt
EXPOSE 8000