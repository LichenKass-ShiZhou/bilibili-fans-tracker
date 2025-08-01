import requests
import pandas as pd
import datetime
import os
from time import sleep

# 配置参数
UID_MOORE = "381875112"         # 摩尔线程B站UID
UID_LISUAN = "3546938628638822"  # 砺算科技B站UID
EXCEL_PATH = "bilibili_fans_data.xlsx"

def get_bili_fans(uid):
    """通过B站API获取粉丝数"""
    url = f"https://api.bilibili.com/x/relation/stat?vmid={uid}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Referer": "https://space.bilibili.com/"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        if data["code"] == 0:
            return data["data"]["follower"]
        else:
            print(f"API错误 (UID:{uid}): {data['message']}")
            return None
    except Exception as e:
        print(f"请求失败 (UID:{uid}): {str(e)}")
        return None

def save_to_excel(moore_fans, lisuan_fans, file_path):
    """保存数据到Excel，两个账号的粉丝数在同一行"""
    current_time = datetime.datetime.now()
    date_str = current_time.strftime("%Y-%m-%d")
    time_str = current_time.strftime("%H:%M:%S")
    
    # 创建新数据行
    new_data = {
        "日期": date_str,
        "时间": time_str,
        "摩尔线程粉丝数": moore_fans,
        "砺算科技粉丝数": lisuan_fans
    }
    
    # 创建DataFrame
    new_df = pd.DataFrame([new_data])
    
    # 处理Excel文件
    if os.path.exists(file_path):
        # 读取现有文件
        df = pd.read_excel(file_path)
        # 追加新数据
        df = pd.concat([df, new_df], ignore_index=True)
    else:
        df = new_df
    
    # 保存到Excel
    df.to_excel(file_path, index=False)
    print(f"数据已保存到 {file_path}")

if __name__ == "__main__":
    # 获取摩尔线程粉丝数
    moore_fans = get_bili_fans(UID_MOORE)
    if moore_fans is not None:
        print(f"摩尔线程当前粉丝数: {moore_fans}")
    else:
        print("摩尔线程未获取到有效数据")
        moore_fans = ""  # 设置为空字符串以便保存
    
    # 添加延迟
    sleep(1)
    
    # 获取砺算科技粉丝数
    lisuan_fans = get_bili_fans(UID_LISUAN)
    if lisuan_fans is not None:
        print(f"砺算科技当前粉丝数: {lisuan_fans}")
    else:
        print("砺算科技未获取到有效数据")
        lisuan_fans = ""  # 设置为空字符串以便保存
    
    # 保存到Excel
    save_to_excel(moore_fans, lisuan_fans, EXCEL_PATH)
