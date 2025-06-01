#!/bin/sh

cd /opt/contrast/bin
MYSQL_PASSWORD=`./edit-properties --print-value -e ../data/esapi/ -f ../data/conf/database.properties -o -p jdbc.pass 2>/dev/null`
sed -i "s#MYSQL_PASSWORD=.*\$#MYSQL_PASSWORD=$MYSQL_PASSWORD#" /root/git/TeamServerLibraryDataTest/bare-metal/.env
if [ $? -eq 0 ]; then
  echo "MySQLのパスワード設定が正常に完了しました。"
else
  echo "MysQLのパスワード設定が失敗しました。"
  exit 1
fi

exit 0

