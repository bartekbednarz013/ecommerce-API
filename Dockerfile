FROM python:3.10-alpine

EXPOSE 8080
VOLUME /app/ecommerce/db.sqlite3
ENV PYTHONBUFFERED 1

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

WORKDIR /app/ecommerce
CMD python manage.py makemigrations && \
    python manage.py migrate && \
    python manage.py runserver 0.0.0.0:8080