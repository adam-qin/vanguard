import asyncio
import sys
import os
from speech_handler import SpeechHandler
from ai_processor import AIProcessor
from mcp_client import MCPClient

class NavigationApp:
    def __init__(self):
        self.speech_handler = SpeechHandler()
        self.ai_processor = AIProcessor()
        self.mcp_client = MCPClient()
        self.running = True
    
    async def run(self):
        """主运行循环"""
        print("=== 高德地图语音导航助手 ===")
        print("支持文字输入和语音输入")
        print("输入 'quit' 或 'exit' 退出程序")
        print("输入 'voice' 开始语音输入")
        print("输入 'mode' 切换导航模式")
        print("-" * 40)
        
        # 测试麦克风
        if not self.speech_handler.test_microphone():
            print("警告: 麦克风不可用，只能使用文字输入")
        
        # 测试导航方法并选择最佳方案
        self.mcp_client.test_navigation_methods()
        
        try:
            while self.running:
                await self.handle_user_input()
        except KeyboardInterrupt:
            print("\n程序被用户中断")
        finally:
            await self.cleanup()
    
    async def handle_user_input(self):
        """处理用户输入"""
        try:
            print("\n请输入导航需求 (或输入 'voice' 使用语音):")
            user_input = input("> ").strip()
            
            if user_input.lower() in ['quit', 'exit', '退出']:
                self.running = False
                return
            
            if user_input.lower() == 'voice':
                voice_result = await self.get_voice_input()
                if voice_result is None:
                    return
                
                user_input, trigger_reason = voice_result
                
                # 如果是超时触发且没有语音内容，提示用户输入
                if trigger_reason == "timeout" and not user_input.strip():
                    print("🔤 请手动输入导航需求:")
                    manual_input = input("> ").strip()
                    if manual_input:
                        user_input = manual_input
                    else:
                        print("未输入任何内容")
                        return
                        
                if not user_input:
                    return
                    
            elif user_input.lower() == 'mode':
                await self.switch_navigation_mode()
                return
            
            if not user_input:
                print("输入为空，请重新输入")
                return
            
            # 处理导航请求
            await self.process_navigation_request(user_input)
            
        except Exception as e:
            print(f"处理输入时出错: {e}")
    
    async def get_voice_input(self):
        """获取智能语音输入"""
        try:
            self.speech_handler.speak("请说出您的导航需求，或说'开始导航'立即处理")
            
            # 在新线程中进行语音识别，避免阻塞
            loop = asyncio.get_event_loop()
            
            # 设置超时时间（比语音识别的超时时间稍长）
            try:
                result = await asyncio.wait_for(
                    loop.run_in_executor(None, self.speech_handler.listen_for_speech),
                    timeout=25.0  # 25秒超时
                )
                
                # 解析返回结果
                if isinstance(result, tuple):
                    text, trigger_reason = result
                else:
                    text, trigger_reason = result, "unknown"
                    
            except asyncio.TimeoutError:
                print("⏰ 语音输入总超时")
                self.speech_handler.speak("语音输入超时，请重新尝试")
                return None, "timeout"
            
            # 处理不同的触发情况
            if trigger_reason == "keyword":
                print("🎯 检测到关键词，立即开始处理")
                self.speech_handler.speak("收到指令，开始处理导航")
            elif trigger_reason == "timeout":
                print("⏰ 超时自动触发，开始处理")
                self.speech_handler.speak("自动开始处理导航")
            elif trigger_reason in ["google_fallback", "google"]:
                print("🔄 使用Google语音识别")
            
            if text and len(text.strip()) > 0:
                print(f"📝 语音识别结果: {text}")
                if trigger_reason not in ["keyword", "timeout"]:
                    self.speech_handler.speak(f"您说的是: {text}")
                return text, trigger_reason
            else:
                if trigger_reason == "timeout":
                    print("🔇 超时期间未检测到语音，但仍然开始处理")
                    self.speech_handler.speak("未检测到具体需求，请稍后手动输入")
                    return "", trigger_reason  # 返回空字符串，让用户后续手动输入
                else:
                    self.speech_handler.speak("没有听清楚，请重新输入")
                    return None, "no_speech"
                
        except Exception as e:
            print(f"语音输入错误: {e}")
            self.speech_handler.speak("语音输入出现错误")
            return None, "error"
    
    async def process_navigation_request(self, user_input):
        """处理导航请求"""
        try:
            print(f"正在处理: {user_input}")
            
            # 使用AI处理用户输入
            result = self.ai_processor.process_navigation_request(user_input)
            
            if "error" in result:
                error_msg = result["error"]
                print(f"处理失败: {error_msg}")
                self.speech_handler.speak(error_msg)
                return
            
            origin = result.get("origin", "")
            destination = result.get("destination", "")
            
            # 验证地址
            is_valid, message = self.ai_processor.validate_addresses(origin, destination)
            if not is_valid:
                print(f"地址验证失败: {message}")
                self.speech_handler.speak(message)
                return
            
            print(f"起点: {origin}")
            print(f"终点: {destination}")
            
            # 语音确认导航
            confirmed = await self.voice_confirm_navigation(origin, destination)
            if not confirmed:
                print("导航已取消")
                self.speech_handler.speak("导航已取消")
                return
            
            # 调用高德MCP服务器进行导航
            success, message = self.mcp_client.navigate_to_destination(origin, destination)
            
            if success:
                success_msg = f"导航成功启动: {message}"
                print(success_msg)
                self.speech_handler.speak("导航已启动，请查看高德地图")
            else:
                error_msg = f"导航启动失败: {message}"
                print(error_msg)
                self.speech_handler.speak("导航启动失败，请检查网络连接")
                
        except Exception as e:
            error_msg = f"处理导航请求时出错: {e}"
            print(error_msg)
            self.speech_handler.speak("处理请求时出现错误")
    
    async def voice_confirm_navigation(self, origin, destination):
        """语音确认导航"""
        try:
            # 语音播报确认信息（同步播放，确保播报完成）
            confirm_msg = f"即将导航从{origin}到{destination}，是否确认？"
            print(confirm_msg)
            
            print("🔊 正在播报确认信息...")
            self.speech_handler.speak(confirm_msg)  # 同步播放，会等待播报完成
            
            # 播报完成后显示提示
            print("🎤 请说出确认指令:")
            print("   ✅ 确认: '确认'、'好的'、'开始导航'、'走吧'")
            print("   ❌ 取消: '取消'、'不要'、'算了'")
            print("   ⏰ 10秒内无响应将提供手动选择")
            
            # 给用户1秒时间看提示
            import time
            time.sleep(1)
            
            # 在新线程中进行语音识别
            loop = asyncio.get_event_loop()
            
            try:
                result = await asyncio.wait_for(
                    loop.run_in_executor(None, self.get_voice_confirmation),
                    timeout=10.0  # 减少到10秒超时
                )
                
                if isinstance(result, tuple):
                    confirmation_text, trigger_reason = result
                else:
                    confirmation_text, trigger_reason = result, "unknown"
                    
            except asyncio.TimeoutError:
                print("⏰ 语音确认超时，提供手动选项")
                self.speech_handler.speak("语音确认超时，请手动选择")
                
                manual_confirm = input("请输入 Y 确认导航或 N 取消: ").strip().lower()
                if manual_confirm in ['y', 'yes', '确认', '好的', '1']:
                    print("✅ 手动确认导航")
                    self.speech_handler.speak("收到确认，开始导航")
                    return True
                else:
                    print("❌ 手动取消导航")
                    self.speech_handler.speak("导航已取消")
                    return False
            
            if confirmation_text:
                print(f"📝 确认语音: {confirmation_text}")
                
                # 检查确认关键词
                confirmation_keywords = ['确认', '好的', '是的', '开始导航', '开始', '导航', '走吧', '出发', 'yes', 'ok', '对', '嗯']
                cancel_keywords = ['取消', '不要', '不用', '算了', 'no', '不', '不是', '不对']
                
                confirmation_lower = confirmation_text.lower().replace(' ', '')
                
                # 检查取消关键词（优先级更高）
                for cancel_word in cancel_keywords:
                    if cancel_word in confirmation_lower:
                        print("❌ 检测到取消指令")
                        self.speech_handler.speak("收到取消指令")
                        return False
                
                # 检查确认关键词
                for confirm_word in confirmation_keywords:
                    if confirm_word in confirmation_lower:
                        print("✅ 检测到确认指令")
                        self.speech_handler.speak("收到确认指令，开始导航")
                        return True
                
                # 如果没有明确的关键词，询问用户
                print("🤔 未识别明确指令，请手动确认")
                self.speech_handler.speak("未识别明确指令，请按Y确认或N取消")
                
                manual_confirm = input("请输入 Y 确认或 N 取消: ").strip().lower()
                if manual_confirm in ['y', 'yes', '确认', '好的']:
                    return True
                else:
                    return False
            else:
                print("🔇 未检测到语音，请手动确认")
                self.speech_handler.speak("未检测到语音，请按Y确认或N取消")
                
                manual_confirm = input("请输入 Y 确认或 N 取消: ").strip().lower()
                return manual_confirm in ['y', 'yes', '确认', '好的']
                
        except Exception as e:
            print(f"语音确认过程出错: {e}")
            self.speech_handler.speak("确认过程出现错误，请手动确认")
            
            manual_confirm = input("请输入 Y 确认或 N 取消: ").strip().lower()
            return manual_confirm in ['y', 'yes', '确认', '好的']
    
    def get_voice_confirmation(self):
        """获取语音确认"""
        try:
            print("🎤 开始语音确认...")
            
            # 只使用科大讯飞进行确认
            if self.speech_handler.use_xfyun and self.speech_handler.xfyun_asr:
                print("🎤 使用科大讯飞进行语音确认...")
                
                # 为确认设置特殊的关键词
                original_keywords = self.speech_handler.xfyun_asr.trigger_keywords
                self.speech_handler.xfyun_asr.trigger_keywords = [
                    '确认', '好的', '开始导航', '开始', '导航', '走吧', '出发',
                    '取消', '不要', '不用', '算了'
                ]
                
                try:
                    # 使用智能触发进行确认，等待时间短一些
                    result = self.speech_handler.xfyun_asr.recognize_speech_with_smart_trigger(max_wait_time=8)
                    
                    if result and isinstance(result, tuple):
                        text, reason = result
                        if text and len(text.strip()) > 0:
                            print(f"✅ 科大讯飞确认结果: {text}")
                            return result
                    
                    print("🔇 科大讯飞未获得确认结果")
                    return None, "no_speech"
                    
                except Exception as xf_error:
                    print(f"❌ 科大讯飞确认失败: {xf_error}")
                    return None, "error"
                finally:
                    # 恢复原始关键词
                    self.speech_handler.xfyun_asr.trigger_keywords = original_keywords
            else:
                print("❌ 科大讯飞不可用")
                return None, "no_xfyun"
                
        except Exception as e:
            print(f"❌ 获取语音确认失败: {e}")
            return None, "error"
    
    async def switch_navigation_mode(self):
        """切换导航模式"""
        try:
            # 获取导航信息
            nav_info = self.mcp_client.get_navigation_info()
            
            print(f"=== 导航模式配置 ===")
            print(f"当前模式: {nav_info['current_mode']}")
            print(f"高德MCP可用: {'是' if nav_info['mcp_available'] else '否'}")
            print(f"浏览器导航可用: {'是' if nav_info['browser_available'] else '否'}")
            print(f"高德API密钥: {'已配置' if nav_info['amap_key_configured'] else '未配置'}")
            
            print("\n请选择导航模式:")
            print("1. 浏览器导航 (兼容性好)")
            print("2. 高德MCP服务器导航 (功能丰富)")
            
            choice = input("请输入选择 (1-2): ").strip()
            
            if choice == '1':
                self.mcp_client.set_navigation_mode(True)
                print("✅ 已切换到浏览器导航模式")
                self.speech_handler.speak("已切换到浏览器导航模式")
            elif choice == '2':
                if nav_info['mcp_available']:
                    self.mcp_client.set_navigation_mode(False)
                    print("✅ 已切换到高德MCP服务器导航模式")
                    self.speech_handler.speak("已切换到高德MCP服务器导航模式")
                else:
                    print("❌ 高德MCP服务器不可用，请检查API密钥配置")
                    self.speech_handler.speak("高德MCP服务器不可用，请检查配置")
            else:
                print("❌ 无效选择")
                self.speech_handler.speak("无效选择")
                
        except Exception as e:
            print(f"❌ 切换导航模式时出错: {e}")
            self.speech_handler.speak("切换导航模式失败")
    
    def cleanup(self):
        """清理资源"""
        print("正在清理资源...")
        # 高德MCP服务器是HTTP API，无需停止进程
        if hasattr(self.speech_handler, 'cleanup'):
            self.speech_handler.cleanup()
        print("程序已退出")

def check_dependencies():
    """检查依赖项"""
    required_modules = [
        'speech_recognition',
        'win32com.client',  # Windows SAPI
        'edge_tts',         # Edge TTS
        'pygame',           # 音频播放
        'dashscope',
        'requests'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print("缺少以下依赖项:")
        for module in missing_modules:
            print(f"  - {module}")
        print("\n请运行以下命令安装依赖:")
        print("pip install -r requirements.txt")
        return False
    
    return True

def check_environment():
    """检查环境变量"""
    required_vars = ['DASHSCOPE_API_KEY', 'AMAP_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("缺少以下环境变量:")
        for var in missing_vars:
            print(f"  - {var}")
        print("\n请设置这些环境变量后重新运行程序")
        return False
    
    return True

async def main():
    """主函数"""
    print("正在启动高德地图语音导航助手...")
    
    # 检查依赖项
    if not check_dependencies():
        return
    
    # 检查环境变量
    if not check_environment():
        return
    
    # 启动应用
    app = NavigationApp()
    await app.run()

if __name__ == "__main__":
    asyncio.run(main())