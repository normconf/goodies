FROM python:3.10

# Install python/pip

COPY projects/wh_app/ /app

COPY projects/wh_app/requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

ENV ENV="INTEGRATION"

EXPOSE 8000

CMD uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
