#!/bin/bash
# bootstrap environment
source /opt/my_python/bin/activate
mkdir -p /data/logs
mkdir -p /data/db
mkdir -p /data/nginx/tmp
export MONGO_PID=""

function mongo_start() {
    mongod --port 27017 --bind_ip 127.0.0.1 --dbpath /data/db &> /data/logs/mongodb.log &
    export MONGO_PID=$!
}

function mongo_stop() {
    if kill -0 $MONGO_PID; then
        kill $MONGO_PID
    fi
}

function mongo_schema_update() {
    python schema.py 2>&1 | tee /data/logs/console_setup.log
}

function nginx_start() {
    nginx -c /app/nginx.conf
}

function nginx_stop () {
    nginx -c /app/nginx.conf -s stop
}

function gunicorn_run() {
    GUNICORN_PORT=8080
    GUNICORN_LOGGING="--log-level info --access-logfile -"
    GUNICORN_ARGS="-w 20"

    if [[ "$1" == "debug" ]]; then
        pip install inotify
        GUNICORN_LOGGING="--log-level debug --access-logfile -"
        GUNICORN_ARGS+=" --reload"
    fi
    if [ -e /data/cert.pem ] && [ -e /data/privkey.pem ]; then
        GUNICORN_PORT=8443
        GUNICORN_ARGS+=" --certfile /data/cert.pem --keyfile /data/privkey.pem"
    fi

    gunicorn -b 0.0.0.0:$GUNICORN_PORT $GUNICORN_LOGGIN $GUNICORN_ARGS wsgi:app 2>&1 | tee /data/logs/console.log
}


mongo_start
mongo_schema_update
nginx_start
gunicorn_run
nginx_stop
mongo_stop
