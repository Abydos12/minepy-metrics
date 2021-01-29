FROM python:3.8-alpine

ENV PYTHONPATH="$PYTHONPATH:/app"

COPY . /app
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD uvicorn src.main:app --port 8000