FROM python:3.8-alpine

ENV PYTHONPATH="$PYTHONPATH:/app"

COPY . /app
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD gunicorn -w 4 -k uvicorn.workers.UvicornWorker --port 8000 --log-level info src.main:app