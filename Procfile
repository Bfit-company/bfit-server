web: gunicorn bfit.wsgi
release: python manage.py makemigrations --no-input
release: python manage.py migrate --no-input
web: python manage.py runserver 0.0.0.0:$PORT --noreload
