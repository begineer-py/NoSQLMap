"""
NoSQLMap 檢測模塊 - 包含數據庫平台檢測功能
"""

import pymongo
import couchdb
import redis
import urllib.parse
import requests
from neo4j import GraphDatabase
from . import config
from i18n_utils import get_message

def detect_platform(target, port=None):
    """
    檢測目標主機上運行的數據庫平台
    
    Args:
        target (str): 目標主機名或IP地址
        port (int, optional): 目標端口，如果未指定則嘗試所有默認端口
        
    Returns:
        tuple: (檢測到的平台名稱, 端口號), 如果沒有檢測到則返回 (None, None)
    """
    # 清理URL前綴，如果存在
    if target.startswith(('http://', 'https://')):
        target = urllib.parse.urlparse(target).netloc
    
    # 如果主機名包含端口，提取主機名
    if ':' in target and not target.endswith(']'):  # IPv6地址會用[]包圍
        target = target.split(':')[0]
    
    print(f"[*] 嘗試檢測平台類型...")
    
    # 如果指定了端口，只檢測該端口
    if port:
        return check_platform(target, port)
        
    # 否則嘗試所有已知平台的默認端口
    for platform_name, default_port in config.DEFAULT_DB_PORTS.items():
        detected, port = check_platform(target, default_port, platform_name)
        if detected:
            return detected, port
    
    # 如果所有檢測都失敗，返回None並使用默認MongoDB
    print(f"[!] 無法檢測到支持的資料庫平台")
    return None, None

def check_platform(target, port, platform_name=None):
    """
    檢查目標端口上運行的平台
    
    Args:
        target (str): 目標主機名或IP地址
        port (int): 目標端口
        platform_name (str, optional): 如果指定，只檢測該平台
        
    Returns:
        tuple: (檢測到的平台名稱, 端口號), 如果沒有檢測到則返回 (None, None)
    """
    if not platform_name or platform_name == "MongoDB":
        print(f"[*] 嘗試連接 MongoDB: {target}:{port}")
        try:
            # 設置超時以避免長時間等待
            client = pymongo.MongoClient(f"mongodb://{target}:{port}", 
                                         serverSelectionTimeoutMS=config.DEFAULT_TIMEOUT * 1000)
            # 嘗試列出數據庫以驗證連接
            client.list_database_names()
            print(f"[+] 在端口 {port} 檢測到平台: MongoDB")
            return "MongoDB", port
        except Exception as e:
            print(f"[!] MongoDB 連接失敗: {e}")
            
    if not platform_name or platform_name == "CouchDB":
        print(f"[*] 嘗試連接 CouchDB: {target}:{port}")
        try:
            response = requests.get(f"http://{target}:{port}/", timeout=config.DEFAULT_TIMEOUT)
            if 'couchdb' in response.text.lower():
                print(f"[+] 在端口 {port} 檢測到平台: CouchDB")
                return "CouchDB", port
        except Exception as e:
            print(f"[!] CouchDB 連接失敗: {e}")
            
    if not platform_name or platform_name == "Redis":
        print(f"[*] 嘗試連接 Redis: {target}:{port}")
        try:
            r = redis.Redis(host=target, port=port, socket_timeout=config.DEFAULT_TIMEOUT)
            # 嘗試執行 PING 命令以驗證連接
            if r.ping():
                print(f"[+] 在端口 {port} 檢測到平台: Redis")
                return "Redis", port
        except Exception as e:
            print(f"[!] Redis 檢測錯誤: {e}")
            
    if not platform_name or platform_name == "Neo4j":
        print(f"[*] 嘗試連接 Neo4j: {target}:{port}")
        try:
            # 嘗試連接 Neo4j（不使用憑據）
            uri = f"bolt://{target}:{port}"
            driver = GraphDatabase.driver(uri, connection_timeout=config.DEFAULT_TIMEOUT)
            with driver.session() as session:
                # 簡單查詢以測試連接
                session.run("RETURN 1")
            print(f"[+] 在端口 {port} 檢測到平台: Neo4j")
            return "Neo4j", port
        except Exception as e:
            print(f"[!] Neo4j 連接失敗: {e}")
    
    # 如果指定了平台但檢測失敗
    if platform_name:
        print(f"[*] 在端口 {port} 上檢測失敗，默認使用平台: {platform_name}")
        return platform_name, port
    
    return None, None 