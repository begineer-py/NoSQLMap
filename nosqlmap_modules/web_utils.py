"""
NoSQLMap Web工具模塊 - 包含Web相關功能
"""

import urllib.parse
import requests
from bs4 import BeautifulSoup
import warnings
import json
from i18n_utils import get_message
import urllib.request

# 抑制來自BeautifulSoup的警告
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

def parse_form(url, headers=None, verbose=False):
    """
    解析指定 URL 的 HTML 頁面中的表單
    
    Args:
        url (str): 表單所在頁面的 URL
        headers (dict): 請求頭
        verbose (bool): 是否顯示詳細信息
    
    Returns:
        tuple: (action_url, method, form_params)
            action_url: 表單提交的目標 URL
            method: 表單提交方法（GET/POST）
            form_params: 表單參數字典
    """
    if verbose:
        print(f"[*] 正在提取表單: {url}")
    
    try:
        # 嘗試不驗證 SSL 證書進行請求
        try:
            response = requests.get(url, headers=headers, verify=False, timeout=10)
            if response.status_code != 200:
                print(f"[!] 無法訪問頁面，狀態碼: {response.status_code}")
                return None, None, None
        except requests.exceptions.SSLError:
            print(f"[!] SSL 錯誤，嘗試不驗證 SSL 證書...")
            response = requests.get(url, headers=headers, verify=False, timeout=10)
            if response.status_code != 200:
                print(f"[!] 無法訪問頁面，狀態碼: {response.status_code}")
                return None, None, None
        except requests.exceptions.ConnectionError:
            print(f"[!] 連接錯誤，檢查 URL 是否正確: {url}")
            return None, None, None
        except Exception as e:
            print(f"[!] 請求頁面時發生錯誤: {e}")
            return None, None, None
            
        # 解析 HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 如果頁面內容非常小，可能是重定向或錯誤頁面
        if len(response.text) < 100:
            print(f"[!] 頁面內容過小，可能是重定向或錯誤頁面: {response.text}")
        
        forms = soup.find_all('form')
        
        if not forms:
            print("[!] 未找到表單")
            # 嘗試查找可能的登錄字段，即使沒有 <form> 標籤
            inputs = soup.find_all('input')
            if inputs:
                print(f"[*] 找到 {len(inputs)} 個輸入字段，但沒有 <form> 標籤")
                # 構建一個虛擬表單
                form_params = {}
                for input_field in inputs:
                    field_name = input_field.get('name')
                    if field_name:
                        field_value = input_field.get('value', '')
                        field_type = input_field.get('type', 'text').lower()
                        if field_type not in ['submit', 'button', 'image', 'reset', 'file']:
                            form_params[field_name] = field_value
                            print(f"[+] 找到輸入字段: {field_name}")
                
                if form_params:
                    print(f"[+] 從輸入字段構建虛擬表單: {form_params}")
                    # 使用當前 URL 作為提交目標
                    return url, "POST", form_params
            
            return None, None, None
        
        if len(forms) > 1:
            print(f"[*] 找到 {len(forms)} 個表單，使用第一個")
            if verbose:
                for i, form in enumerate(forms):
                    print(f"[*] 表單 {i+1} 信息:")
                    print(f"    方法: {form.get('method', 'GET')}")
                    print(f"    動作: {form.get('action', '')}")
                    print(f"    ID: {form.get('id', 'None')}")
                    print(f"    類: {form.get('class', 'None')}")
        
        # 使用第一個表單
        form = forms[0]
        
        # 獲取表單提交方法和目標 URL
        method = form.get('method', 'GET').upper()
        action = form.get('action', '')
        
        # 處理相對 URL
        if action.startswith('/'):
            # 從原始 URL 中提取基本 URL
            parsed_url = urllib.parse.urlparse(url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            action_url = base_url + action
        elif action.startswith('http'):
            action_url = action
        else:
            # 相對路徑，與當前 URL 路徑結合
            path = '/'.join(urllib.parse.urlparse(url).path.split('/')[:-1])
            if path and not path.endswith('/'):
                path += '/'
            action_url = urllib.parse.urljoin(url, path + action)
        
        # 如果 action 為空，使用當前 URL
        if not action:
            action_url = url
        
        # 提取表單參數
        form_params = {}
        for input_field in form.find_all(['input', 'select', 'textarea']):
            field_name = input_field.get('name')
            if not field_name:
                continue
                
            field_value = input_field.get('value', '')
            field_type = input_field.get('type', 'text').lower()
            
            # 排除 submit、button、image 類型的輸入框
            if field_type in ['submit', 'button', 'image', 'reset', 'file']:
                continue
                
            # 處理 select 元素
            if input_field.name == 'select':
                selected_option = input_field.find('option', selected=True)
                if selected_option:
                    field_value = selected_option.get('value', selected_option.text.strip())
                else:
                    options = input_field.find_all('option')
                    if options:
                        field_value = options[0].get('value', options[0].text.strip())
            
            form_params[field_name] = field_value
        
        if verbose:
            print(f"[+] 表單解析成功:")
            print(f"    提交方法: {method}")
            print(f"    提交 URL: {action_url}")
            print(f"    表單參數: {form_params}")
        
        if not form_params:
            print("[!] 表單中沒有找到有效參數")
            
        return action_url, method, form_params
        
    except Exception as e:
        print(f"[!] 解析表單時出錯: {e}")
        return None, None, None

def verify_site_availability(url, headers=None, timeout=10):
    """
    驗證目標站點是否可用
    
    Args:
        url (str): 目標 URL
        headers (dict): 請求頭
        timeout (int): 超時時間（秒）
        
    Returns:
        tuple: (是否可用, 響應內容長度, 響應時間)
    """
    try:
        import time
        start_time = time.time()
        
        # 嘗試不驗證 SSL 證書進行請求
        try:
            response = requests.get(url, headers=headers, verify=False, timeout=timeout)
        except requests.exceptions.SSLError:
            print(f"[!] SSL 錯誤，嘗試不驗證 SSL 證書...")
            response = requests.get(url, headers=headers, verify=False, timeout=timeout)
        
        end_time = time.time()
        response_time = round(end_time - start_time, 2)
        
        if response.status_code == 200:
            content_length = len(response.text)
            return True, content_length, response_time
        else:
            print(f"[!] 站點返回非200狀態碼: {response.status_code}")
            return False, 0, response_time
            
    except Exception as e:
        print(f"[!] 驗證站點可用性時出錯: {e}")
        return False, 0, 0

def parse_url(url):
    """
    解析 URL，提取協議、主機名、端口和路徑
    
    Args:
        url (str): 要解析的 URL
        
    Returns:
        tuple: (協議, 主機名, 端口, 路徑, 完整URL)
    """
    try:
        parsed = urllib.parse.urlparse(url)
        
        # 提取協議
        scheme = parsed.scheme or "http"
        
        # 提取主機名
        netloc = parsed.netloc
        
        # 如果netloc為空，可能是因為URL格式不完整
        if not netloc and parsed.path:
            # 嘗試從路徑中提取主機名
            parts = parsed.path.split("/", 1)
            netloc = parts[0]
            path = "/" + parts[1] if len(parts) > 1 else "/"
            print(f"[*] 警告: URL格式不完整，已從路徑提取主機名: {netloc}")
        else:
            path = parsed.path or "/"
        
        # 提取端口
        if ":" in netloc:
            host, port_str = netloc.split(":", 1)
            try:
                port = int(port_str)
            except ValueError:
                port = 443 if scheme == "https" else 80
        else:
            host = netloc
            port = 443 if scheme == "https" else 80
        
        # 確保主機名不包含協議
        if host.startswith("http:") or host.startswith("https:"):
            print(f"[!] 錯誤: 主機名包含協議，將被清理: {host}")
            # 移除協議部分
            host = host.split("//", 1)[1] if "//" in host else host
        
        # 添加查詢參數
        if parsed.query:
            path += "?" + parsed.query
        
        # 構建完整 URL
        full_url = f"{scheme}://{host}:{port}{path}"
        
        return scheme, host, port, path, full_url
    
    except Exception as e:
        print(f"[!] 解析 URL 時出錯: {e}")
        return "http", "", 80, "/", ""

def is_valid_url(url, base_domain=None):
    """
    判斷 URL 是否有效，並且如果指定了 base_domain，判斷 URL 是否屬於該域名
    
    Args:
        url (str): 要檢查的 URL
        base_domain (str, optional): 基礎域名
        
    Returns:
        bool: URL 是否有效
    """
    try:
        parsed = urllib.parse.urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            return False
            
        if base_domain and parsed.netloc != base_domain:
            # 檢查是否是子域名
            if not parsed.netloc.endswith("." + base_domain):
                return False
                
        return True
    except:
        return False

def get_response_body(url, headers=None, data=None, method="GET"):
    """
    獲取 URL 的響應內容
    
    Args:
        url (str): 目標 URL
        headers (dict): 請求頭
        data (dict): POST 數據
        method (str): 請求方法
        
    Returns:
        str: 響應內容
    """
    try:
        if method.upper() == "GET":
            req = urllib.request.Request(url, None, headers or {})
        else:
            if isinstance(data, dict):
                data = urllib.parse.urlencode(data).encode('utf-8')
            req = urllib.request.Request(url, data, headers or {})
            
        return getResponseBodyHandlingErrors(req)
    except Exception as e:
        print(f"[!] 獲取響應內容時出錯: {e}")
        return None

def getResponseBodyHandlingErrors(req):
    """
    處理 URL 請求並處理可能的錯誤
    
    Args:
        req: 請求對象
        
    Returns:
        str: 響應內容
    """
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        body = resp.read()
        return body
    except urllib.error.HTTPError as e:
        print(f"[!] HTTP 錯誤: {e.code} {e.reason}")
        return None
    except urllib.error.URLError as e:
        print(f"[!] URL 錯誤: {e.reason}")
        return None
    except Exception as e:
        print(f"[!] 請求時出錯: {e}")
        return None 