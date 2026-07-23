FROM python:3.13-slim

WORKDIR /app
COPY . /app


RUN pip install -r requirements.txt

COPY . .

RUN python -m src.pipeline.train_pipeline

EXPOSE 8080
CMD ["python", "app.py"]