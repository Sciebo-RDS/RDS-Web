#!/usr/bin/env bash
export EXISTING_VARS=$(printenv | awk -F= '{print $1}' | sed 's/^/\$/g' | paste -sd,);
for file in $JSFOLDER;
do
  mv $file $file.bak
  cat $file.bak | envsubst $EXISTING_VARS > $file
  rm $file.bak
done

gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 -b 0.0.0.0:8080 --access-logfile "-" --log-file "-" --log-level "debug" starter:app