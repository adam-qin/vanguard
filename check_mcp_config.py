#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from config import AMAP_API_KEY, AMAP_MCP_BASE_URL

def check_mcp_configuration():
    """检查MCP配置"""
    print("=== 高德MCP配置检查 ===")
    
    # 检查API密钥
    if AMAP_API_KEY and AMAP_API_KEY != 'your-amap-api-key':
        print(f"✅ 高德API密钥: 已配置 ({AMAP_API_KEY[:8]}...)")
    else:
        print("❌ 高德API密钥: 未配置或使用默认值")
        print("   请在.env文件中设置 AMAP_API_KEY")
        return False
    
    # 检查MCP URL
    print(f"🌐 MCP服务器URL: {AMAP_MCP_BASE_URL}")
    
    # 检查环境变量
    env_key = os.getenv('AMAP_API_KEY')
    if env_key:
        print(f"✅ 环境变量AMAP_API_KEY: 已设置")
    else:
        print("⚠️ 环境变量AMAP_API_KEY: 未设置，使用配置文件中的默认值")
    
    # 测试网络连接
    try:
        import requests
        print("\n🔍 测试网络连接...")
        
        # 测试高德API连接
        test_url = "https://restapi.amap.com/v3/config/district"
        params = {
            'key': AMAP_API_KEY,
            'keywords': '中国',
            'subdistrict': 0
        }
        
        response = requests.get(test_url, params=params, timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('status') == '1':
                print("✅ 高德API连接正常")
                return True
            else:
                print(f"❌ 高德API返回错误: {result.get('info', '未知错误')}")
                return False
        else:
            print(f"❌ 高德API连接失败: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 网络连接测试失败: {e}")
        return False

def show_configuration_guide():
    """显示配置指南"""
    print(f"\n=== 配置指南 ===")
    print("1. 获取高德地图API密钥:")
    print("   - 访问: https://console.amap.com/")
    print("   - 注册/登录账号")
    print("   - 创建应用，获取API密钥")
    
    print(f"\n2. 配置API密钥:")
    print("   方法1: 在.env文件中添加:")
    print("   AMAP_API_KEY=your_actual_api_key")
    
    print(f"\n   方法2: 直接修改config.py文件:")
    print("   AMAP_API_KEY = 'your_actual_api_key'")
    
    print(f"\n3. 重启程序使配置生效")

if __name__ == "__main__":
    success = check_mcp_configuration()
    
    if not success:
        show_configuration_guide()
    else:
        print(f"\n🎉 MCP配置检查通过！可以使用高德MCP服务器功能")