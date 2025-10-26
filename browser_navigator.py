import webbrowser
import urllib.parse
import requests
import json
import os
from typing import Tuple, Optional
from config import AMAP_API_KEY

class BrowserNavigator:
    def __init__(self):
        self.amap_api_key = AMAP_API_KEY
        self.geocode_api = "https://restapi.amap.com/v3/geocode/geo"
        self.regeo_api = "https://restapi.amap.com/v3/geocode/regeo"
    
    def geocode_address(self, address: str) -> Optional[Tuple[float, float]]:
        """地址转换为经纬度坐标"""
        try:
            params = {
                'key': self.amap_api_key,
                'address': address,
                'output': 'json'
            }
            
            response = requests.get(self.geocode_api, params=params, timeout=3)
            data = response.json()
            
            if data['status'] == '1' and data['geocodes']:
                location = data['geocodes'][0]['location']
                lng, lat = map(float, location.split(','))
                print(f"地址 '{address}' 转换为坐标: ({lng}, {lat})")
                return lng, lat
            else:
                print(f"地址 '{address}' 转换失败: {data.get('info', '未知错误')}")
                return None
                
        except Exception as e:
            print(f"地址转换错误: {e}")
            return None
    
    def build_amap_url(self, origin: str, destination: str) -> str:
        """构建高德地图导航URL"""
        try:
            # 获取起点和终点坐标
            origin_coords = None
            dest_coords = None
            
            # 处理起点
            if origin and origin != "当前位置":
                origin_coords = self.geocode_address(origin)
            
            # 处理终点
            if destination:
                dest_coords = self.geocode_address(destination)
            
            if not dest_coords:
                # 如果无法获取坐标，使用地址名称
                base_url = "https://uri.amap.com/navigation"
                params = {
                    'to': destination,
                    'mode': 'car',  # 驾车导航
                    'policy': '1',  # 推荐路线
                    'src': 'myapp'
                }
                
                if origin and origin != "当前位置":
                    params['from'] = origin
                
                # 构建URL
                url = f"{base_url}?" + urllib.parse.urlencode(params, encoding='utf-8')
                return url
            
            # 使用坐标构建更精确的URL
            base_url = "https://uri.amap.com/navigation"
            params = {
                'to': f"{dest_coords[0]},{dest_coords[1]}",
                'toname': destination,
                'mode': 'car',
                'policy': '1',
                'src': 'myapp'
            }
            
            if origin_coords:
                params['from'] = f"{origin_coords[0]},{origin_coords[1]}"
                params['fromname'] = origin
            
            url = f"{base_url}?" + urllib.parse.urlencode(params, encoding='utf-8')
            return url
            
        except Exception as e:
            print(f"构建导航URL失败: {e}")
            # 回退到简单URL
            simple_url = f"https://ditu.amap.com/search?query={urllib.parse.quote(destination)}"
            return simple_url
    
    def open_navigation(self, origin: str, destination: str) -> Tuple[bool, str]:
        """打开浏览器进行导航"""
        try:
            print(f"正在构建导航链接: {origin} -> {destination}")
            
            # 构建高德地图导航URL
            nav_url = self.build_amap_url(origin, destination)
            print(f"导航URL: {nav_url}")
            
            # 打开浏览器
            success = webbrowser.open(nav_url)
            
            if success:
                return True, "浏览器导航已启动"
            else:
                return False, "无法打开浏览器"
                
        except Exception as e:
            print(f"打开导航失败: {e}")
            return False, f"导航启动失败: {str(e)}"
    
    def open_simple_search(self, location: str) -> Tuple[bool, str]:
        """打开简单的地点搜索"""
        try:
            search_url = f"https://ditu.amap.com/search?query={urllib.parse.quote(location)}"
            success = webbrowser.open(search_url)
            
            if success:
                return True, f"已打开 {location} 的搜索结果"
            else:
                return False, "无法打开浏览器"
                
        except Exception as e:
            return False, f"搜索失败: {str(e)}"
    
    def test_api_connection(self) -> bool:
        """测试高德API连接"""
        try:
            # 测试地理编码API
            test_address = "北京市天安门"
            coords = self.geocode_address(test_address)
            
            if coords:
                print("高德API连接测试成功")
                return True
            else:
                print("高德API连接测试失败")
                return False
                
        except Exception as e:
            print(f"API连接测试错误: {e}")
            return False
    
    def get_current_location(self) -> Optional[Tuple[float, float]]:
        """获取当前位置（基于IP的粗略定位）"""
        try:
            # 使用高德IP定位API
            ip_api = "https://restapi.amap.com/v3/ip"
            params = {
                'key': self.amap_api_key,
                'output': 'json'
            }
            
            response = requests.get(ip_api, params=params, timeout=5)
            data = response.json()
            
            if data['status'] == '1' and 'rectangle' in data:
                # 从矩形区域中心点获取坐标
                rectangle = data['rectangle']
                coords = rectangle.split(';')[0].split(',')
                lng, lat = map(float, coords)
                print(f"当前大致位置: ({lng}, {lat}) - {data.get('city', '未知城市')}")
                return lng, lat
            
            return None
            
        except Exception as e:
            print(f"获取当前位置失败: {e}")
            return None