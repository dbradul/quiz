#!/bin/bash

rm /tmp/celerybeat-schedule /tmp/celerybeat.pid
celery --workdir src -A app beat -l info --schedule=/tmp/celerybeat-schedule --pidfile=/tmp/celerybeat.pid
