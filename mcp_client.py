import json
import requests
import asyncio
import os
from typing import Dict, Any, Optional
from browser_navigator import BrowserNavigator

class MCPClient:
    def __init__(self):
        self.browser_navigator = BrowserNavigator()
        self.use_browser_fallback = True  # 启用浏览器备选方案
        
        # 高德地图MCP服务器配置
        self.amap_key = os.getenv('AMAP_API_KEY', '')
        self.mcp_base_url = f"https://mcp.amap.com/mcp?key={self.amap_key}"
        
        # 请求配置
        self.timeout = 10
        self.headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Fellow-Traveler/1.0'
        }
    
    def test_mcp_connection(self) -> bool:
        """测试高德MCP服务器连接"""
        try:
            if not self.amap_key:
                print("❌ 未配置高德地图API密钥")
                return False
            
            print("🔍 测试高德MCP服务器连接...")
            
            # 测试连接
            test_url = f"{self.mcp_base_url}&method=ping"
            response = requests.get(test_url, headers=self.headers, timeout=self.timeout)
            
            if response.status_code == 200:
                print("✅ 高德MCP服务器连接成功")
                return True
            else:
                print(f"❌ 高德MCP服务器响应异常: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ 高德MCP服务器连接失败: {e}")
            return False
    
    def send_mcp_request(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """发送高德MCP请求"""
        try:
            # 构建请求URL
            url = f"{self.mcp_base_url}&method={method}"
            
            # 构建请求数据
            request_data = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": method,
                "params": params
            }
            
            print(f"🌐 发送MCP请求: {method}")
            
            # 发送POST请求
            response = requests.post(
                url, 
                json=request_data, 
                headers=self.headers, 
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ MCP请求成功")
                return result
            else:
                error_msg = f"HTTP {response.status_code}: {response.text}"
                print(f"❌ MCP请求失败: {error_msg}")
                return {"error": error_msg}
                
        except requests.exceptions.Timeout:
            error_msg = "请求超时"
            print(f"❌ MCP请求超时")
            return {"error": error_msg}
        except requests.exceptions.RequestException as e:
            error_msg = f"网络请求错误: {e}"
            print(f"❌ MCP网络错误: {error_msg}")
            return {"error": error_msg}
        except Exception as e:
            error_msg = f"MCP请求异常: {e}"
            print(f"❌ MCP请求异常: {error_msg}")
            return {"error": error_msg}
    
    def navigate_to_destination(self, origin: str, destination: str):
        """调用高德地图导航"""
        # 优先尝试MCP服务器导航
        if not self.use_browser_fallback and self.amap_key:
            print(f"🗺️ 使用高德MCP服务器导航: {origin} -> {destination}")
            
            try:
                # 发送导航请求到高德MCP服务器
                response = self.send_mcp_request(
                    "navigation.route",
                    {
                        "origin": origin,
                        "destination": destination,
                        "strategy": "0",  # 0-速度优先，1-费用优先，2-距离优先，3-不走高速
                        "extensions": "all",
                        "output": "json"
                    }
                )
                
                if "error" not in response and response.get("result"):
                    result = response["result"]
                    if result.get("status") == "1":  # 成功
                        route_info = result.get("route", {})
                        paths = route_info.get("paths", [])
                        
                        if paths:
                            path = paths[0]
                            distance = path.get("distance", "未知")
                            duration = path.get("duration", "未知")
                            
                            print(f"✅ MCP导航路线规划成功:")
                            print(f"   📏 距离: {distance}米")
                            print(f"   ⏱️ 预计时间: {int(duration)//60}分钟")
                            
                            # 构建高德地图URL并打开
                            map_url = f"https://uri.amap.com/navigation?from={origin}&to={destination}&mode=car"
                            import webbrowser
                            webbrowser.open(map_url)
                            
                            return True, f"MCP导航成功，距离{distance}米，预计{int(duration)//60}分钟"
                        else:
                            print("❌ MCP导航未找到路线")
                    else:
                        error_msg = result.get("info", "未知错误")
                        print(f"❌ MCP导航失败: {error_msg}")
                else:
                    print(f"❌ MCP导航请求失败: {response.get('error', '未知错误')}")
                
                # MCP失败，切换到浏览器导航
                print("🔄 切换到浏览器导航")
                return self.browser_navigator.open_navigation(origin, destination)
                
            except Exception as e:
                print(f"❌ MCP导航调用异常: {e}")
                print("🔄 切换到浏览器导航")
                return self.browser_navigator.open_navigation(origin, destination)
        else:
            # 直接使用浏览器导航
            print("🌐 使用浏览器导航模式")
            return self.browser_navigator.open_navigation(origin, destination)
    
    def search_location(self, address: str):
        """搜索地址位置"""
        # 优先使用MCP服务器搜索
        if not self.use_browser_fallback and self.amap_key:
            print(f"🔍 使用高德MCP服务器搜索: {address}")
            
            try:
                # 发送搜索请求到高德MCP服务器
                response = self.send_mcp_request(
                    "geocode.geo",
                    {
                        "address": address,
                        "city": "全国",
                        "output": "json"
                    }
                )
                
                if "error" not in response and response.get("result"):
                    result = response["result"]
                    if result.get("status") == "1":  # 成功
                        geocodes = result.get("geocodes", [])
                        
                        if geocodes:
                            location = geocodes[0]
                            formatted_address = location.get("formatted_address", address)
                            location_coords = location.get("location", "")
                            
                            print(f"✅ MCP搜索成功:")
                            print(f"   📍 地址: {formatted_address}")
                            print(f"   🌐 坐标: {location_coords}")
                            
                            # 构建高德地图搜索URL并打开
                            search_url = f"https://uri.amap.com/marker?position={location_coords}&name={formatted_address}"
                            import webbrowser
                            webbrowser.open(search_url)
                            
                            return formatted_address, "MCP搜索成功"
                        else:
                            print("❌ MCP搜索未找到结果")
                    else:
                        error_msg = result.get("info", "未知错误")
                        print(f"❌ MCP搜索失败: {error_msg}")
                else:
                    print(f"❌ MCP搜索请求失败: {response.get('error', '未知错误')}")
                
                # MCP失败，切换到浏览器搜索
                print("🔄 切换到浏览器搜索")
                return self.browser_navigator.open_simple_search(address)
                
            except Exception as e:
                print(f"❌ MCP搜索调用异常: {e}")
                print("🔄 切换到浏览器搜索")
                return self.browser_navigator.open_simple_search(address)
        else:
            # 直接使用浏览器搜索
            print("🌐 使用浏览器搜索模式")
            return self.browser_navigator.open_simple_search(address)
    
    def get_weather_info(self, city: str) -> Optional[Dict[str, Any]]:
        """获取天气信息"""
        if not self.amap_key:
            print("❌ 未配置高德地图API密钥，无法获取天气信息")
            return None
            
        try:
            print(f"🌤️ 获取{city}天气信息...")
            
            # 发送天气请求到高德MCP服务器
            response = self.send_mcp_request(
                "weather.weatherInfo",
                {
                    "city": city,
                    "extensions": "all",
                    "output": "json"
                }
            )
            
            if "error" not in response and response.get("result"):
                result = response["result"]
                if result.get("status") == "1":  # 成功
                    lives = result.get("lives", [])
                    if lives:
                        weather = lives[0]
                        return {
                            "city": weather.get("city", city),
                            "weather": weather.get("weather", "未知"),
                            "temperature": weather.get("temperature", "未知"),
                            "humidity": weather.get("humidity", "未知"),
                            "winddirection": weather.get("winddirection", "未知"),
                            "windpower": weather.get("windpower", "未知"),
                            "reporttime": weather.get("reporttime", "未知")
                        }
            
            print(f"❌ 获取{city}天气信息失败")
            return None
            
        except Exception as e:
            print(f"❌ 天气信息获取异常: {e}")
            return None
    
    def test_navigation_methods(self):
        """测试可用的导航方法"""
        print("🔍 正在测试导航方法...")
        
        # 测试高德MCP服务器连接
        mcp_available = self.test_mcp_connection()
        
        # 测试浏览器导航
        browser_available = self.browser_navigator.test_api_connection()
        
        if mcp_available:
            print("✅ 高德MCP服务器可用，优先使用MCP导航")
            self.use_browser_fallback = False
            return True
        elif browser_available:
            print("✅ 浏览器导航可用，使用浏览器导航")
            self.use_browser_fallback = True
            return True
        else:
            print("❌ 所有导航方法都不可用")
            self.use_browser_fallback = True  # 默认使用浏览器
            return False
    
    def set_navigation_mode(self, use_browser: bool):
        """设置导航模式"""
        self.use_browser_fallback = use_browser
        mode = "浏览器导航" if use_browser else "高德MCP服务器导航"
        print(f"🔧 导航模式已设置为: {mode}")
    
    def get_navigation_info(self) -> Dict[str, Any]:
        """获取导航配置信息"""
        return {
            "mcp_available": bool(self.amap_key and self.test_mcp_connection()),
            "browser_available": self.browser_navigator.test_api_connection(),
            "current_mode": "浏览器导航" if self.use_browser_fallback else "高德MCP服务器导航",
            "amap_key_configured": bool(self.amap_key),
            "mcp_base_url": self.mcp_base_url if self.amap_key else "未配置"
        }