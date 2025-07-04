#!/bin/sh

if [ $# -ne 1 ]; then
  echo "引数でFILE_NAMEが渡されていません。"
  exit 1
fi
FILE_NAME=$1
DIRECTORY="/opt/contrast/work"
CHECK_INTERVAL=60
TIMEOUT=180

START_TIME=`date +%s`
MD5SUM_FILE="${DIRECTORY}/${FILE_NAME}-md5.txt"
while true; do
  TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
  if [ -f "$MD5SUM_FILE" ] && [ -s "$MD5SUM_FILE" ]; then
    echo "MD5SUMファイル '$MD5SUM_FILE' が見つかりました。"
    break
  else
    echo "エラー: MD5SUMファイルが存在しない、またはファイルサイズが０です。"
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

ZIP_FILE="${DIRECTORY}/${FILE_NAME}"

EXPECTED_MD5SUM=`cat "$MD5SUM_FILE"`
if [ -z "$EXPECTED_MD5SUM" ]; then
  echo "エラー: MD5SUMファイル '$MD5SUM_FILE' が空です。"
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

