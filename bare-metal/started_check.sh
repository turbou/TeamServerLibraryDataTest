#!/bin/sh

MAX_RETRIES=20
SLEEP_SECONDS=30
for i in $(seq 1 $MAX_RETRIES); do
  LOGS=$(docker-compose -p eop logs teamserver)
  if echo "$LOGS" | grep -q " started on "; then
    echo "TeamServer started successfully."
    break
  fi  
  echo "Waiting for TeamServer to start... (Attempt $i/$MAX_RETRIES)"
  sleep $SLEEP_SECONDS
  if [ $i -eq $MAX_RETRIES ]; then
    echo "TeamServer did not start within the expected time."
    exit 1
  fi  
done

exit 0

