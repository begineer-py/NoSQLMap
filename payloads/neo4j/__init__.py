"""
Neo4j 注入載荷模組
包含用於Neo4j Cypher查詢注入的各種類型載荷
"""

# 检查是否存在子模块文件
import os
import importlib.util

# 获取当前目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 要导入的模块
modules_to_import = ['auth_bypass', 'blind_injection']
available_modules = {}

# 循环检查并导入可用模块
for module_name in modules_to_import:
    module_path = os.path.join(current_dir, f"{module_name}.py")
    
    # 检查文件是否存在
    if os.path.exists(module_path):
        try:
            # 动态导入模块
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # 将模块添加到当前命名空间和字典中
            globals()[module_name] = module
            available_modules[module_name] = module
        except Exception as e:
            print(f"导入 {module_name} 时出错: {str(e)}")

# 公開子模組
__all__ = list(available_modules.keys()) 