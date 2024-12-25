#!/bin/bash

./wait-for-it.sh warehouse_db:5433 --timeout=5 --strict -- echo "Database is up"
./wait-for-it.sh warehouse_storage:9001 --timeout=5 --strict -- echo "Storage is up"

# Apply database migrations
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py fill_data


# Create superuser if it doesn't exist
if [ "$DJANGO_SUPERUSER_USERNAME" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ]; then
    python manage.py createsuperuser --noinput --username "$DJANGO_SUPERUSER_USERNAME" --email "$DJANGO_SUPERUSER_EMAIL" || true
fi

python manage.py runserver 0.0.0.0:8000
