FROM python:3.12-slim

WORKDIR /app

COPY code/deployment/api/requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY code/deployment/api/main.py main.py

COPY models/model.joblib models/model.joblib

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]