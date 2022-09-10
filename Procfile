web: gunicorn project.wsgi
reslease: python manage.py makemigrations --noinput
reslease: python manage.py collectstatic --noinput
reslease: python manage.py migrate --noinput
reslease: python manage.py runscript create_db_data