import json
import requests
import webbrowser
import urllib.parse
import os
from typing import Dict, Any, Optional, Tuple

class QiniuMCPClient:
    """基于七牛云高德MCP SERVER的导航客户端"""
    
    def __init__(self):
        # 七牛云MCP SERVER配置
        self.openai_base_url = os.getenv('OPENAI_BASE_URL', '').rstrip('/')
        self.openai_api_key = os.getenv('OPENAI_API_KEY', '')
        self.model = os.getenv('MCP_MODEL', 'deepseek-v3-tool')
        self.use_qiniu_mcp = os.getenv('USE_QINIU_MCP', 'true').lower() == 'true'
        
        # 请求配置
        self.timeout = 15  # 正常请求超时时间
        self.test_timeout = 5  # 测试连接超时时间
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.openai_api_key}'
        }
        
        # 打印配置信息（隐藏敏感信息）
        if self.openai_base_url and self.openai_api_key:
            masked_key = self.openai_api_key[:8] + '...' + self.openai_api_key[-4:] if len(self.openai_api_key) > 12 else '***'
            print(f"🔧 七牛云MCP配置:")
            print(f"   服务地址: {self.openai_base_url}")
            print(f"   API密钥: {masked_key}")
            print(f"   模型: {self.model}")
            print(f"   启用状态: {self.use_qiniu_mcp}")
        else:
            print("⚠️ 七牛云MCP配置不完整")
    
    def test_mcp_connection(self) -> bool:
        """测试七牛云MCP SERVER连接"""
        try:
            if not self.openai_base_url or not self.openai_api_key:
                print("❌ 未配置七牛云MCP SERVER环境变量")
                print("   需要设置: OPENAI_BASE_URL 和 OPENAI_API_KEY")
                return False
            
            print("🔍 测试七牛云MCP SERVER连接...")
            
            # 使用简单的连接测试
            test_payload = {
                "messages": [
                    {
                        "role": "user", 
                        "content": "test"
                    }
                ],
                "model": self.model,
                "max_tokens": 1  # 限制响应长度以加快测试
            }
            
            response = requests.post(
                f"{self.openai_base_url}/v1/chat/completions",
                headers=self.headers,
                json=test_payload,
                timeout=self.test_timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    print("✅ 七牛云MCP SERVER连接成功")
                    return True
                else:
                    print("❌ 七牛云MCP SERVER响应格式异常")
                    return False
            else:
                print(f"❌ 七牛云MCP SERVER响应异常: {response.status_code}")
                print(f"   响应内容: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ 七牛云MCP SERVER连接失败: {e}")
            return False
    
    def get_coordinates_from_mcp(self, origin: str, destination: str) -> Tuple[Optional[str], Optional[str]]:
        """通过七牛云MCP SERVER获取起点和终点坐标"""
        try:
            print(f"🌐 调用七牛云MCP SERVER获取坐标...")
            print(f"   起点: {origin}")
            print(f"   终点: {destination}")
            
            # 构建请求内容
            content = f"从{origin}导航到{destination},给出源地址和目标地址的坐标"
            
            payload = {
                "messages": [
                    {
                        "role": "user",
                        "content": content
                    }
                ],
                "model": self.model
            }
            
            # 发送请求到七牛云MCP SERVER
            response = requests.post(
                f"{self.openai_base_url}/v1/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code != 200:
                print(f"❌ MCP SERVER请求失败: {response.status_code}")
                print(f"   响应内容: {response.text}")
                return None, None
            
            result = response.json()
            
            # 解析响应
            if 'choices' not in result or len(result['choices']) == 0:
                print("❌ MCP SERVER响应格式异常")
                return None, None
            
            choice = result['choices'][0]
            message = choice.get('message', {})
            
            # 提取坐标信息
            origin_coords = None
            dest_coords = None
            
            # 从tool_references中提取坐标
            if 'tool_references' in result:
                print(f"   📋 找到 {len(result['tool_references'])} 个工具调用结果")
                for i, tool_ref in enumerate(result['tool_references']):
                    try:
                        print(f"   🔍 解析工具调用 {i+1}...")
                        content_data = json.loads(tool_ref['content'])
                        if 'content' in content_data:
                            for content_item in content_data['content']:
                                if content_item['type'] == 'text':
                                    tool_result = json.loads(content_item['text'])
                                    if 'return' in tool_result and len(tool_result['return']) > 0:
                                        location = tool_result['return'][0].get('location', '')
                                        if location:
                                            # 根据工具调用的顺序分配坐标
                                            if origin_coords is None:
                                                origin_coords = location
                                                print(f"   ✅ 起点坐标: {origin_coords}")
                                            elif dest_coords is None:
                                                dest_coords = location
                                                print(f"   ✅ 终点坐标: {dest_coords}")
                                        else:
                                            print(f"   ⚠️ 工具调用 {i+1} 未返回location字段")
                                    else:
                                        print(f"   ⚠️ 工具调用 {i+1} 未返回有效的return数据")
                    except (json.JSONDecodeError, KeyError) as e:
                        print(f"   ⚠️ 解析工具结果 {i+1} 时出错: {e}")
                        # 打印原始数据用于调试
                        print(f"   📄 原始数据: {tool_ref.get('content', 'N/A')[:200]}...")
                        continue
            
            # 如果没有从tool_references获取到坐标，尝试从消息内容中提取
            if not origin_coords or not dest_coords:
                content_text = message.get('content', '')
                print(f"   📝 MCP响应内容: {content_text}")
                
                # 使用多种正则表达式模式提取坐标
                import re
                
                # 模式1: 标准坐标格式 (经度,纬度)
                coord_pattern1 = r'(\d+\.\d+,\d+\.\d+)'
                coords1 = re.findall(coord_pattern1, content_text)
                
                # 模式2: 带反引号的坐标格式
                coord_pattern2 = r'`(\d+\.\d+,\d+\.\d+)`'
                coords2 = re.findall(coord_pattern2, content_text)
                
                # 模式3: 分别提取经纬度
                lng_pattern = r'经度[：:]\s*(\d+\.\d+)'
                lat_pattern = r'纬度[：:]\s*(\d+\.\d+)'
                lngs = re.findall(lng_pattern, content_text)
                lats = re.findall(lat_pattern, content_text)
                
                # 优先使用带反引号的坐标
                coords = coords2 if coords2 else coords1
                
                # 如果找到分离的经纬度，组合成坐标
                if not coords and len(lngs) >= 2 and len(lats) >= 2:
                    coords = [f"{lngs[0]},{lats[0]}", f"{lngs[1]},{lats[1]}"]
                
                print(f"   🔍 提取到 {len(coords)} 个坐标: {coords}")
                
                if len(coords) >= 2:
                    if not origin_coords:
                        origin_coords = coords[0]
                        print(f"   ✅ 从内容提取起点坐标: {origin_coords}")
                    if not dest_coords:
                        dest_coords = coords[1]
                        print(f"   ✅ 从内容提取终点坐标: {dest_coords}")
                elif len(coords) == 1:
                    if not origin_coords:
                        origin_coords = coords[0]
                        print(f"   ✅ 从内容提取起点坐标: {origin_coords}")
                    elif not dest_coords:
                        dest_coords = coords[0]
                        print(f"   ✅ 从内容提取终点坐标: {dest_coords}")
                else:
                    print(f"   ⚠️ 未能从响应内容中提取坐标")
            
            if origin_coords and dest_coords:
                print("✅ 成功获取坐标信息")
                return origin_coords, dest_coords
            else:
                print("❌ 未能获取完整的坐标信息")
                return None, None
                
        except requests.exceptions.Timeout:
            print("❌ MCP SERVER请求超时")
            return None, None
        except requests.exceptions.RequestException as e:
            print(f"❌ MCP SERVER网络请求错误: {e}")
            return None, None
        except Exception as e:
            print(f"❌ MCP SERVER调用异常: {e}")
            return None, None
    
    def build_amap_navigation_url(self, origin_coords: str, dest_coords: str, 
                                 origin_name: str = "", dest_name: str = "") -> str:
        """构建高德地图导航URL"""
        try:
            print("🔗 构建高德地图导航URL...")
            
            # 高德地图导航URL基础地址
            base_url = "https://uri.amap.com/navigation"
            
            # 构建参数
            params = {
                'to': dest_coords,
                'mode': 'car',  # 驾车导航
                'policy': '1',  # 推荐路线
                'src': 'myapp'
            }
            
            # 添加起点坐标
            if origin_coords:
                params['from'] = origin_coords
            
            # 添加地点名称
            if dest_name:
                params['toname'] = dest_name
            if origin_name:
                params['fromname'] = origin_name
            
            # 构建完整URL
            url = f"{base_url}?" + urllib.parse.urlencode(params, encoding='utf-8')
            
            print(f"   📍 起点坐标: {origin_coords}")
            print(f"   📍 终点坐标: {dest_coords}")
            print(f"   🔗 导航URL: {url}")
            
            return url
            
        except Exception as e:
            print(f"❌ 构建导航URL失败: {e}")
            # 回退到简单搜索URL
            if dest_name:
                fallback_url = f"https://ditu.amap.com/search?query={urllib.parse.quote(dest_name)}"
                print(f"   🔄 使用回退URL: {fallback_url}")
                return fallback_url
            return ""
    
    def navigate_to_destination(self, origin: str, destination: str) -> Tuple[bool, str]:
        """执行导航功能"""
        try:
            print(f"🗺️ 开始导航: {origin} -> {destination}")
            
            # 1. 通过七牛云MCP SERVER获取坐标
            origin_coords, dest_coords = self.get_coordinates_from_mcp(origin, destination)
            
            if not origin_coords or not dest_coords:
                error_msg = "无法获取地址坐标，请检查地址是否正确"
                print(f"❌ {error_msg}")
                return False, error_msg
            
            # 2. 构建高德地图导航URL
            nav_url = self.build_amap_navigation_url(
                origin_coords, dest_coords, origin, destination
            )
            
            if not nav_url:
                error_msg = "构建导航URL失败"
                print(f"❌ {error_msg}")
                return False, error_msg
            
            # 3. 打开浏览器进行导航
            print("🌐 打开浏览器导航...")
            success = webbrowser.open(nav_url)
            
            if success:
                success_msg = f"导航成功启动，从 {origin}({origin_coords}) 到 {destination}({dest_coords})"
                print(f"✅ {success_msg}")
                return True, success_msg
            else:
                error_msg = "无法打开浏览器"
                print(f"❌ {error_msg}")
                return False, error_msg
                
        except Exception as e:
            error_msg = f"导航执行失败: {e}"
            print(f"❌ {error_msg}")
            return False, error_msg
    
    def search_location(self, address: str) -> Tuple[bool, str]:
        """搜索地址位置"""
        try:
            print(f"🔍 搜索地址: {address}")
            
            # 通过MCP SERVER获取地址坐标
            coords, _ = self.get_coordinates_from_mcp(address, address)
            
            if coords:
                # 构建高德地图标记URL
                marker_url = f"https://uri.amap.com/marker?position={coords}&name={urllib.parse.quote(address)}"
                
                print(f"🌐 打开地址搜索结果...")
                success = webbrowser.open(marker_url)
                
                if success:
                    success_msg = f"地址搜索成功: {address}({coords})"
                    print(f"✅ {success_msg}")
                    return True, success_msg
                else:
                    error_msg = "无法打开浏览器"
                    print(f"❌ {error_msg}")
                    return False, error_msg
            else:
                error_msg = f"未找到地址: {address}"
                print(f"❌ {error_msg}")
                return False, error_msg
                
        except Exception as e:
            error_msg = f"地址搜索失败: {e}"
            print(f"❌ {error_msg}")
            return False, error_msg
    
    def get_client_info(self) -> Dict[str, Any]:
        """获取客户端配置信息"""
        # 测试连接状态
        mcp_available = False
        try:
            mcp_available = self.test_mcp_connection()
        except Exception as e:
            print(f"⚠️ 测试MCP连接时出错: {e}")
        
        return {
            "mcp_available": mcp_available,
            "openai_base_url": self.openai_base_url if self.openai_base_url else "未配置",
            "api_key_configured": bool(self.openai_api_key),
            "model": self.model,
            "client_type": "七牛云MCP CLIENT"
        }