"""
NoSQLMap 主程序模塊 - 程序入口
"""

import sys
import signal
import argparse
from i18n_utils import get_message, set_language
from . import config
from . import detect
from . import menu
from . import attack
from . import web_utils

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
    advanced.add_argument('--platform', choices=['MongoDB', 'Neo4j', 'CouchDB'], help=get_message('PLATFORM_HELP'))
    advanced.add_argument('--dbPort', '-dp', type=int, help=get_message('DBPORT_HELP'))
    advanced.add_argument('--webPort', '-wp', type=int, help=get_message('WEBPORT_HELP'))
    advanced.add_argument('--uri', '-u', help=get_message('URI_HELP'))
    advanced.add_argument('--httpMethod', '-m', choices=['GET', 'POST'], 
                           help=get_message('METHOD_HELP'))
    # 爬蟲選項
    advanced.add_argument('--crawl', '-c', type=int, dest='depth', 
                           help=get_message('CRAWL_HELP'))

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
        start_url = f"{scheme}://{config.victim}{port}"
        
        if config.uri != "Not Set":
            start_url += config.uri
        
        from . import crawl
        crawl.crawl(start_url, args.depth)
    
    # 直接進入交互模式，無論是否提供了參數
    # 啟動主菜單
    while menu.main_menu():
        pass

# 確保函數可以被導入
__all__ = ['build_parser', 'main'] 