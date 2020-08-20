#!/bin/sh

export ROOT_SUBDIRECTORY_PATH

envsubst '${ROOT_SUBDIRECTORY_PATH}' < /etc/nginx/config.template > /etc/nginx/conf.d/default.conf

nginx -g "daemon off;"
