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
    pattern3 = r"^(\d{6}) (\d{2}\.\d{2}\.\d{2},\d{3}).*?Insert records complete.*$"
    #pattern3 = r"^(\d{6}) (\d{2}\.\d{2}\.\d{2},\d{3}).*?Import temporary table 'artifacts_dot_net' completed.*$"

    started_on = []
    beginning_csv = []
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
                    print(f"抽出された日付文字列: {date_str}")
                    print(f"datetime オブジェクト: {date_object}")
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
                    print(f"抽出された日時文字列: {date_str} {time_str}")
                    print(f"datetime オブジェクト: {date_object}")
                    print(f"抽出された artifacts 名: {artifacts_name}")
                    print('-------------------------------------------')
        
                match3 = re.search(pattern3, line)
                if match3:
                    date_str = match3.group(1)
                    time_str = match3.group(2)
                    day = int(date_str[0:2])
                    month = int(date_str[2:4])
                    year = 2000 + int(date_str[4:6])
                    date_object = datetime.strptime(f"{year}{month}{day} {time_str}", "%Y%m%d %H.%M.%S,%f")
                    print('Insert records complete')
                    print(f"抽出された日時文字列: {date_str} {time_str}")
                    print(f"datetime オブジェクト: {date_object}")
                    print('-------------------------------------------')
                    time_diff = date_object - started_on[-1]
                    total_seconds = time_diff.total_seconds()
                    total_hours = total_seconds / 3600
                    hours = int(total_seconds // 3600)
                    remaining_seconds = total_seconds % 3600
                    minutes = int(remaining_seconds // 60)
                    print(f"datetime1: {started_on[-1]}")
                    print(f"datetime2: {date_object}")
                    print(f"所要時間: {hours}時間 {minutes}分")
                    message = {
                        "CONTRAST_URL": "http://18.176.117.9/Contrast/",
                        "HOURS": f"所要時間: {hours}時間 {minutes}分"
                    }
                    post_slack_message(message)
                    return
    
    except docker.errors.APIError as e:
        print(f"Error reading logs from container '{container.name}': {e}")

if __name__ == "__main__":
    print("Log monitor started.")
    monitor_logs()
    print("Log monitor finished.")

