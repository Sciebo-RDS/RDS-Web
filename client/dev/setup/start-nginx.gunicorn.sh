#!/usr/bin/env bash
export EXISTING_VARS=$(printenv | awk -F= '{print $1}' | sed 's/^/\$/g' | paste -sd,);
for file in $JSFOLDER;
do
  mv $file $file.bak
  cat $file.bak | envsubst $EXISTING_VARS | tee $file
  rm $file.bak
done
gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:5000 starter:app --log-level debug > /dev/stdout &
nginx -g 'daemon off;' > /dev/stdout