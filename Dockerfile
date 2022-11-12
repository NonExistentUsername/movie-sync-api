FROM python:3.10.8

WORKDIR /app

COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir mysqlclient

RUN rm requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--workers", "1", "--host", "0.0.0.0", "--port", "8000"]