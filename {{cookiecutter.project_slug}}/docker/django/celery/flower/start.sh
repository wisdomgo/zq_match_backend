#!/bin/bash

set -o errexit
set -o nounset


exec celery \
    -A server \
    -b "${CELERY_BROKER_URL}" \
    flower \
    --basic_auth="${CELERY_FLOWER_USER}:${CELERY_FLOWER_PASSWORD}" \
    --url-prefix=flower
