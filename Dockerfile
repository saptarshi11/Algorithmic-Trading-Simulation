FROM python:3.9-slim

WORKDIR /app
COPY /src .
RUN pip install -r requirements.txt

CMD gunicorn -b 127.0.0.1:80 app:server
