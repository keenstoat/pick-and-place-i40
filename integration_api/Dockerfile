FROM python:3.12.3-alpine

COPY rest_api /rest_api

WORKDIR /rest_api
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "."]