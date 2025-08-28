FROM python:3.11-slim

RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 10000

CMD python manage.py migrate && python manage.py setup_rooms && python manage.py create_initial_users && gunicorn --bind 0.0.0.0:10000 hotel_pms.wsgi:application