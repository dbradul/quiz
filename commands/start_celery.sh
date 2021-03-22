#!/bin/bash

celery --workdir src -A app worker -l info -c $CELERY_NUM_WORKERS
