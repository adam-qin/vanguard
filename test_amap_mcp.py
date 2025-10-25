#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time

# 设置环境变量
os.environ['USE_XFYUN_ASR'] = 'true'

def test_amap_mcp_integration():
    """测试高德MCP服务器集成"""
    try:
        print("=== 高德MCP服务器集成测试 ===")
        
        from mcp_client import MCPClient
        
        # 创建MCP客户端
        mcp_client = MCPClient()
        
        # 1. 测试连接
        print("\n1. 测试高德MCP服务器连接...")
        connection_ok = mcp_client.test_mcp_connection()
        
        if not connection_ok:
            print("❌ 高德MCP服务器连接失败，请检查API密钥配置")
            return False
        
        # 2. 获取导航信息
        print("\n2. 获取导航配置信息...")
        nav_info = mcp_client.get_navigation_info()
        
        for key, value in nav_info.items():
            print(f"   {key}: {value}")
        
        # 3. 测试地址搜索
        print("\n3. 测试地址搜索...")
        test_addresses = [
            "深圳市南山区科技园",
            "深圳市福田区市民中心",
            "深圳市宝安区机场"
        ]
        
        for address in test_addresses:
            print(f"\n--- 搜索: {address} ---")
            result, message = mcp_client.search_location(address)
            print(f"结果: {result}")
            print(f"消息: {message}")
            time.sleep(1)
        
        # 4. 测试导航规划
        print("\n4. 测试导航规划...")
        test_routes = [
            ("深圳市南山区科技园", "深圳市福田区市民中心"),
            ("深圳市福田区市民中心", "深圳市宝安区机场"),
            ("当前位置", "深圳南山海岸城")
        ]
        
        for origin, destination in test_routes:
            print(f"\n--- 导航: {origin} → {destination} ---")
            success, message = mcp_client.navigate_to_destination(origin, destination)
            print(f"成功: {success}")
            print(f"消息: {message}")
            time.sleep(2)
        
        # 5. 测试天气信息
        print("\n5. 测试天气信息...")
        weather_cities = ["深圳", "北京", "上海"]
        
        for city in weather_cities:
            print(f"\n--- {city}天气 ---")
            weather = mcp_client.get_weather_info(city)
            if weather:
                print(f"   城市: {weather['city']}")
                print(f"   天气: {weather['weather']}")
                print(f"   温度: {weather['temperature']}°C")
                print(f"   湿度: {weather['humidity']}%")
                print(f"   风向: {weather['winddirection']}")
                print(f"   风力: {weather['windpower']}级")
                print(f"   更新时间: {weather['reporttime']}")
            else:
                print(f"   获取{city}天气信息失败")
            time.sleep(1)
        
        # 6. 测试导航模式切换
        print("\n6. 测试导航模式切换...")
        
        print("切换到MCP模式...")
        mcp_client.set_navigation_mode(False)
        success, message = mcp_client.navigate_to_destination("科技园", "海岸城")
        print(f"MCP导航结果: {success}, {message}")
        
        time.sleep(1)
        
        print("切换到浏览器模式...")
        mcp_client.set_navigation_mode(True)
        success, message = mcp_client.navigate_to_destination("科技园", "海岸城")
        print(f"浏览器导航结果: {success}, {message}")
        
        print(f"\n🎉 高德MCP服务器集成测试完成")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_mcp_vs_browser():
    """对比MCP和浏览器导航性能"""
    try:
        print(f"\n=== MCP vs 浏览器导航性能对比 ===")
        
        from mcp_client import MCPClient
        
        mcp_client = MCPClient()
        
        test_origin = "深圳市南山区科技园"
        test_destination = "深圳市福田区市民中心"
        
        # 测试MCP导航
        print(f"\n1. 测试MCP导航...")
        mcp_client.set_navigation_mode(False)
        
        start_time = time.time()
        success_mcp, message_mcp = mcp_client.navigate_to_destination(test_origin, test_destination)
        mcp_time = time.time() - start_time
        
        print(f"MCP导航结果: {success_mcp}")
        print(f"MCP导航消息: {message_mcp}")
        print(f"MCP导航耗时: {mcp_time:.2f}秒")
        
        time.sleep(2)
        
        # 测试浏览器导航
        print(f"\n2. 测试浏览器导航...")
        mcp_client.set_navigation_mode(True)
        
        start_time = time.time()
        success_browser, message_browser = mcp_client.navigate_to_destination(test_origin, test_destination)
        browser_time = time.time() - start_time
        
        print(f"浏览器导航结果: {success_browser}")
        print(f"浏览器导航消息: {message_browser}")
        print(f"浏览器导航耗时: {browser_time:.2f}秒")
        
        # 性能对比
        print(f"\n📊 性能对比:")
        print(f"   MCP导航: {mcp_time:.2f}秒")
        print(f"   浏览器导航: {browser_time:.2f}秒")
        
        if mcp_time < browser_time:
            print(f"   ✅ MCP导航更快 (快{browser_time - mcp_time:.2f}秒)")
        else:
            print(f"   ✅ 浏览器导航更快 (快{mcp_time - browser_time:.2f}秒)")
        
        return True
        
    except Exception as e:
        print(f"❌ 性能对比测试失败: {e}")
        return False

if __name__ == "__main__":
    success1 = test_amap_mcp_integration()
    success2 = test_mcp_vs_browser()
    
    if success1 and success2:
        print(f"\n🎉 所有测试通过！高德MCP服务器集成成功")
    else:
        print(f"\n⚠️ 部分测试失败，请检查配置")