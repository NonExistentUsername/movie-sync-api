FROM python:3.10.8

WORKDIR /app

COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]