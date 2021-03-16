#!/bin/bash


gunicorn -w ${WSGI_WORKERS} -b 0:${WSGI_PORT} --chdir ./src app.wsgi:application --log-level=${WSGI_LOG_LEVEL}