"""
NoSQLMap注入載荷模組
提供各種NoSQL數據庫的注入載荷和攻擊向量
"""

# 版本信息
__version__ = '0.1.0'

# 支持的平台列表
SUPPORTED_PLATFORMS = ['mongodb', 'neo4j', 'redis', 'couchdb']

def get_platform_payloads(platform_name):
    """
    根據指定的平台名稱獲取對應的載荷模組
    
    Args:
        platform_name (str): 平台名稱，如'mongodb', 'neo4j'等
        
    Returns:
        module: 對應平台的載荷模組，如果不支持則返回None
    """
    platform_name = platform_name.lower()
    if platform_name not in SUPPORTED_PLATFORMS:
        return None
    
    try:
        if platform_name == 'mongodb':
            from .mongodb import auth_bypass, blind_injection
            return {
                'auth_bypass': auth_bypass,
                'blind_injection': blind_injection
            }
        elif platform_name == 'neo4j':
            from .neo4j import auth_bypass, blind_injection
            return {
                'auth_bypass': auth_bypass,
                'blind_injection': blind_injection
            }
        elif platform_name == 'redis':
            from .redis import injection
            return {
                'injection': injection
            }
        elif platform_name == 'couchdb':
            from .couchdb import injection
            return {
                'injection': injection
            }
    except ImportError as e:
        print(f"無法導入{platform_name}載荷模組: {str(e)}")
        return None
    
    return None 