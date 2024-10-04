FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /fastapi

# Install system dependencies
RUN apt-get update && apt-get install -y cmake 

EXPOSE 8000

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY .env .

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
