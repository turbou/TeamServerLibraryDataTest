import docker
import os
import sys
import requests
import json
import time
import re
from datetime import datetime

def monitor_folder():
    client = docker.from_env()
    try:
        container = client.containers.get('contrast.teamserver')
        command = "ls -1 /opt/contrast/data/libraries" 
        exit_code, output = container.exec_run(cmd=command)
        if exit_code == 0:
            file_list = output.decode('utf-8').strip().split('\n')
            file_list = [f for f in file_list if f and f not in ('.', '..')]
            print(file_list)
        else:
            print(f"エラー: コンテナ内でコマンドの実行に失敗しました。終了コード: {exit_code}")
            print(f"エラー出力:\n{output.decode('utf-8')}")
    except docker.errors.APIError as e:
        print(f"Error reading logs from container '{container.name}': {e}")

if __name__ == "__main__":
    print("Folder monitor started.")
    monitor_folder()
    print("Folder monitor finished.")

