import docker
import os
import requests
import json
import time
import re
from datetime import datetime

def post_slack_message(message):
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post('https://hooks.slack.com/triggers/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', headers=headers, data=json.dumps(message))
        response.raise_for_status()
        print("Message sent to Slack workflow successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error sending message to Slack workflow: {e}")

def monitor_logs():
    pattern = r", started on (Sun|Mon|Tue|Wed|Thu|Fri|Sat) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (\d{1,2}) (\d{2}:\d{2}:\d{2}) JST (\d{4}),"
    pattern2 = r"^(\d{6}) (\d{2}\.\d{2}\.\d{2},\d{3}).*?Beginning CSV import.*?into '([^']+)'$"
    pattern3 = r"^(\d{6}) (\d{2}\.\d{2}\.\d{2},\d{3}).*?Insert records table '([^']+)'.*$"
    pattern4 = r"^(\d{6}) (\d{2}\.\d{2}\.\d{2},\d{3}).*?Beginning CSV import.*licenses.csv'$"
    pattern5 = r"^(\d{6}) (\d{2}\.\d{2}\.\d{2},\d{3}).*?Insert records complete.*$"
    #pattern3 = r"^(\d{6}) (\d{2}\.\d{2}\.\d{2},\d{3}).*?Import temporary table 'artifacts_dot_net' completed.*$"

    started_on = []
    beginning_csv = []
    beginning_start_dict = {}
    client = docker.from_env()
    try:
        container = client.containers.get('contrast.teamserver')
        while True:
            logs = container.logs(stream=False).decode('utf-8')
            for line in logs.splitlines():
                match = re.search(pattern, line)
                if match:
                    date_str = match.group(1) + " " + match.group(2) + " " + match.group(3) + " " + match.group(4) + " " + match.group(5)
                    date_object = datetime.strptime(date_str, "%a %b %d %H:%M:%S %Y")
                    started_on.append(date_object)
                    print('started on')
                    #print(f"抽出された日付文字列: {date_str}")
                    print(f"datetime オブジェクト: {date_object.strftime('%Y-%m-%d %H:%M:%S')}")
                    print('-------------------------------------------')

                match2 = re.search(pattern2, line)
                if match2:
                    date_str = match2.group(1)
                    time_str = match2.group(2)
                    artifacts_name = match2.group(3)
                    day = int(date_str[0:2])
                    month = int(date_str[2:4])
                    year = 2000 + int(date_str[4:6])
                    date_object = datetime.strptime(f"{year}{month}{day} {time_str}", "%Y%m%d %H.%M.%S,%f")
                    beginning_csv.append(date_object)
                    beginning_start_dict[artifacts_name ] = date_object
                    print('Beginning CSV import')
                    #print(f"抽出された日時文字列: {date_str} {time_str}")
                    print(f"datetime オブジェクト: {date_object.strftime('%Y-%m-%d %H:%M:%S')}")
                    print(f"抽出された artifacts 名: {artifacts_name}")
                    print('-------------------------------------------')

                match3 = re.search(pattern3, line)
                if match3:
                    date_str = match3.group(1)
                    time_str = match3.group(2)
                    artifacts_name = match3.group(3)
                    day = int(date_str[0:2])
                    month = int(date_str[2:4])
                    year = 2000 + int(date_str[4:6])
                    date_object = datetime.strptime(f"{year}{month}{day} {time_str}", "%Y%m%d %H.%M.%S,%f")
                    print('Insert records table')
                    #print(f"抽出された日時文字列: {date_str} {time_str}")
                    print(f"datetime オブジェクト: {date_object.strftime('%Y-%m-%d %H:%M:%S')}")
                    print(f"抽出された artifacts 名: {artifacts_name}")
                    if artifacts_name != 'artifacts_vulnerabilities_tmp':
                        time_diff = date_object - beginning_start_dict[artifacts_name]
                        total_seconds = time_diff.total_seconds()
                        total_hours = total_seconds / 3600
                        hours = int(total_seconds // 3600)
                        remaining_seconds = total_seconds % 3600
                        minutes = int(remaining_seconds // 60)
                        print(f"所要時間: {hours}時間 {minutes}分")
                    print('-------------------------------------------')

                match4 = re.search(pattern4, line)
                if match4:
                    date_str = match4.group(1)
                    time_str = match4.group(2)
                    day = int(date_str[0:2])
                    month = int(date_str[2:4])
                    year = 2000 + int(date_str[4:6])
                    date_object = datetime.strptime(f"{year}{month}{day} {time_str}", "%Y%m%d %H.%M.%S,%f")
                    beginning_csv.append(date_object)
                    beginning_start_dict['license' ] = date_object
                    print('Beginning CSV import(License)')
                    #print(f"抽出された日時文字列: {date_str} {time_str}")
                    print(f"datetime オブジェクト: {date_object.strftime('%Y-%m-%d %H:%M:%S')}")
                    print('-------------------------------------------')

                match5 = re.search(pattern5, line)
                if match5:
                    date_str = match5.group(1)
                    time_str = match5.group(2)
                    day = int(date_str[0:2])
                    month = int(date_str[2:4])
                    year = 2000 + int(date_str[4:6])
                    date_object = datetime.strptime(f"{year}{month}{day} {time_str}", "%Y%m%d %H.%M.%S,%f")
                    print('Insert records complete')
                    #print(f"抽出された日時文字列: {date_str} {time_str}")
                    print(f"datetime オブジェクト: {date_object}")
                    print('-------------------------------------------')
                    time_diff = date_object - beginning_csv[0]
                    total_seconds = time_diff.total_seconds()
                    total_hours = total_seconds / 3600
                    hours = int(total_seconds // 3600)
                    remaining_seconds = total_seconds % 3600
                    minutes = int(remaining_seconds // 60)
                    print(f"CSV読み込み開始: {beginning_csv[0].strftime('%Y-%m-%d %H:%M:%S')}")
                    print(f"CSV読み込み完了: {date_object.strftime('%Y-%m-%d %H:%M:%S')}")
                    print(f"所要時間: {hours}時間 {minutes}分")
                    message = {
                        "CONTRAST_URL": f"http://{os.environ['EIP']}/Contrast/",
                        "HOURS": f"所要時間: {hours}時間 {minutes}分 (os.environ['INSTANCE_TYPE'])"
                    }
                    print(message)
                    #post_slack_message(message)
                    return
            time.sleep(900)

    except docker.errors.APIError as e:
        print(f"Error reading logs from container '{container.name}': {e}")

if __name__ == "__main__":
    print("Log monitor started.")
    env_not_found = False
    for env_key in ['INSTANCE_TYPE', 'EIP']:
        if not env_key in os.environ:
            print('Environment variable %s is not set' % env_key)
            env_not_found |= True
    if env_not_found:
        sys.exit(1)
    monitor_logs()
    print("Log monitor finished.")

