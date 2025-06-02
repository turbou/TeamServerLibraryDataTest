#!/bin/sh

ZIP_FILENAME=$1
docker-compose -p eop exec teamserver bash -c "cd /work && unzip ${ZIP_FILENAME} -d /opt/contrast/data/libraries/"
exit $?

