#!/bin/bash

# Wait for MySQL to be ready
until nc -z "$DB_HOST" "$DB_PORT"; do
  echo "sleeping"
  sleep 1
done

echo "MySQL is up"

poetry run python manage.py makemigrations
poetry run python manage.py migrate

# Insert initial items setup
poetry run python manage.py runscript \
    insert_categories_fromconfig \
    insert_itemtypes_fromconfig \
    insert_materials_fromconfig \
    insert_enchantments_fromconfig

exec "$@"