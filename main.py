import requests
import pandas as pd
import datetime
import os
from time import sleep

# 配置参数
UID = "381875112"  # 摩尔线程B站UID（在官网URL中找到）
EXCEL_PATH = "bilibili_fans.xlsx"

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
            print(f"API错误: {data['message']}")
            return None
    except Exception as e:
        print(f"请求失败: {str(e)}")
        return None

def save_to_excel(fans_count, file_path):
    """保存数据到Excel（自动创建文件或追加数据）"""
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_data = pd.DataFrame({
        "日期": [current_time.split()[0]],
        "时间": [current_time.split()[1]],
        "粉丝数": [fans_count]
    })
    
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        df = pd.concat([df, new_data], ignore_index=True)
    else:
        df = new_data
    
    df.to_excel(file_path, index=False)
    print(f"数据已保存到 {file_path}")

if __name__ == "__main__":
    fans = get_bili_fans(UID)
    if fans is not None:
        print(f"当前粉丝数: {fans}")
        save_to_excel(fans, EXCEL_PATH)
    else:
        print("未获取到有效数据")