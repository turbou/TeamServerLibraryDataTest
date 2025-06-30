#!/bin/sh

if [ $# -ne 1 ]; then
  echo "引数でEIPが渡されていません。"
  exit 1
fi
EIP=$1
echo "teamserver.url=http://${EIP}/Contrast を /opt/contrast/data/conf/general.properties に追記します。"
docker-compose -p eop exec teamserver sh -c "echo \"teamserver.url=http://${EIP}:8080/Contrast\" >> /opt/contrast/data/conf/general.properties"
if [ $? -eq 0 ]; then
  echo "設定への追記が正常に完了しました。"
else
  echo "設定への追記が失敗しました。"
  exit 1
fi

exit 0

