import json
import requests
import asyncio
import os
import urllib.parse
from typing import Dict, Any, Optional
from browser_navigator import BrowserNavigator

class MCPClient:
    def __init__(self):
        self.browser_navigator = BrowserNavigator()
        self.use_browser_fallback = True  # 启用浏览器备选方案
        
        # 高德地图API配置
        self.amap_key = os.getenv('AMAP_API_KEY', '')
        self.amap_base_url = "https://restapi.amap.com/v3"
        
        # 请求配置
        self.timeout = 10  # 正常请求超时时间
        self.test_timeout = 3  # 测试连接超时时间
        self.headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Fellow-Traveler/1.0'
        }
    
    def test_amap_connection(self) -> bool:
        """测试高德地图API连接"""
        try:
            if not self.amap_key:
                print("❌ 未配置高德地图API密钥")
                return False
            
            print("🔍 测试高德地图API连接...")
            
            # 使用简单的行政区查询测试连接
            test_url = f"{self.amap_base_url}/config/district"
            params = {
                'key': self.amap_key,
                'keywords': '中国',
                'subdistrict': 0
            }
            
            response = requests.get(test_url, params=params, timeout=self.test_timeout)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('status') == '1':
                    print("✅ 高德地图API连接成功")
                    return True
                else:
                    error_info = result.get('info', '未知错误')
                    print(f"❌ 高德地图API错误: {error_info}")
                    return False
            else:
                print(f"❌ 高德地图API响应异常: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ 高德地图API连接失败: {e}")
            return False
    
    def send_amap_request(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """发送高德地图API请求"""
        try:
            # 构建请求URL
            url = f"{self.amap_base_url}/{endpoint}"
            
            # 添加API密钥
            params['key'] = self.amap_key
            params['output'] = 'json'
            
            print(f"🌐 发送高德API请求: {endpoint}")
            
            # 发送GET请求
            response = requests.get(
                url, 
                params=params, 
                headers=self.headers, 
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ 高德API请求成功")
                return result
            else:
                error_msg = f"HTTP {response.status_code}: {response.text}"
                print(f"❌ 高德API请求失败: {error_msg}")
                return {"error": error_msg}
                
        except requests.exceptions.Timeout:
            error_msg = "请求超时"
            print(f"❌ 高德API请求超时")
            return {"error": error_msg}
        except requests.exceptions.RequestException as e:
            error_msg = f"网络请求错误: {e}"
            print(f"❌ 高德API网络错误: {error_msg}")
            return {"error": error_msg}
        except Exception as e:
            error_msg = f"高德API请求异常: {e}"
            print(f"❌ 高德API请求异常: {error_msg}")
            return {"error": error_msg}
    
    def navigate_to_destination(self, origin: str, destination: str):
        """调用高德地图导航"""
        # 优先尝试高德API导航
        if not self.use_browser_fallback and self.amap_key:
            print(f"🗺️ 使用高德地图API导航: {origin} -> {destination}")
            
            try:
                # 首先将地址转换为坐标
                print("📍 转换地址为坐标...")
                origin_coords = self.browser_navigator.geocode_address(origin) if origin != "当前位置" else None
                dest_coords = self.browser_navigator.geocode_address(destination)
                
                if not dest_coords:
                    print("❌ 无法获取终点坐标，切换到浏览器导航")
                    return self.browser_navigator.open_navigation(origin, destination)
                
                # 构建坐标字符串
                origin_coord_str = f"{origin_coords[0]},{origin_coords[1]}" if origin_coords else None
                dest_coord_str = f"{dest_coords[0]},{dest_coords[1]}"
                
                print(f"   起点坐标: {origin_coord_str if origin_coord_str else '当前位置'}")
                print(f"   终点坐标: {dest_coord_str}")
                
                # 发送路径规划请求到高德API
                api_params = {
                    "destination": dest_coord_str,
                    "strategy": 0,  # 0-速度优先，1-费用优先，2-距离优先，3-不走高速
                    "extensions": "all"
                }
                
                # 如果有起点坐标，添加到参数中
                if origin_coord_str:
                    api_params["origin"] = origin_coord_str
                
                response = self.send_amap_request("direction/driving", api_params)
                
                if "error" not in response and response.get("status") == "1":
                    route_info = response.get("route", {})
                    paths = route_info.get("paths", [])
                    
                    if paths:
                        path = paths[0]
                        distance = path.get("distance", "未知")
                        duration = path.get("duration", "未知")
                        
                        print(f"✅ 高德API导航路线规划成功:")
                        print(f"   📏 距离: {distance}米")
                        print(f"   ⏱️ 预计时间: {int(float(duration))//60}分钟")
                        
                        # 构建高德地图URL并打开（使用坐标）
                        import webbrowser
                        
                        if origin_coords:
                            map_url = f"https://uri.amap.com/navigation?from={origin_coord_str}&to={dest_coord_str}&fromname={urllib.parse.quote(origin)}&toname={urllib.parse.quote(destination)}&mode=car"
                        else:
                            map_url = f"https://uri.amap.com/navigation?to={dest_coord_str}&toname={urllib.parse.quote(destination)}&mode=car"
                        
                        print(f"🔗 导航URL: {map_url}")
                        webbrowser.open(map_url)
                        
                        return True, f"高德API导航成功，距离{distance}米，预计{int(float(duration))//60}分钟"
                    else:
                        print("❌ 高德API导航未找到路线")
                else:
                    error_msg = response.get("info", "未知错误")
                    print(f"❌ 高德API导航失败: {error_msg}")
                
                # API失败，切换到浏览器导航
                print("🔄 切换到浏览器导航")
                return self.browser_navigator.open_navigation(origin, destination)
                
            except Exception as e:
                print(f"❌ 高德API导航调用异常: {e}")
                print("🔄 切换到浏览器导航")
                return self.browser_navigator.open_navigation(origin, destination)
        else:
            # 直接使用浏览器导航
            print("🌐 使用浏览器导航模式")
            return self.browser_navigator.open_navigation(origin, destination)
    
    def search_location(self, address: str):
        """搜索地址位置"""
        # 优先使用高德API搜索
        if not self.use_browser_fallback and self.amap_key:
            print(f"🔍 使用高德地图API搜索: {address}")
            
            try:
                # 发送地理编码请求到高德API
                response = self.send_amap_request(
                    "geocode/geo",
                    {
                        "address": address,
                        "city": "全国"
                    }
                )
                
                if "error" not in response and response.get("status") == "1":
                    geocodes = response.get("geocodes", [])
                    
                    if geocodes:
                        location = geocodes[0]
                        formatted_address = location.get("formatted_address", address)
                        location_coords = location.get("location", "")
                        
                        print(f"✅ 高德API搜索成功:")
                        print(f"   📍 地址: {formatted_address}")
                        print(f"   🌐 坐标: {location_coords}")
                        
                        # 构建高德地图搜索URL并打开
                        search_url = f"https://uri.amap.com/marker?position={location_coords}&name={formatted_address}"
                        import webbrowser
                        webbrowser.open(search_url)
                        
                        return formatted_address, "高德API搜索成功"
                    else:
                        print("❌ 高德API搜索未找到结果")
                else:
                    error_msg = response.get("info", "未知错误")
                    print(f"❌ 高德API搜索失败: {error_msg}")
                
                # API失败，切换到浏览器搜索
                print("🔄 切换到浏览器搜索")
                return self.browser_navigator.open_simple_search(address)
                
            except Exception as e:
                print(f"❌ 高德API搜索调用异常: {e}")
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
            
            # 发送天气请求到高德API
            response = self.send_amap_request(
                "weather/weatherInfo",
                {
                    "city": city,
                    "extensions": "base"
                }
            )
            
            if "error" not in response and response.get("status") == "1":
                lives = response.get("lives", [])
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
        
        # 测试高德API连接
        amap_available = self.test_amap_connection()
        
        # 测试浏览器导航
        browser_available = self.browser_navigator.test_api_connection()
        
        if amap_available:
            print("✅ 高德地图API可用，优先使用API导航")
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
        mode = "浏览器导航" if use_browser else "高德地图API导航"
        print(f"🔧 导航模式已设置为: {mode}")
    
    def get_navigation_info(self) -> Dict[str, Any]:
        """获取导航配置信息"""
        # 安全地测试API连接
        amap_available = False
        if self.amap_key:
            try:
                amap_available = self.test_amap_connection()
            except Exception as e:
                print(f"⚠️ 测试高德API连接时出错: {e}")
                amap_available = False
        
        # 安全地测试浏览器导航
        browser_available = False
        try:
            browser_available = self.browser_navigator.test_api_connection()
        except Exception as e:
            print(f"⚠️ 测试浏览器导航时出错: {e}")
            browser_available = False
        
        return {
            "amap_available": amap_available,
            "browser_available": browser_available,
            "current_mode": "浏览器导航" if self.use_browser_fallback else "高德地图API导航",
            "amap_key_configured": bool(self.amap_key),
            "amap_base_url": self.amap_base_url if self.amap_key else "未配置"
        }
     