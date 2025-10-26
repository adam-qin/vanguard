#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环境变量加载器
支持从.env文件加载环境变量
"""

import os
from typing import Dict, Optional

class EnvLoader:
    """环境变量加载器"""
    
    @staticmethod
    def load_env_file(env_file: str = '.env') -> Dict[str, str]:
        """从.env文件加载环境变量"""
        env_vars = {}
        
        if not os.path.exists(env_file):
            print(f"⚠️ 环境变量文件 {env_file} 不存在")
            return env_vars
        
        try:
            with open(env_file, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    
                    # 跳过空行和注释
                    if not line or line.startswith('#'):
                        continue
                    
                    # 解析键值对
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        
                        # 移除引号
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        elif value.startswith("'") and value.endswith("'"):
                            value = value[1:-1]
                        
                        env_vars[key] = value
                        
                        # 设置到系统环境变量（如果尚未设置）
                        if key not in os.environ:
                            os.environ[key] = value
                    else:
                        print(f"⚠️ {env_file}:{line_num} 格式错误: {line}")
            
            print(f"✅ 成功加载 {len(env_vars)} 个环境变量从 {env_file}")
            return env_vars
            
        except Exception as e:
            print(f"❌ 加载环境变量文件失败: {e}")
            return env_vars
    
    @staticmethod
    def get_env_var(key: str, default: str = '', required: bool = False) -> str:
        """获取环境变量"""
        value = os.getenv(key, default)
        
        if required and not value:
            raise ValueError(f"必需的环境变量 {key} 未设置")
        
        return value
    
    @staticmethod
    def get_bool_env_var(key: str, default: bool = False) -> bool:
        """获取布尔类型环境变量"""
        value = os.getenv(key, str(default)).lower()
        return value in ('true', '1', 'yes', 'on')
    
    @staticmethod
    def get_int_env_var(key: str, default: int = 0) -> int:
        """获取整数类型环境变量"""
        try:
            return int(os.getenv(key, str(default)))
        except ValueError:
            return default
    
    @staticmethod
    def check_required_vars(required_vars: list) -> Dict[str, bool]:
        """检查必需的环境变量"""
        results = {}
        
        for var in required_vars:
            value = os.getenv(var)
            results[var] = bool(value and value.strip())
        
        return results
    
    @staticmethod
    def print_env_status():
        """打印环境变量状态"""
        print("=== 环境变量状态 ===")
        
        # 基础配置
        print("基础配置:")
        dashscope_key = os.getenv('DASHSCOPE_API_KEY', '')
        if dashscope_key:
            masked_key = dashscope_key[:8] + '...' + dashscope_key[-4:] if len(dashscope_key) > 12 else '***'
            print(f"  ✅ DASHSCOPE_API_KEY: {masked_key}")
        else:
            print(f"  ❌ DASHSCOPE_API_KEY: 未设置")
        
        # 七牛云MCP配置
        print("\n七牛云MCP配置:")
        openai_url = os.getenv('OPENAI_BASE_URL', '')
        openai_key = os.getenv('OPENAI_API_KEY', '')
        mcp_model = os.getenv('MCP_MODEL', 'deepseek-v3-tool')
        use_qiniu = os.getenv('USE_QINIU_MCP', 'true')
        
        print(f"  {'✅' if openai_url else '❌'} OPENAI_BASE_URL: {openai_url or '未设置'}")
        if openai_key:
            masked_key = openai_key[:8] + '...' + openai_key[-4:] if len(openai_key) > 12 else '***'
            print(f"  ✅ OPENAI_API_KEY: {masked_key}")
        else:
            print(f"  ❌ OPENAI_API_KEY: 未设置")
        print(f"  📋 MCP_MODEL: {mcp_model}")
        print(f"  🔧 USE_QINIU_MCP: {use_qiniu}")
        
        # 传统高德API配置
        print("\n传统高德API配置:")
        amap_key = os.getenv('AMAP_API_KEY', '')
        if amap_key:
            masked_key = amap_key[:8] + '...' + amap_key[-4:] if len(amap_key) > 12 else '***'
            print(f"  ✅ AMAP_API_KEY: {masked_key}")
        else:
            print(f"  ❌ AMAP_API_KEY: 未设置")
        
        # 语音配置
        print("\n语音配置:")
        xfyun_app_id = os.getenv('XFYUN_APP_ID', '')
        xfyun_api_key = os.getenv('XFYUN_API_KEY', '')
        use_xfyun = os.getenv('USE_XFYUN_ASR', 'true')
        
        print(f"  {'✅' if xfyun_app_id else '❌'} XFYUN_APP_ID: {xfyun_app_id or '未设置'}")
        if xfyun_api_key:
            masked_key = xfyun_api_key[:8] + '...' + xfyun_api_key[-4:] if len(xfyun_api_key) > 12 else '***'
            print(f"  ✅ XFYUN_API_KEY: {masked_key}")
        else:
            print(f"  ❌ XFYUN_API_KEY: 未设置")
        print(f"  🔧 USE_XFYUN_ASR: {use_xfyun}")
        
        print("=" * 30)

def load_environment():
    """加载环境变量的便捷函数"""
    loader = EnvLoader()
    
    # 尝试加载.env文件
    env_vars = loader.load_env_file('.env')
    
    # 如果.env不存在，尝试加载.env.example作为模板提示
    if not env_vars and os.path.exists('.env.example'):
        print("💡 提示: 发现 .env.example 文件，请复制为 .env 并配置实际值")
    
    return env_vars

if __name__ == "__main__":
    # 测试环境变量加载
    load_environment()
    EnvLoader.print_env_status()