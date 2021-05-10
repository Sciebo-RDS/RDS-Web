#!/usr/bin/env bash
export EXISTING_VARS=$(printenv | awk -F= '{print $1}' | sed 's/^/\$/g' | paste -sd,);
for file in $JSFOLDER;
do
  cat $file | envsubst $EXISTING_VARS | tee $file
done
gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:5000 starter:app --log-level debug --daemon && nginx -g 'daemon off;'