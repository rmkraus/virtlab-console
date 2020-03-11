source /opt/my_python/bin/activate


if [ -e /data/cert.pem ] && [ -e /data/privkey.pem ]; then
    gunicorn -b 0.0.0.0:8443 --certfile /data/cert.pem --keyfile=/data/privkey.pem wsgi:app
else
    gunicorn -b 0.0.0.0:8080 wsgi:app
fi
