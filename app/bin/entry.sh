source /opt/my_python/bin/activate

gunicorn -b 0.0.0.0:8080 -w 1 --threads 1 wsgi:app
