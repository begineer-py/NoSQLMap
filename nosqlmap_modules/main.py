"""
NoSQLMap 主程序模塊 - 程序入口
"""

import sys
import signal
import argparse
import os
from i18n_utils import get_message, set_language
from . import config
from . import detect
from . import menu
from . import attack
from . import web_utils

# 嘗試導入載荷模組
try:
    import payloads
    PAYLOADS_AVAILABLE = True
except ImportError:
    PAYLOADS_AVAILABLE = False

def signal_handler(signal, frame):
    """
    處理CTRL+C終止信號
    """
    print("\n[!] 檢測到 CTRL+C，正在退出...")
    sys.exit(0)

def build_parser():
    """
    構建命令行參數解析器
    
    Returns:
        argparse.ArgumentParser: 參數解析器對象
    """
    parser = argparse.ArgumentParser(
        description=get_message('TOOL_DESC'),
        epilog=get_message('USAGE_EXAMPLES'),
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument('url', nargs='?', help=get_message('URL_HELP'))
    parser.add_argument('--myIP', help=get_message('MYIP_HELP'))
    parser.add_argument('--form', '-f', action='store_true', 
                         help=get_message('FORM_HELP'))

    # 語言選項
    lang_group = parser.add_mutually_exclusive_group()
    lang_group.add_argument('--language', choices=['en', 'zh'], 
                           help=get_message('LANGUAGE_HELP'))
    lang_group.add_argument('-zh', '--chinese', action='store_true', 
                           help=get_message('CHINESE_HELP'))
    lang_group.add_argument('-en', '--english', action='store_true', 
                           help=get_message('ENGLISH_HELP'))

    # 高級選項
    advanced = parser.add_argument_group(get_message('ADVANCED_OPTIONS'))
    advanced.add_argument('--victim', '-v', help=get_message('VICTIM_HELP'))
    if PAYLOADS_AVAILABLE:
        platform_choices = ['MongoDB', 'Neo4j', 'CouchDB', 'Redis']
    else:
        platform_choices = ['MongoDB', 'Neo4j', 'CouchDB']
    advanced.add_argument('--platform', choices=platform_choices, help=get_message('PLATFORM_HELP'))
    advanced.add_argument('--dbPort', '-dp', type=int, help=get_message('DBPORT_HELP'))
    advanced.add_argument('--webPort', '-wp', type=int, help=get_message('WEBPORT_HELP'))
    advanced.add_argument('--uri', '-u', help=get_message('URI_HELP'))
    advanced.add_argument('--httpMethod', '-m', choices=['GET', 'POST'], 
                           help=get_message('METHOD_HELP'))
    # 爬蟲選項
    advanced.add_argument('--crawl', '-c', type=int, dest='depth', 
                           help=get_message('CRAWL_HELP'))

    # 載荷選項，僅當payloads可用時顯示
    if PAYLOADS_AVAILABLE:
        payload_group = parser.add_argument_group('Payload Options')
        payload_group.add_argument('--list-payloads', action='store_true', 
                                help='列出所有可用的注入載荷')
        payload_group.add_argument('--show-payload', 
                                help='顯示特定載荷的詳細信息，格式為平台:類別:名稱')

    return parser

def main(args=None):
    """
    主程序函數
    
    Args:
        args (argparse.Namespace, optional): 命令行參數
        
    Returns:
        None
    """
    # 註冊信號處理，使程序能夠在CTRL+C時優雅退出
    signal.signal(signal.SIGINT, signal_handler)
    
    # 如果無參數，直接進入交互模式
    if args is None:
        # 初始化配置
        config.init_config()
        # 啟動主菜單
        while menu.main_menu():
            pass
        return
    
    # 調試模式開關
    DEBUG = False
    
    # 處理語言設置
    if args.chinese:
        set_language('zh')
        config.language = 'zh'
        if DEBUG:
            print(f"[DEBUG] 語言設置為: {config.language}")
    elif args.english:
        set_language('en')
        config.language = 'en'
        if DEBUG:
            print(f"[DEBUG] 語言設置為: {config.language}")
    elif args.language:
        set_language(args.language)
        config.language = args.language
        if DEBUG:
            print(f"[DEBUG] 語言設置為: {config.language}")
    else:
        # 如果沒有指定語言，使用默認語言
        set_language(config.language)
        if DEBUG:
            print(f"[DEBUG] 使用默認語言: {config.language}")
    
    # 初始化配置
    config.init_config()
    # 保留語言設置
    lang = config.language
    # 更新配置後恢復語言設置
    config.language = lang
    
    # 處理載荷相關參數
    if PAYLOADS_AVAILABLE:
        if hasattr(args, 'list_payloads') and args.list_payloads:
            list_available_payloads()
            return
        
        if hasattr(args, 'show_payload') and args.show_payload:
            show_payload_details(args.show_payload)
            return
    
    # 處理URL參數
    if args.url:
        # 解析URL
        scheme, host, port, path, full_url = web_utils.parse_url(args.url)
        
        # 設置全局變量
        config.victim = host
        config.webPort = port
        config.uri = path
        config.https = "ON" if scheme == "https" else "OFF"
        
        print(f"[+] 目標URL已設置:")
        print(f"    主機: {host}")
        print(f"    端口: {port}")
        if path != "/":
            print(f"    URI路徑: {path}")
        print(f"    HTTPS: {'是' if scheme == 'https' else '否'}")
        
        print(f"\n[+] 已自動設置目標主機為: {host}")
    
    # 處理其他參數
    if args.victim:
        config.victim = args.victim
        print(f"[+] 目標主機: {args.victim}")
    
    if args.platform:
        config.platform = args.platform
        print(f"[+] 平台類型: {args.platform}")
    
    if args.dbPort:
        config.dbPort = args.dbPort
        print(f"[+] 數據庫端口: {args.dbPort}")
    
    if args.webPort:
        config.webPort = args.webPort
        print(f"[+] Web 端口: {args.webPort}")
    
    if args.uri:
        # 確保 URI 以 / 開頭
        if not args.uri.startswith('/'):
            config.uri = '/' + args.uri
        else:
            config.uri = args.uri
        print(f"[+] URI 路徑: {args.uri}")
    
    if args.httpMethod:
        config.httpMethod = args.httpMethod
        print(f"[+] HTTP 方法: {args.httpMethod}")
    
    if args.myIP:
        config.myIP = args.myIP
        print(f"[+] 本地 IP: {args.myIP}")
    
    # 如果指定了表單參數
    if args.form and config.victim != "Not Set":
        # 構建完整 URL
        scheme = "https" if config.https == "ON" else "http"
        port = f":{config.webPort}" if (config.https == "ON" and config.webPort != 443) or (config.https == "OFF" and config.webPort != 80) else ""
        url = f"{scheme}://{config.victim}{port}{config.uri}"
        
        # 解析表單並設置參數
        success, message = attack.process_form_attack(url)
        
        if not success:
            print(f"[!] {message}")
            sys.exit(1)
    
    # 如果有URL，嘗試檢測平台
    if (args.url or args.victim) and config.platform == "Not Set":
        print("\n[*] 嘗試檢測平台類型...")
        detected_platform, detected_port = detect.detect_platform(config.victim)
        
        if detected_platform:
            config.platform = detected_platform
            if not args.dbPort:  # 如果沒有指定dbPort，使用檢測到的端口
                config.dbPort = detected_port
            print(f"[+] 在端口 {detected_port} 檢測到平台: {detected_platform}")
    
    # 如果指定了爬蟲深度
    if args.depth and args.depth > 0:
        # 構建完整 URL
        scheme = "https" if config.https == "ON" else "http"
        port = f":{config.webPort}" if (config.https == "ON" and config.webPort != 443) or (config.https == "OFF" and config.webPort != 80) else ""
        url = f"{scheme}://{config.victim}{port}{config.uri}"
        
        print(f"[*] 開始以深度 {args.depth} 爬取 {url}...")
        # TODO: 實現爬蟲功能
        print("[!] 爬蟲功能尚未實現")
    
    # 啟動主菜單
    while menu.main_menu():
        pass

def list_available_payloads():
    """
    列出所有可用的注入載荷
    """
    if not PAYLOADS_AVAILABLE:
        print("[!] 載荷模組不可用")
        return
    
    print("\n=== 可用的注入載荷 ===")
    
    # 遍歷所有支持的平台
    platforms = ["mongodb", "neo4j", "redis", "couchdb"]
    found_payloads = False
    
    for platform in platforms:
        platform_payloads = payloads.get_platform_payloads(platform)
        if not platform_payloads:
            continue
            
        found_payloads = True
        print(f"\n## {platform.upper()} 載荷")
        
        # 列出該平台的所有類別
        for category, module in platform_payloads.items():
            print(f"\n### {category}")
            
            # 獲取該類別中的所有載荷列表
            payload_lists = [attr for attr in dir(module) if attr.endswith('_PAYLOADS') and attr.isupper()]
            
            if not payload_lists:
                print("  - 無可用載荷")
                continue
                
            # 列出該類別中的所有載荷列表
            for payload_list in payload_lists:
                try:
                    payloads_data = getattr(module, payload_list)
                    count = len(payloads_data) if isinstance(payloads_data, list) else "N/A"
                    print(f"  - {payload_list} ({count} 個載荷)")
                except Exception as e:
                    print(f"  - {payload_list} (錯誤: {str(e)})")
    
    if not found_payloads:
        print("[!] 未找到任何載荷")

def show_payload_details(payload_spec):
    """
    顯示特定載荷的詳細信息
    
    Args:
        payload_spec (str): 載荷規格，格式為平台:類別:名稱
    """
    if not PAYLOADS_AVAILABLE:
        print("[!] 載荷模組不可用")
        return
    
    # 解析載荷規格
    try:
        parts = payload_spec.split(':')
        if len(parts) != 3:
            print("[!] 無效的載荷規格，格式應為：平台:類別:名稱")
            print("    例如: mongodb:auth_bypass:AUTH_BYPASS_PAYLOADS")
            return
            
        platform, category, payload_name = parts
        
        # 獲取平台載荷
        platform_payloads = payloads.get_platform_payloads(platform)
        if not platform_payloads:
            print(f"[!] 平台 '{platform}' 的載荷不可用")
            return
            
        # 獲取類別模塊
        if category not in platform_payloads:
            print(f"[!] 平台 '{platform}' 中找不到類別 '{category}'")
            print(f"    可用類別: {', '.join(platform_payloads.keys())}")
            return
            
        module = platform_payloads[category]
        
        # 獲取載荷列表
        if not hasattr(module, payload_name):
            print(f"[!] 在 '{platform}/{category}' 中找不到載荷 '{payload_name}'")
            payload_lists = [attr for attr in dir(module) if attr.endswith('_PAYLOADS') and attr.isupper()]
            if payload_lists:
                print(f"    可用載荷: {', '.join(payload_lists)}")
            else:
                print(f"    該類別中沒有可用的載荷")
            return
            
        payloads_data = getattr(module, payload_name)
        
        # 顯示載荷詳情
        print(f"\n=== {platform.upper()} {category} {payload_name} ===\n")
        
        if isinstance(payloads_data, list):
            print(f"共 {len(payloads_data)} 個載荷:\n")
            for i, payload in enumerate(payloads_data):
                print(f"{i+1}. {repr(payload)}")
        elif isinstance(payloads_data, dict):
            print(f"共 {len(payloads_data)} 個載荷:\n")
            for key, value in payloads_data.items():
                print(f"- {key}: {repr(value)}")
        else:
            print(f"載荷值: {repr(payloads_data)}")
            
    except Exception as e:
        print(f"[!] 顯示載荷時出錯: {str(e)}")

if __name__ == "__main__":
    args = build_parser().parse_args()
    main(args)

# 確保函數可以被導入
__all__ = ['build_parser', 'main'] 