#!/bin/sh

DIRECTORY="/opt/contrast/work"
CHECK_INTERVAL=60
TIMEOUT=180

START_TIME=`date +%s`
while true; do
  TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
  MD5SUM_FILE=`find $DIRECTORY -maxdepth 1 -name "*.zip-md5.txt"`
  if [ -z "$MD5SUM_FILE" ]; then
    echo "エラー: MD5SUMファイルが存在しません。"
  else
    echo "MD5SUMファイル '$MD5SUM_FILE' が見つかりました。"
    break
  fi
  CURRENT_TIME=`date +%s`
  ELAPSED_TIME=`expr "$CURRENT_TIME" - "$START_TIME"`
  if [ "$ELAPSED_TIME" -ge "$TIMEOUT" ]; then
    echo "Timeout reached (${TIMEOUT} seconds). Exiting."
    exit 1
  fi
  echo "Waiting for ${CHECK_INTERVAL} seconds..."
  sleep "$CHECK_INTERVAL"
done

base_name=`basename $MD5SUM_FILE .zip-md5.txt`
ZIP_FILE="${DIRECTORY}/${base_name}.zip"

EXPECTED_MD5SUM=`cat "$MD5SUM_FILE"`
if [ -z "$EXPECTED_MD5SUM" ]; then
  echo "エラー: MD5SUMファイル '$DIRECTORY/$MD5SUM_FILE' が空です。"
  exit 1
fi

echo "期待するMD5SUM: $EXPECTED_MD5SUM"

# チェック処理
TIMEOUT=600
START_TIME=`date +%s`
while true; do
  TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
  if [ -f "$ZIP_FILE" ]; then
    echo "$TIMESTAMP: ZIPファイル '$ZIP_FILE' が存在します。MD5SUMを計算します..."
    ACTUAL_MD5SUM=`md5sum "$ZIP_FILE" | awk '{print $1}'`
    echo "$TIMESTAMP: ZIPファイルのMD5SUM: $ACTUAL_MD5SUM"
    if [ "$EXPECTED_MD5SUM" == "$ACTUAL_MD5SUM" ]; then
      echo "$TIMESTAMP: MD5SUMが一致しました！"
      exit 0
    else
      echo "$TIMESTAMP: MD5SUMが一致しません。再試行します..."
    fi
  else
    echo "$TIMESTAMP: ZIPファイル '$ZIP_FILE' はまだ存在しません。待機します..."
  fi

  CURRENT_TIME=`date +%s`
  ELAPSED_TIME=`expr "$CURRENT_TIME" - "$START_TIME"`
  if [ "$ELAPSED_TIME" -ge "$TIMEOUT" ]; then
    echo "Timeout reached (${TIMEOUT} seconds). Exiting."
    exit 1
  fi
  echo "Waiting for ${CHECK_INTERVAL} seconds..."
  sleep "$CHECK_INTERVAL"
done

