FROM python:3.11-slim

WORKDIR /API_model

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./API_model .
COPY ./src/model ./model

EXPOSE 8000

# export logs to mlflow
ENV MLFLOW_TRACKING_URI=http://host.docker.internal:5001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]