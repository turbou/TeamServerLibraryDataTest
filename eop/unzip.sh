#!/bin/sh

docker-compose -p eop exec teamserver bash -c "cd /work && unzip Contrast-Data-Export-*.zip -d /opt/contrast/data/libraries/"

exit 0

