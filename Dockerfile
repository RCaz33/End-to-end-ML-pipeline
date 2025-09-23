FROM python:3.11-slim

WORKDIR /API_model

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY ./src/model ./model

EXPOSE 8000

CMD ["uvicorn", "main:API_model", "--host", "0.0.0.0", "--port", "8000"]