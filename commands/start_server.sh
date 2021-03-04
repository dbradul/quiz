#!/bin/bash


python src/manage.py runserver --settings=app.settings.${MODE} 0:${WSGI_PORT}
