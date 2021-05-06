FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .

USER nobody

CMD ["python3", "app/app.py"]

EXPOSE 5000