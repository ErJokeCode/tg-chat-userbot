FROM python:3.13.2

WORKDIR /app/api

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "src/main.py"]