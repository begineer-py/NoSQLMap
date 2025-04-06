"""
MongoDB 注入載荷模組
包含用於MongoDB注入的各種類型載荷
"""

# 引入子模組
from . import auth_bypass
from . import blind_injection

# 公開子模組
__all__ = ['auth_bypass', 'blind_injection'] 