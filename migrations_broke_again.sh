#!/usr/bin/sh

rm db.sqlite3
rm -r ./**/__pycache__/
rm -r ./*/migrations/
mkdir main/migrations solution_manager/migrations
touch main/migrations/__init__.py solution_manager/migrations/__init__.py
python3 ./manage.py makemigrations
python3 ./manage.py migrate --run-syncdb
