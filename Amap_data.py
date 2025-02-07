import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import os
import time
from datetime import datetime
import requests
import csv
import pandas as pd
import json
import re

from utils.read_write import writeOneJson
from utils.time_change import getBetweenDay

# 设置工作目录存放爬取到的json文件和CSV文件
base_dir = r'D:\code\GDlink'
json_output_dir = os.path.join(base_dir, 'jsonout')
csv_output_dir = os.path.join(base_dir, 'city_csv')

os.makedirs(json_output_dir, exist_ok=True)  # 创建JSON文件目录
os.makedirs(csv_output_dir, exist_ok=True)  # 创建CSV文件目录

# HTTP 请求头
headers = {
    "User-agent": (
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0"
    )
}

# 从 citylist.csv 文件中读取 citycode 列
def get_city_list_from_csv(file_path):
    city_list = []
    if os.path.exists(file_path):
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if 'citycode' in row:
                    try:
                        city_list.append(int(row['citycode']))
                    except ValueError:
                        print(f"Invalid citycode value: {row['citycode']}")
    else:
        print(f"City list file not found: {file_path}")
    return city_list

# 发送请求并处理响应，增加重试机制
def requests_url_with_retry(url, city, riqi, max_retries=3, retry_delay=5):
    attempt = 0
    while attempt < max_retries:
        try:
            response = requests.get(url, timeout=1000, headers=headers, verify=False)  # 关闭 SSL 验证
            response.raise_for_status()  # 检查 HTTP 状态码
            data = response.json()  # 更安全的 JSON 解析方式
            file_name = os.path.join(json_output_dir, f"{city}_{riqi}.json")
            writeOneJson(data, file_name)  # 写入 JSON 文件
            return True  # 请求成功
        except requests.exceptions.RequestException:
            attempt += 1
            time.sleep(retry_delay)
    return False  # 超过最大重试次数后返回失败

# 城市范围下载
def city_range(city, date_list, failed_tasks):
    for riqi in date_list:
        file_name = os.path.join(json_output_dir, f"{city}_{riqi}.json")
        if not os.path.exists(file_name):
            url = (
                f"https://trp.autonavi.com/cityTravel/inAndOutCity.do?"
                f"adcode={city}&dt={riqi}&willReal=WILL&inOut=OUT&size=200"
            )
            success = requests_url_with_retry(url, city, riqi)
            if not success:
                failed_tasks.append((city, riqi))  # 记录失败任务

# 合并城市数据为 CSV 文件
def merge_city_json_to_csv(city, date_list):
    json_files = [
        os.path.join(json_output_dir, f"{city}_{riqi}.json") for riqi in date_list
        if os.path.exists(os.path.join(json_output_dir, f"{city}_{riqi}.json"))
    ]

    city_data = []

    for json_file in json_files:
        with open(json_file, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                df = pd.json_normalize(data)
            except (json.JSONDecodeError, Exception):
                continue

        match = re.match(rf"{city}_(\d{{4}}-\d{{2}}-\d{{2}})\.json", os.path.basename(json_file))
        if match:
            date = match.group(1)
            df['date'] = date
            city_data.append(df)

    if city_data:
        combined_df = pd.concat(city_data, ignore_index=True)
        combined_df['city_code'] = city
        combined_df = combined_df[['date', 'city_code'] + [col for col in combined_df.columns if col not in ['date', 'city_code']]]
        csv_file = os.path.join(csv_output_dir, f"{city}.csv")
        combined_df.to_csv(csv_file, index=False, encoding='utf-8-sig')
        print(f"城市 {city} 的数据已保存到 {csv_file}")

# 日期变化处理
def process_cities(city_list, start_date):
    failed_tasks = []  # 用于记录失败的任务
    date_list = getBetweenDay(start_date)  # 获取日期范围列表

    for city in city_list:
        print(f"开始爬取城市 {city} 的数据...")
        city_range(city, date_list, failed_tasks)
        merge_city_json_to_csv(city, date_list)
        print(f"完成城市 {city} 的数据爬取并生成 CSV 文件。")

    # 处理失败的任务
    if failed_tasks:
        print(f"共有 {len(failed_tasks)} 个任务失败，开始重试...")
        for city, riqi in failed_tasks:
            city_range(city, [riqi], failed_tasks)
        print("失败任务处理完成。")

# 主程序入口
if __name__ == '__main__':
    citylist_file = os.path.join(base_dir, 'citylist.csv')

    city_list = get_city_list_from_csv(citylist_file)

    if not city_list:
        print("City list is empty or file is not formatted correctly.")
    else:
        print(f"City list loaded: {city_list}")

    process_cities(city_list, '2024-01-01')

