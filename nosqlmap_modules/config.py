"""
NoSQLMap 配置模塊 - 保存全局配置變量
"""

# 全局變量
victim = "Not Set"     # 目標主機
webPort = 80           # Web 端口
dbPort = 27017         # 數據庫端口
myIP = "Not Set"       # 本機 IP
myPort = 4444          # Shell 監聽端口
uri = "Not Set"        # URI 路徑
httpMethod = "GET"     # HTTP 方法
https = "OFF"          # HTTPS 開關
platform = "Not Set"   # 數據庫平台
postData = {}          # POST 數據
args_headers = {}      # 請求頭
verb = "OFF"           # 詳細模式開關
language = "en"        # 當前語言

# HTTP認證變量
httpUser = "Not Set"   # HTTP 認證用戶名
httpPass = "Not Set"   # HTTP 認證密碼
httpAuth = "Not Set"   # HTTP 認證類型

# 默認的數據庫端口
DEFAULT_DB_PORTS = {
    "MongoDB": 27017,
    "CouchDB": 5984,
    "Redis": 6379,
    "Neo4j": 7687
}

# 默認的目標超時設置
DEFAULT_TIMEOUT = 2  # 秒

# 可用的數據庫平台
AVAILABLE_PLATFORMS = ["MongoDB", "CouchDB", "Redis", "Neo4j"]

def init_config():
    """
    初始化/重置全局配置變量
    """
    global victim, webPort, dbPort, myIP, myPort, uri, httpMethod, https, platform, postData, args_headers, verb, language, httpUser, httpPass, httpAuth
    
    victim = "Not Set"
    webPort = 80
    dbPort = 27017
    myIP = "Not Set"
    myPort = 4444
    uri = "Not Set"
    httpMethod = "GET"
    https = "OFF"
    platform = "Not Set"
    postData = {}
    args_headers = {}
    verb = "OFF"
    language = "en"
    httpUser = "Not Set"
    httpPass = "Not Set"
    httpAuth = "Not Set"

def get_config():
    """
    獲取當前配置
    
    Returns:
        dict: 包含當前配置的字典
    """
    return {
        "victim": victim,
        "webPort": webPort,
        "dbPort": dbPort,
        "myIP": myIP,
        "myPort": myPort,
        "uri": uri,
        "httpMethod": httpMethod,
        "https": https,
        "platform": platform,
        "postData": postData,
        "args_headers": args_headers,
        "verb": verb,
        "language": language,
        "httpUser": httpUser,
        "httpPass": httpPass,
        "httpAuth": httpAuth
    }

def update_config(config_dict):
    """
    使用字典更新配置
    
    Args:
        config_dict (dict): 包含要更新的配置項的字典
    """
    global victim, webPort, dbPort, myIP, myPort, uri, httpMethod, https, platform, postData, args_headers, verb, language, httpUser, httpPass, httpAuth
    
    if "victim" in config_dict:
        victim = config_dict["victim"]
    if "webPort" in config_dict:
        webPort = config_dict["webPort"]
    if "dbPort" in config_dict:
        dbPort = config_dict["dbPort"]
    if "myIP" in config_dict:
        myIP = config_dict["myIP"]
    if "myPort" in config_dict:
        myPort = config_dict["myPort"]
    if "uri" in config_dict:
        uri = config_dict["uri"]
    if "httpMethod" in config_dict:
        httpMethod = config_dict["httpMethod"]
    if "https" in config_dict:
        https = config_dict["https"]
    if "platform" in config_dict:
        platform = config_dict["platform"]
    if "postData" in config_dict:
        postData = config_dict["postData"]
    if "args_headers" in config_dict:
        args_headers = config_dict["args_headers"]
    if "verb" in config_dict:
        verb = config_dict["verb"]
    if "language" in config_dict:
        language = config_dict["language"]
    if "httpUser" in config_dict:
        httpUser = config_dict["httpUser"]
    if "httpPass" in config_dict:
        httpPass = config_dict["httpPass"]
    if "httpAuth" in config_dict:
        httpAuth = config_dict["httpAuth"] 