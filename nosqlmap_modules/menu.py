"""
NoSQLMap 菜單模塊 - 包含菜單和選項處理
"""

import json
import urllib.parse
from urllib.parse import urlparse
from i18n_utils import get_message
from . import config
from . import detect
from . import attack
from . import web_utils
import sys
def print_banner():
    """打印啟動橫幅"""
    print(get_message('STARTUP_BANNER'))

def main_menu():
    """
    顯示主菜單並處理用戶選擇
    
    Returns:
        bool: 如果用戶選擇退出則返回False，否則返回True
    """
    print_banner()
    
    # 直接使用自定義菜單，不使用get_message
    print("\n================================")
    print("        NoSQLMap 主菜單")
    print("================================")
    print(f"1. 設置目標主機      (當前: {config.victim})")
    print(f"2. 設置Web端口       (當前: {config.webPort})")
    print(f"3. 設置URI路徑        (當前: {config.uri})")
    print(f"4. 設置完整URL        (當前: {get_full_url()})")
    print("5. 設置HTTP認證")
    print(f"6. 設置HTTP方法      (當前: {config.httpMethod})")
    print(f"7. 設置本地IP        (當前: {config.myIP})")
    print(f"8. 設置Shell端口     (當前: {config.myPort})")
    print(f"9. 設置平台          (當前: {config.platform})")
    print(f"10. 設置數據庫端口   (當前: {config.dbPort})")
    print(f"11. 切換HTTPS        (當前: {config.https})")
    print(f"12. 更改語言         (當前: {config.language})")
    print("13. NoSQL數據庫攻擊")
    print("14. NoSQL Web應用攻擊")
    print("15. 掃描匿名訪問")
    print("16. 自動配置URL與目標主機")
    print("x. 退出")
    
    # 獲取用戶輸入
    try:
        select = input('> ')
    except KeyboardInterrupt:
        print("\n[!] 檢測到 CTRL+C，正在退出...")
        sys.exit(0)
    
    if select == "1":
        # 設置目標主機
        print("\n=== 獲取目標主機選項 ===")
        # 檢查是否已通過URL設置了主機
        if config.victim != "Not Set" and config.victim:
            print(f"[*] 當前目標主機: {config.victim}")
            change = input("要更改目標主機嗎? (y/n): ")
            if change.lower() != 'y':
                return True
                
        print("1-手動輸入")
        print("2-使用命令行工具獲取本機IP")
        print("3-掃描當前網絡中的主機")
        print("4-從文件讀取主機列表")
        host_select = input("> ")
        
        if host_select == "1":
            # 手動輸入
            victim = input(get_message('ENTER_HOST'))
            if victim == "":
                print(get_message('INVALID_HOSTNAME'))
            else:
                config.victim = victim
                print(f"[+] 目標主機設置為: {victim}")
        elif host_select == "2":
            # 使用命令行工具獲取本機IP
            try:
                import subprocess
                import platform
                import re
                
                print("[*] 正在獲取本機IP地址...")
                
                # 根據操作系統使用不同的命令
                if platform.system() == "Windows":
                    result = subprocess.run(['ipconfig'], capture_output=True, text=True)
                    if result.returncode == 0:
                        # 使用正則表達式從ipconfig輸出中提取IPv4地址
                        ipv4_pattern = r'IPv4.*?(\d+\.\d+\.\d+\.\d+)'
                        matches = re.findall(ipv4_pattern, result.stdout)
                        
                        if matches:
                            if len(matches) > 1:
                                print("[*] 檢測到多個IP地址：")
                                for i, ip in enumerate(matches, 1):
                                    print(f"{i}-{ip}")
                                ip_select = input("選擇要使用的IP (輸入編號): ")
                                try:
                                    ip_index = int(ip_select) - 1
                                    if 0 <= ip_index < len(matches):
                                        config.victim = matches[ip_index]
                                        print(f"[+] 目標主機設置為: {config.victim}")
                                    else:
                                        print("[!] 無效的選擇")
                                except ValueError:
                                    print("[!] 請輸入有效的數字")
                            else:
                                config.victim = matches[0]
                                print(f"[+] 目標主機設置為: {config.victim}")
                        else:
                            print("[!] 無法從ipconfig輸出中找到IPv4地址")
                    else:
                        print("[!] 執行ipconfig命令失敗")
                        print(f"錯誤信息: {result.stderr}")
                else:
                    # 非Windows系統使用hostname -I
                    result = subprocess.run(['hostname', '-I'], capture_output=True, text=True)
                    if result.returncode == 0:
                        # 獲取所有IP地址
                        ips = result.stdout.strip().split()
                        if ips:
                            if len(ips) > 1:
                                print("[*] 檢測到多個IP地址：")
                                for i, ip in enumerate(ips, 1):
                                    print(f"{i}-{ip}")
                                ip_select = input("選擇要使用的IP (輸入編號): ")
                                try:
                                    ip_index = int(ip_select) - 1
                                    if 0 <= ip_index < len(ips):
                                        config.victim = ips[ip_index]
                                        print(f"[+] 目標主機設置為: {config.victim}")
                                    else:
                                        print("[!] 無效的選擇")
                                except ValueError:
                                    print("[!] 請輸入有效的數字")
                            else:
                                config.victim = ips[0]
                                print(f"[+] 目標主機設置為: {config.victim}")
                        else:
                            print("[!] 無法獲取IP地址")
                    else:
                        print("[!] 執行命令失敗")
                        print(f"錯誤信息: {result.stderr}")
            except Exception as e:
                print(f"[!] 獲取主機信息時出錯: {str(e)}")
        elif host_select == "3":
            # 掃描當前網絡中的主機
            try:
                import subprocess
                import ipaddress
                import socket
                
                # 先獲取本機IP和網絡掩碼
                print("[*] 正在獲取本機網絡信息...")
                ip_result = subprocess.run(['hostname', '-I'], capture_output=True, text=True)
                if ip_result.returncode != 0:
                    print("[!] 無法獲取本機IP地址")
                    return True
                
                local_ip = ip_result.stdout.strip().split()[0]
                print(f"[*] 本機IP: {local_ip}")
                
                # 使用默認的24位掩碼
                network = f"{'.'.join(local_ip.split('.')[:3])}.0/24"
                print(f"[*] 假定網絡為: {network}")
                
                # 提醒用戶這個過程可能需要一些時間
                print("[*] 正在掃描網絡中的主機，這可能需要一些時間...")
                
                # 使用ping命令檢測存活主機
                print("[*] 使用ping命令檢測存活主機...")
                active_hosts = []
                
                # 只掃描網絡中的前20個IP (為了演示)
                network_obj = ipaddress.ip_network(network)
                hosts = list(network_obj.hosts())[:20]
                
                for host in hosts:
                    host_str = str(host)
                    # 不掃描自己
                    if host_str == local_ip:
                        continue
                    
                    print(f"\r[*] 正在ping {host_str}...", end="")
                    ping_result = subprocess.run(
                        ['ping', '-n', '1', '-w', '200', host_str], 
                        capture_output=True, 
                        text=True
                    )
                    
                    if ping_result.returncode == 0:
                        try:
                            hostname = socket.gethostbyaddr(host_str)[0]
                        except:
                            hostname = "未知"
                        
                        active_hosts.append((host_str, hostname))
                
                print("\r" + " " * 50 + "\r", end="")  # 清除當前行
                
                if active_hosts:
                    print("[+] 發現以下存活主機:")
                    for i, (ip, hostname) in enumerate(active_hosts, 1):
                        print(f"{i}-{ip} ({hostname})")
                    
                    host_select = input("選擇要設置為目標的主機 (輸入編號): ")
                    try:
                        host_index = int(host_select) - 1
                        if 0 <= host_index < len(active_hosts):
                            config.victim = active_hosts[host_index][0]
                            print(f"[+] 目標主機設置為: {config.victim}")
                        else:
                            print("[!] 無效的選擇")
                    except ValueError:
                        print("[!] 請輸入有效的數字")
                else:
                    print("[!] 未發現存活主機")
            except Exception as e:
                print(f"[!] 掃描網絡時出錯: {str(e)}")
        elif host_select == "4":
            # 從文件讀取主機列表
            try:
                filename = input("輸入包含主機列表的文件名: ")
                if not filename:
                    print("[!] 未提供文件名")
                    return True
                
                with open(filename, 'r') as f:
                    hosts = f.readlines()
                
                hosts = [h.strip() for h in hosts if h.strip()]
                
                if hosts:
                    print("[+] 從文件讀取以下主機:")
                    for i, host in enumerate(hosts, 1):
                        print(f"{i}-{host}")
                    
                    host_select = input("選擇要設置為目標的主機 (輸入編號): ")
                    try:
                        host_index = int(host_select) - 1
                        if 0 <= host_index < len(hosts):
                            config.victim = hosts[host_index]
                            print(f"[+] 目標主機設置為: {config.victim}")
                        else:
                            print("[!] 無效的選擇")
                    except ValueError:
                        print("[!] 請輸入有效的數字")
                else:
                    print("[!] 文件為空或不包含有效的主機")
            except FileNotFoundError:
                print(f"[!] 找不到文件: {filename}")
            except Exception as e:
                print(f"[!] 讀取文件時出錯: {str(e)}")
        else:
            print(get_message('INVALID_OPTION'))
        return True
    
    elif select == "2":
        # 設置Web端口
        try:
            webPort = input(get_message('ENTER_WEBPORT'))
            if webPort == "":
                print(get_message('INVALID_PORT'))
            else:
                config.webPort = int(webPort)
                print(f"[+] Web端口設置為: {webPort}")
        except ValueError:
            print(get_message('INVALID_PORT'))
        return True
    
    elif select == "3":
        # 設置URI路徑
        uri = input(get_message('ENTER_URI'))
        
        # 檢查是否輸入的是完整URL
        if uri.startswith('http://') or uri.startswith('https://'):
            print("[!] 檢測到輸入的是完整URL，將自動解析各部分")
            try:
                from . import web_utils
                scheme, host, port, path, full_url = web_utils.parse_url(uri)
                
                # 詢問用戶是否也要更新主機信息
                update_host = input(f"是否要將目標主機更新為 {host}? (y/n): ")
                if update_host.lower() == 'y':
                    config.victim = host
                    config.webPort = port
                    config.https = "ON" if scheme == "https" else "OFF"
                    print(f"[+] 目標主機已更新為: {host}")
                    print(f"[+] Web端口已更新為: {port}")
                    print(f"[+] HTTPS已設置為: {'開啟' if config.https == 'ON' else '關閉'}")
                
                # 始終更新URI路徑
                config.uri = path
                print(f"[+] URI路徑設置為: {path}")
                return True
            except Exception as e:
                print(f"[!] 解析URL時出錯: {str(e)}")
                print("[*] 將嘗試基本處理...")
        
        # 移除可能的協議前綴和主機部分
        if '://' in uri:
            # 先移除協議前綴
            uri = uri.split('://', 1)[1]
            # 再檢查是否包含主機部分
            if '/' in uri:
                # 分離主機和路徑部分
                host_part, path_part = uri.split('/', 1)
                
                # 詢問用戶是否要更新主機信息
                if host_part:
                    update_host = input(f"是否要將目標主機更新為 {host_part}? (y/n): ")
                    if update_host.lower() == 'y':
                        # 檢查主機部分是否包含端口
                        if ':' in host_part:
                            host, port_str = host_part.split(':', 1)
                            try:
                                port = int(port_str)
                                config.webPort = port
                                print(f"[+] Web端口已更新為: {port}")
                            except ValueError:
                                print("[!] 無法解析端口，使用默認端口")
                        else:
                            host = host_part
                        
                        config.victim = host
                        print(f"[+] 目標主機已更新為: {host}")
                
                # 設置路徑部分
                uri = '/' + path_part
            else:
                # 沒有路徑部分，可能只有主機
                if uri and uri != '/':
                    update_host = input(f"是否要將目標主機更新為 {uri}? (y/n): ")
                    if update_host.lower() == 'y':
                        config.victim = uri
                        print(f"[+] 目標主機已更新為: {uri}")
                uri = '/'
        
        # 確保URI以/開頭
        if uri != "" and not uri.startswith('/'):
            uri = '/' + uri
        config.uri = uri if uri != "" else "/"
        print(f"[+] URI路徑設置為: {config.uri}")
        return True
    
    elif select == "4":
        # 設置完整URL
        from . import web_utils
        url = input("請輸入完整URL (例如 http://example.com/app): ")
        if url == "":
            print(get_message('INVALID_HOSTNAME'))
            return True
        
        try:
            # 解析URL
            # 檢查URL是否包含協議前綴，如果沒有則添加
            if not url.startswith('http://') and not url.startswith('https://'):
                url = 'http://' + url
                print(f"[*] 已自動添加http://前綴: {url}")
                
            scheme, host, port, path, full_url = web_utils.parse_url(url)
            
            # 設置全局變量
            config.victim = host
            config.webPort = port
            config.uri = path
            config.https = "ON" if scheme == "https" else "OFF"
            
            print(f"[+] 目標URL已設置:")
            print(f"    主機: {host}")
            print(f"    端口: {port}")
            print(f"    路徑: {path}")
            print(f"    HTTPS: {config.https}")
            
            # 提示用戶主機已設置
            print(f"\n[+] 已自動設置目標主機為: {host}")
            
        except Exception as e:
            print(f"[!] 解析URL時出錯: {str(e)}")
        
        return True
    
    elif select == "5":
        # 設置HTTP認證
        print("\n=== HTTP認證設置 ===")
        http_auth_menu()
        return True
    
    elif select == "6":
        # 設置HTTP方法
        print("\n=== HTTP方法設置 ===")
        print(get_message('SELECT_HTTP_METHOD'))
        print(get_message('HTTP_GET_OPTION'))
        print(get_message('HTTP_POST_OPTION'))
        
        httpMethod = input("> ")
        if httpMethod == "1":
            config.httpMethod = "GET"
            print(get_message('GET_REQUEST_SET'))
        elif httpMethod == "2":
            config.httpMethod = "POST"
            print(get_message('POST_REQUEST_SET'))
            
            # 如果選擇了POST，詢問POST數據
            postData = input(get_message('ENTER_POST_DATA'))
            if postData != "":
                config.postData = postData
                
        else:
            print(get_message('INVALID_OPTION'))
        
        return True
    
    elif select == "7":
        # 設置本地IP
        if config.platform != "Not Set":
            prompt = f"請輸入用於{config.platform}/Shell的本地IP: "
        else:
            prompt = "請輸入用於Shell的本地IP: "
            
        myIP = input(prompt)
        if myIP == "":
            print(get_message('INVALID_HOSTNAME'))
        else:
            config.myIP = myIP
            print(f"[+] 本地IP設置為: {myIP}")
        return True
    
    elif select == "8":
        # 設置本地監聽端口
        myPort = input(get_message('ENTER_SHELL_PORT'))
        if myPort == "":
            print(get_message('INVALID_PORT'))
        else:
            try:
                config.myPort = int(myPort)
                print(get_message('SHELL_PORT_SET_TO').format(myPort=myPort))
            except ValueError:
                print(get_message('INVALID_PORT'))
        return True
    
    elif select == "9":
        # 設置NoSQL數據庫類型
        print("\n=== 平台設置 ===")
        set_platform_menu()
        return True
    
    elif select == "10":
        # 設置數據庫端口
        platform_port = input(get_message('ENTER_DB_PORT').format(platform=config.platform))
        if platform_port == "":
            print(get_message('INVALID_PORT'))
        else:
            try:
                config.dbPort = int(platform_port)
                print(get_message('DB_PORT_SET_TO').format(platform=config.platform, dbPort=platform_port))
            except ValueError:
                print(get_message('INVALID_PORT'))
        return True
    
    elif select == "11":
        # 切換HTTPS
        if config.https == "OFF":
            config.https = "ON"
            print("[+] HTTPS 已啟用")
        else:
            config.https = "OFF"
            print("[+] HTTPS 已禁用")
        return True
    
    elif select == "12":
        # 更改語言
        from i18n_utils import set_language
        
        print("\n=== 語言設置 ===")
        print(get_message('LANGUAGE_PROMPT'))
        print(get_message('LANGUAGE_PROMPT_1'))
        print(get_message('LANGUAGE_PROMPT_2'))
        lang_choice = input(get_message('LANGUAGE_PROMPT_3'))
        
        if lang_choice == "1":
            success = set_language('en')
            if success:
                print(get_message('LANGUAGE_SET').format(lang='English'))
        elif lang_choice == "2":
            success = set_language('zh')
            if success:
                print(get_message('LANGUAGE_SET').format(lang='中文'))
        else:
            print(get_message('INVALID_LANGUAGE'))
        
        return True
    
    elif select == "13":
        # NoSQL數據庫攻擊
        print("\n=== NoSQL數據庫攻擊 ===")
        # 檢查平台設置
        if config.platform == "Not Set":
            print("[!] 請先設置目標平台 (選項9)")
            return True
        
        # 根據不同平台調用不同的攻擊菜單
        if config.platform == "MongoDB":
            mongodb_menu()
        elif config.platform == "CouchDB":
            couchdb_menu()
        elif config.platform == "Redis":
            redis_menu()
        elif config.platform == "Neo4j":
            neo4j_menu()
        else:
            print(f"[!] 不支持的平台: {config.platform}")
        return True
    
    elif select == "14":
        # NoSQL Web應用攻擊
        print("\n=== NoSQL Web應用攻擊 ===")
        # 檢查必要設置
        if config.victim == "Not Set":
            print("[!] 請先設置目標主機 (選項1)")
            return True
        
        # 根據HTTP方法執行不同的攻擊
        if config.httpMethod == "GET":
            from . import attack
            attack.web_app_get_attack()
        elif config.httpMethod == "POST":
            from . import attack
            attack.web_app_post_attack()
        return True
    
    elif select == "15":
        # 掃描匿名訪問
        print("[*] 此功能尚未實現")
        return True
    
    elif select == "16":
        # 自動配置URL與目標主機
        print("\n=== 自動配置URL與目標主機 ===")
        
        if config.victim == "Not Set":
            print("[!] 未設置目標主機，無法自動配置")
            return True
        
        # 更新完整URL
        full_url = get_full_url()
        print(f"[+] 根據當前設置，完整URL為: {full_url}")
        
        # 詢問是否要測試URL連通性
        test_conn = input("是否要測試URL連通性? (y/n): ")
        if test_conn.lower() == 'y':
            try:
                import requests
                print(f"[*] 正在測試連接到 {full_url}...")
                response = requests.get(full_url, timeout=5)
                
                if response.status_code == 200:
                    print(f"[+] 連接成功! 響應狀態碼: {response.status_code}")
                    print(f"[+] 響應內容長度: {len(response.text)} 字節")
                    # 顯示部分響應內容
                    if len(response.text) > 0:
                        preview_length = min(200, len(response.text))
                        print(f"\n[+] 響應預覽 (前 {preview_length} 字節):")
                        print("-" * 50)
                        print(response.text[:preview_length] + ("..." if len(response.text) > preview_length else ""))
                        print("-" * 50)
                else:
                    print(f"[!] 收到狀態碼: {response.status_code}")
                    print(f"[!] 響應內容: {response.text[:100]}...")
            except Exception as e:
                print(f"[!] 連接測試失敗: {str(e)}")
        
        return True
    
    elif select.lower() == "q" or select.lower() == "x":
        return False
    
    else:
        print(get_message('INVALID_OPTION'))
        return True

def attack_menu():
    """
    顯示攻擊菜單並處理用戶選擇
    
    Returns:
        bool: 如果用戶選擇返回主菜單則返回False，否則返回True
    """
    # 顯示攻擊菜單
    print(get_message('ATTACK_MENU').format(
        config.victim,
        config.dbPort
    ))
    
    # 獲取用戶輸入
    select = input('> ')
    
    if select == "q":
        return False
    
    # 執行選擇的攻擊
    try:
        attack_option = int(select)
        attack.attack(attack_option)
    except ValueError:
        print(get_message('INVALID_ATTACK_SELECTION'))
    except Exception as e:
        print(f"[!] 執行攻擊時出錯: {str(e)}")
    
    input("\n" + get_message('RETURN_TO_MAIN'))
    return True

def mongodb_menu():
    """
    顯示MongoDB菜單並處理用戶選擇
    
    Returns:
        bool: 如果用戶選擇返回主菜單則返回False，否則返回True
    """
    # 顯示MongoDB菜單
    print(get_message('MONGODB_INJECTION_MENU').format(
        config.victim,
        config.dbPort
    ))
    
    # 獲取用戶輸入
    select = input('> ')
    
    if select == "q":
        return False
    
    # 執行選擇的操作
    try:
        mongodb_option = int(select)
        # 具體功能待實現
        print(f"[*] 選擇了MongoDB選項 {mongodb_option}，功能待實現")
    except ValueError:
        print(get_message('INVALID_ATTACK_SELECTION'))
    except Exception as e:
        print(f"[!] 執行MongoDB操作時出錯: {str(e)}")
    
    input("\n" + get_message('RETURN_TO_MAIN'))
    return True

def neo4j_menu():
    """
    顯示Neo4j菜單並處理用戶選擇
    
    Returns:
        bool: 如果用戶選擇返回主菜單則返回False，否則返回True
    """
    # 顯示Neo4j菜單
    print(get_message('NEOJ4_ATTACK_MENU').format(
        config.victim,
        config.dbPort
    ))
    
    # 獲取用戶輸入
    select = input('> ')
    
    if select == "q":
        return False
    
    # 執行選擇的操作
    try:
        neo4j_option = int(select)
        # 具體功能待實現
        print(f"[*] 選擇了Neo4j選項 {neo4j_option}，功能待實現")
    except ValueError:
        print(get_message('INVALID_ATTACK_SELECTION'))
    except Exception as e:
        print(f"[!] 執行Neo4j操作時出錯: {str(e)}")
    
    input("\n" + get_message('RETURN_TO_MAIN'))
    return True

def http_auth_menu():
    """
    顯示HTTP認證菜單並處理用戶選擇
    
    Returns:
        None
    """
    # 顯示HTTP認證菜單
    while True:
        print("\n=== HTTP認證設置 ===")
        print(f"1 - 設置用戶名     (當前: {config.httpUser})")
        print(f"2 - 設置密碼       (當前: {config.httpPass})")
        print(f"3 - 設置認證類型   (當前: {config.httpAuth})")
        print("0 - 返回主菜單")
        
        # 獲取用戶輸入
        select = input('> ')
        
        if select == "0":
            break
        
        elif select == "1":
            # 設置HTTP認證用戶名
            http_user = input("請輸入HTTP認證用戶名: ")
            config.httpUser = http_user
            print(f"[+] HTTP用戶名設置為: {http_user}")
        
        elif select == "2":
            # 設置HTTP認證密碼
            http_pass = input("請輸入HTTP認證密碼: ")
            config.httpPass = http_pass
            print(f"[+] HTTP密碼設置為: {http_pass}")
        
        elif select == "3":
            # 設置HTTP認證類型
            print("\n選擇HTTP認證類型:")
            print("1 - 基本認證 (Basic)")
            print("2 - 摘要認證 (Digest)")
            auth_type = input('> ')
            
            if auth_type == "1":
                config.httpAuth = "Basic"
                print("[+] 認證類型設置為: Basic")
            elif auth_type == "2":
                config.httpAuth = "Digest"
                print("[+] 認證類型設置為: Digest")
            else:
                print("[!] 無效的選擇")
        
        else:
            print("[!] 無效的選擇")

def set_platform_menu():
    """
    設置NoSQL數據庫平台類型菜單
    
    Returns:
        None
    """
    print("\n選擇NoSQL數據庫平台:")
    print("1 - MongoDB")
    print("2 - CouchDB")
    print("3 - Redis")
    print("4 - Neo4j")
    
    # 獲取用戶輸入
    select = input('> ')
    
    if select == "1":
        config.platform = "MongoDB"
        print("[+] 平台設置為 MongoDB")
    elif select == "2":
        config.platform = "CouchDB"
        print("[+] 平台設置為 CouchDB")
    elif select == "3":
        config.platform = "Redis"
        print("[+] 平台設置為 Redis")
    elif select == "4":
        config.platform = "Neo4j"
        print("[+] 平台設置為 Neo4j")
    else:
        print(get_message('INVALID_OPTION'))

def get_full_url():
    """
    基於當前配置構建完整URL
    
    Returns:
        str: 完整URL
    """
    if config.victim == "Not Set":
        return "Not Set"
    
    scheme = "https" if config.https == "ON" else "http"
    port = ""
    
    # 只有在非標準端口時才顯示端口
    if (scheme == "http" and config.webPort != 80) or (scheme == "https" and config.webPort != 443):
        port = f":{config.webPort}"
    
    url = f"{scheme}://{config.victim}{port}{config.uri}"
    return url

def redis_menu():
    """
    顯示Redis菜單並處理用戶選擇
    
    Returns:
        bool: 如果用戶選擇返回主菜單則返回False，否則返回True
    """
    # 顯示Redis菜單
    print("\n=== Redis攻擊選項 ===")
    print(f"目標主機: {config.victim}")
    print(f"端口: {config.dbPort}")
    print("\n1 - 獲取服務器信息")
    print("2 - 執行Redis命令")
    print("3 - 獲取數據庫鍵")
    print("4 - 轉儲數據")
    print("5 - 獲取Redis配置")
    print("6 - 檢查漏洞")
    print("q - 返回主菜單")
    
    # 獲取用戶輸入
    select = input('> ')
    
    if select.lower() == "q":
        return False
    
    # 執行選擇的操作
    try:
        redis_option = int(select)
        # 具體功能待實現
        print(f"[*] 選擇了Redis選項 {redis_option}，功能待實現")
    except ValueError:
        print(f"[!] 無效的選擇: {select}")
    except Exception as e:
        print(f"[!] 執行Redis操作時出錯: {str(e)}")
    
    input("\n按Enter返回...")
    return True

def couchdb_menu():
    """
    顯示CouchDB菜單並處理用戶選擇
    
    Returns:
        bool: 如果用戶選擇返回主菜單則返回False，否則返回True
    """
    # 顯示CouchDB菜單
    print("\n=== CouchDB攻擊選項 ===")
    print(f"目標主機: {config.victim}")
    print(f"端口: {config.dbPort}")
    print("\n1 - 獲取服務器信息")
    print("2 - 列出數據庫")
    print("3 - 獲取數據庫詳情")
    print("4 - 檢查管理員權限")
    print("5 - 創建用戶")
    print("6 - 獲取所有用戶")
    print("7 - 檢查漏洞")
    print("q - 返回主菜單")
    
    # 獲取用戶輸入
    select = input('> ')
    
    if select.lower() == "q":
        return False
    
    # 執行選擇的操作
    try:
        couchdb_option = int(select)
        # 具體功能待實現
        print(f"[*] 選擇了CouchDB選項 {couchdb_option}，功能待實現")
    except ValueError:
        print(f"[!] 無效的選擇: {select}")
    except Exception as e:
        print(f"[!] 執行CouchDB操作時出錯: {str(e)}")
    
    input("\n按Enter返回...")
    return True 