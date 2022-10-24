FROM python:3.10-slim

# Install python/pip

COPY ./app /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r app/requirements.txt

ENV ENV="INTEGRATION"

EXPOSE 8000

CMD uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
