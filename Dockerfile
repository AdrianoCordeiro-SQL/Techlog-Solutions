FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir fastapi[standard] uvicorn[standard]

COPY app/ ./app/
COPY static/ ./static/
COPY templates/ ./templates/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
