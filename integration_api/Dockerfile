FROM python:3.12.3-alpine

COPY app /app

WORKDIR /app
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "."]