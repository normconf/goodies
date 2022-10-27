FROM python:3.10-slim

# Copy requirements before building so as to not invalidate build cache
COPY requirements.txt app/requirements.txt
WORKDIR /app
RUN pip install -r /app/requirements.txt
COPY . /app

ENV ENV="INTEGRATION"

EXPOSE 8000

CMD uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
