#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import asyncio

# 设置环境变量
os.environ['DASHSCOPE_API_KEY'] = 'sk-9bf124f946124600b9d70824998dc2a2'
os.environ['AMAP_API_KEY'] = '95fd23e5ff3e8d97d46b5c07f5077a4e'
os.environ['XFYUN_APP_ID'] = 'f5df0409'
os.environ['XFYUN_API_SECRET'] = 'YTgwNDFmYzc2MmVjMDQ0NDQ0OWQyNmJm'
os.environ['XFYUN_API_KEY'] = '654d10ef61d2357133a93d84e6278628'
os.environ['USE_XFYUN_ASR'] = 'true'

from main import NavigationApp

async def test_voice_confirmation():
    """测试语音确认功能"""
    print("=== 语音确认功能测试 ===")
    
    try:
        app = NavigationApp()
        
        # 测试语音确认
        print("测试语音确认功能...")
        print("模拟导航确认: 从当前位置到南山区海岸城")
        
        confirmed = await app.voice_confirm_navigation("当前位置", "南山区海岸城")
        
        if confirmed:
            print("✅ 用户确认导航")
        else:
            print("❌ 用户取消导航")
            
        return confirmed
        
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_full_navigation_flow():
    """测试完整导航流程"""
    print("\n=== 完整导航流程测试 ===")
    
    try:
        app = NavigationApp()
        
        # 模拟处理导航请求
        test_input = "从当前位置到南山区海岸城"
        print(f"测试输入: {test_input}")
        
        await app.process_navigation_request(test_input)
        
        return True
        
    except Exception as e:
        print(f"完整流程测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("开始语音确认功能测试...\n")
    
    # 测试语音确认
    asyncio.run(test_voice_confirmation())
    
    print("\n" + "="*50 + "\n")
    
    # 测试完整流程
    asyncio.run(test_full_navigation_flow())
    
    print("\n测试完成！")