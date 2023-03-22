FROM python:3.10.10

ARG APP_DIR=/app
ARG APPLICATION_PORT=8000
ARG PATH_TO_LOG=logs

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
ENV PATH=$PATH:${APP_DIR} PYTHONPATH=${APP_DIR}

ENV PATH_TO_LOG=${PATH_TO_LOG}
ENV APPLICATION_PORT=${APPLICATION_PORT}
EXPOSE ${APPLICATION_PORT}

RUN apt-get update && apt-get install -y cron

# Create app directory
WORKDIR ${APP_DIR}

# Install app dependencies
ADD requirements.txt ${APP_DIR}
RUN mkdir ${PATH_TO_LOG} && pip install -r requirements.txt
ADD . ${APP_DIR}
