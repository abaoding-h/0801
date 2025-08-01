import time
import pandas as pd
import os
import re#正则
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup  # 新增的模块

# 时间关键词，正则表达式
time_prefix_pattern = re.compile(
    r"^(August|October|November|December|January|February|March|April|May|June|July|September|"
    r"Early|Late|Spring|Summer|Fall|Winter|Ongoing|End of|Beginning of)[^\n]{0,30}\d{4}",
    re.IGNORECASE
)

def init_driver():
    options = Options()
    options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    options.add_argument("--lang=en-US")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("prefs", {"intl.accept_languages": "en-US,en"})

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def search_and_extract(driver, sysname):
    query = f"Summarize {sysname} AI adoption timeline"
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}&hl=en&gl=us"
    driver.get(search_url)

    #等待页面加载
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//ul[@class='U6u95']"))
        )
    except:
        return query, []  #无数据返回

    # 获取HTML源码
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    li_items = soup.select("ul.U6u95 li")

    # 筛选出以时间开头的 <li> 项
    summary_list = []
    for li in li_items:
        text = li.get_text(strip=True)
        if time_prefix_pattern.match(text):
            summary_list.append(text)

    return query, summary_list

def main():
    input_file = "aha_hosp_w_ai.xlsx"
    output_file = "google_ai_timeline_split.xlsx"
    output_path = os.path.join(os.getcwd(), output_file)

    if not os.path.exists(input_file):
        print(f" 输入文件 {input_file} 不存在，需将文件放在脚本同目录下")
        return

    df = pd.read_excel(input_file)
    sysnames = df['sysname'].dropna().drop_duplicates().reset_index(drop=True)

    driver = init_driver()
    print("\n 浏览器已开，手动登录 Google 账号以确保AO 内容可见")
    input(" 登录完成后请按回车继续...\n")

    all_rows = []

    for idx, sysname in enumerate(sysnames):
        print(f" 搜索中 ({idx+1}/{len(sysnames)}): {sysname} ...")
        query, summary_list = search_and_extract(driver, sysname)

        for s in summary_list:
            all_rows.append({
                "sysname": sysname,
                "query": query,
                "summary": s
            })

        # 实时保存防止中断
        pd.DataFrame(all_rows).to_excel(output_path, index=False)
        time.sleep(2)

    driver.quit()
    print(f"\n 抓取完成，结果已保存为：{output_path}")

if __name__ == "__main__":
    main()
