"""
NoSQLMap 爬蟲模塊 - 包含網站爬取功能
"""

import re
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import warnings
from . import web_utils

# 抑制來自BeautifulSoup的警告
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

def crawl(start_url, max_depth=2):
    """
    爬取目標網站，獲取所有鏈接
    
    Args:
        start_url (str): 起始URL
        max_depth (int): 最大爬取深度
        
    Returns:
        list: 爬取到的URL列表
    """
    print(f"[*] 開始爬取網站: {start_url}")
    
    # 解析起始URL獲取主域名
    parsed_url = urlparse(start_url)
    base_domain = parsed_url.netloc
    
    # 存儲已訪問的URL
    visited_urls = set()
    # 存儲要訪問的URL和其深度
    url_queue = [(start_url, 0)]
    # 存儲爬取到的所有URL
    all_urls = []
    
    while url_queue:
        current_url, depth = url_queue.pop(0)
        
        # 如果超過最大深度或URL已訪問，則跳過
        if depth > max_depth or current_url in visited_urls:
            continue
            
        # 標記URL為已訪問
        visited_urls.add(current_url)
        
        # 嘗試請求URL
        try:
            print(f"[*] 爬取 (深度 {depth}): {current_url}")
            
            # 檢查URL是否有效
            if not web_utils.is_valid_url(current_url, base_domain):
                print(f"[!] 跳過非法或外部URL: {current_url}")
                continue
                
            # 請求URL
            response = requests.get(current_url, verify=False, timeout=10)
            
            if response.status_code != 200:
                print(f"[!] 請求失敗 ({response.status_code}): {current_url}")
                continue
                
            # 將當前URL添加到結果列表
            all_urls.append(current_url)
            
            # 如果已達到最大深度，不再繼續爬取
            if depth == max_depth:
                continue
                
            # 解析響應內容
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 提取所有鏈接
            links = soup.find_all('a')
            for link in links:
                href = link.get('href')
                
                if not href:
                    continue
                    
                # 將相對路徑轉為絕對路徑
                absolute_url = urljoin(current_url, href)
                
                # 解析 URL
                parsed_link = urlparse(absolute_url)
                
                # 排除錨點、JavaScript和郵件鏈接
                if parsed_link.scheme in ['http', 'https'] and parsed_link.netloc == base_domain:
                    # 移除錨點
                    clean_url = absolute_url.split('#')[0]
                    
                    # 如果URL未訪問過，則添加到隊列
                    if clean_url not in visited_urls:
                        url_queue.append((clean_url, depth + 1))
                        
        except requests.exceptions.RequestException as e:
            print(f"[!] 請求錯誤: {e}")
            continue
        except Exception as e:
            print(f"[!] 爬取時出錯: {e}")
            continue
    
    # 過濾重複URL
    unique_urls = list(set(all_urls))
    
    print(f"[+] 爬取完成，共找到 {len(unique_urls)} 個唯一URL")
    for url in unique_urls:
        print(f"    - {url}")
        
    return unique_urls

def crawl_for_forms(start_url, max_depth=1):
    """
    爬取網站並尋找包含表單的頁面
    
    Args:
        start_url (str): 起始URL
        max_depth (int): 最大爬取深度
        
    Returns:
        list: 包含表單的URL列表
    """
    print(f"[*] 開始爬取網站尋找表單: {start_url}")
    
    # 爬取網站
    urls = crawl(start_url, max_depth)
    
    # 存儲包含表單的URL
    form_urls = []
    
    # 檢查每個URL是否包含表單
    for url in urls:
        try:
            print(f"[*] 檢查是否包含表單: {url}")
            
            # 請求URL
            response = requests.get(url, verify=False, timeout=10)
            
            if response.status_code != 200:
                print(f"[!] 請求失敗 ({response.status_code}): {url}")
                continue
                
            # 解析響應內容
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 檢查是否包含表單
            forms = soup.find_all('form')
            
            if forms:
                print(f"[+] 找到 {len(forms)} 個表單: {url}")
                form_urls.append(url)
            else:
                print(f"[-] 未找到表單: {url}")
                
        except Exception as e:
            print(f"[!] 檢查表單時出錯: {e}")
            continue
    
    print(f"[+] 爬取完成，共找到 {len(form_urls)} 個包含表單的URL")
    for url in form_urls:
        print(f"    - {url}")
        
    return form_urls

def is_same_domain(url1, url2):
    """
    檢查兩個URL是否屬於同一域名
    
    Args:
        url1 (str): 第一個URL
        url2 (str): 第二個URL
        
    Returns:
        bool: 是否屬於同一域名
    """
    parsed1 = urlparse(url1)
    parsed2 = urlparse(url2)
    
    return parsed1.netloc == parsed2.netloc 