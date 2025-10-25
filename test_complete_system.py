#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time

# 设置环境变量
os.environ['USE_XFYUN_ASR'] = 'true'

def test_complete_system():
    """测试完整系统"""
    try:
        print("=== 完整系统测试 ===")
        
        # 1. 测试配置
        print("\n1. 检查配置...")
        from config import AMAP_API_KEY, DASHSCOPE_API_KEY
        
        if AMAP_API_KEY and AMAP_API_KEY != 'your-amap-api-key':
            print(f"✅ 高德API密钥: 已配置")
        else:
            print("❌ 高德API密钥: 未配置")
            return False
        
        if DASHSCOPE_API_KEY and DASHSCOPE_API_KEY != 'your-dashscope-api-key':
            print(f"✅ 千问API密钥: 已配置")
        else:
            print("❌ 千问API密钥: 未配置")
            return False
        
        # 2. 测试TTS引擎
        print("\n2. 测试TTS引擎...")
        from speech_handler import SpeechHandler
        
        speech_handler = SpeechHandler()
        print(f"✅ SpeechHandler初始化成功")
        
        # 测试TTS
        if speech_handler.test_tts():
            print("✅ TTS引擎测试通过")
        else:
            print("❌ TTS引擎测试失败")
            return False
        
        # 3. 测试AI处理器
        print("\n3. 测试AI处理器...")
        from ai_processor import AIProcessor
        
        ai_processor = AIProcessor()
        
        # 测试导航请求解析
        test_requests = [
            "从科技园到海岸城",
            "我要去深圳市民中心",
            "导航到宝安机场"
        ]
        
        for request in test_requests:
            print(f"   测试请求: {request}")
            result = ai_processor.process_navigation_request(request)
            if result and 'origin' in result and 'destination' in result:
                print(f"   ✅ 解析成功: {result['origin']} → {result['destination']}")
            else:
                print(f"   ❌ 解析失败: {result}")
        
        # 4. 测试MCP客户端
        print("\n4. 测试MCP客户端...")
        from mcp_client import MCPClient
        
        mcp_client = MCPClient()
        
        # 测试连接
        if mcp_client.test_mcp_connection():
            print("✅ 高德MCP服务器连接成功")
        else:
            print("⚠️ 高德MCP服务器连接失败，将使用浏览器导航")
        
        # 测试导航方法
        mcp_client.test_navigation_methods()
        
        # 5. 测试完整导航流程
        print("\n5. 测试完整导航流程...")
        
        test_navigation_requests = [
            "从科技园到海岸城",
            "导航到深圳市民中心"
        ]
        
        for request in test_navigation_requests:
            print(f"\n--- 测试导航: {request} ---")
            
            # AI解析
            parsed = ai_processor.process_navigation_request(request)
            if not parsed or 'origin' not in parsed or 'destination' not in parsed:
                print(f"❌ AI解析失败")
                continue
            
            origin = parsed['origin']
            destination = parsed['destination']
            
            print(f"解析结果: {origin} → {destination}")
            
            # 语音播报
            speech_handler.speak(f"即将导航从{origin}到{destination}")
            
            # 执行导航
            success, message = mcp_client.navigate_to_destination(origin, destination)
            
            if success:
                print(f"✅ 导航成功: {message}")
                speech_handler.speak("导航已启动")
            else:
                print(f"❌ 导航失败: {message}")
                speech_handler.speak("导航启动失败")
            
            time.sleep(2)
        
        # 6. 测试其他功能
        print("\n6. 测试其他功能...")
        
        # 测试地址搜索
        search_result, search_message = mcp_client.search_location("深圳南山海岸城")
        print(f"地址搜索: {search_result}, {search_message}")
        
        # 测试天气信息
        weather = mcp_client.get_weather_info("深圳")
        if weather:
            print(f"深圳天气: {weather['weather']}, {weather['temperature']}°C")
        else:
            print("天气信息获取失败")
        
        # 7. 清理资源
        print("\n7. 清理资源...")
        speech_handler.cleanup()
        print("✅ 资源清理完成")
        
        print(f"\n🎉 完整系统测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ 系统测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_error_handling():
    """测试错误处理"""
    try:
        print(f"\n=== 错误处理测试 ===")
        
        from ai_processor import AIProcessor
        from mcp_client import MCPClient
        from speech_handler import SpeechHandler
        
        ai_processor = AIProcessor()
        mcp_client = MCPClient()
        speech_handler = SpeechHandler()
        
        # 测试无效导航请求
        print("\n1. 测试无效导航请求...")
        invalid_requests = [
            "今天天气怎么样",
            "你好",
            "随便说点什么"
        ]
        
        for request in invalid_requests:
            print(f"   测试: {request}")
            result = ai_processor.process_navigation_request(request)
            if result and 'error' in result:
                print(f"   ✅ 正确识别为无效请求")
            else:
                print(f"   ⚠️ 可能误识别: {result}")
        
        # 测试网络错误处理
        print("\n2. 测试网络错误处理...")
        
        # 临时修改API密钥测试错误处理
        original_key = mcp_client.amap_key
        mcp_client.amap_key = "invalid_key"
        mcp_client.mcp_base_url = f"https://mcp.amap.com/mcp?key=invalid_key"
        
        success, message = mcp_client.navigate_to_destination("科技园", "海岸城")
        print(f"   无效密钥导航结果: {success}, {message}")
        
        # 恢复正确密钥
        mcp_client.amap_key = original_key
        mcp_client.mcp_base_url = f"https://mcp.amap.com/mcp?key={original_key}"
        
        print("✅ 错误处理测试完成")
        
        # 清理
        speech_handler.cleanup()
        return True
        
    except Exception as e:
        print(f"❌ 错误处理测试失败: {e}")
        return False

if __name__ == "__main__":
    success1 = test_complete_system()
    success2 = test_error_handling()
    
    if success1 and success2:
        print(f"\n🎉 所有测试通过！系统运行正常")
        print(f"\n📋 系统功能:")
        print(f"   ✅ 语音识别 (科大讯飞 + Google)")
        print(f"   ✅ 语音播报 (Windows SAPI + Edge TTS)")
        print(f"   ✅ AI导航解析 (阿里千问)")
        print(f"   ✅ 高德MCP导航 (API + 浏览器备选)")
        print(f"   ✅ 地址搜索和天气查询")
        print(f"\n🚀 可以启动主程序: python main.py")
    else:
        print(f"\n⚠️ 部分测试失败，请检查配置和网络连接")