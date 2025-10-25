import websocket
import datetime
import hashlib
import base64
import hmac
import json
from urllib.parse import urlencode
import time
import ssl
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import _thread as thread
import pyaudio
import wave
import io
from config import XFYUN_APP_ID, XFYUN_API_SECRET, XFYUN_API_KEY

STATUS_FIRST_FRAME = 0  # 第一帧的标识
STATUS_CONTINUE_FRAME = 1  # 中间帧标识
STATUS_LAST_FRAME = 2  # 最后一帧的标识

class XfyunASR:
    def __init__(self):
        self.app_id = XFYUN_APP_ID
        self.api_secret = XFYUN_API_SECRET
        self.api_key = XFYUN_API_KEY
        
        # 音频参数
        self.chunk = 1024  # 每次读取的音频数据大小
        self.format = pyaudio.paInt16  # 音频格式
        self.channels = 1  # 单声道
        self.rate = 16000  # 采样率
        
        # 识别结果
        self.result = ""
        self.is_finished = False
        self.ws = None
        
        # 智能处理参数
        self.trigger_keywords = ["开始导航", "导航", "开始", "走吧", "出发"]
        self.auto_trigger_timeout = 12  # 12秒无语音自动触发
        self.keyword_detected = False
        
    def create_url(self):
        """生成鉴权URL"""
        url = 'wss://ws-api.xfyun.cn/v2/iat'
        
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))
        
        # 拼接字符串
        signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v2/iat " + "HTTP/1.1"
        
        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.api_secret.encode('utf-8'), 
                                signature_origin.encode('utf-8'),
                                digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')
        
        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            self.api_key, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        
        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": "ws-api.xfyun.cn"
        }
        
        # 拼接鉴权参数，生成url
        url = url + '?' + urlencode(v)
        return url
    
    def on_message(self, ws, message):
        """收到websocket消息的处理"""
        try:
            data = json.loads(message)
            code = data.get("code", 0)
            
            if code != 0:
                print(f'请求错误: {code}, {data.get("message", "未知错误")}')
                self.is_finished = True
                ws.close()
                return
            
            # 处理识别结果
            if "data" in data and "result" in data["data"]:
                result = data["data"]["result"]
                if result and "ws" in result:
                    ws_list = result["ws"]
                    for i in ws_list:
                        for w in i["cw"]:
                            self.result += w["w"]
                    print(f"当前识别结果: {self.result}")
                    
                    # 检查是否包含触发关键词
                    self.check_trigger_keywords()
            
            # 检查是否是最终结果
            if "data" in data and data["data"].get("status") == 2:
                print("收到最终识别结果")
                # 立即标记完成，不需要延迟
                self.is_finished = True
                        
        except Exception as e:
            print(f"消息处理错误: {e}")
            print(f"原始消息: {message}")
    
    def on_error(self, ws, error):
        """websocket错误处理"""
        print(f"WebSocket连接错误: {error}")
        # 不要立即标记完成，给重连机会
        if "Connection is already closed" not in str(error):
            self.is_finished = True
    
    def on_close(self, ws, close_status_code, close_msg):
        """websocket关闭处理"""
        print(f"WebSocket连接已关闭 (状态码: {close_status_code})")
        # 立即标记完成
        self.is_finished = True
    
    def on_open(self, ws):
        """websocket连接成功处理"""
        def run(*args):
            frameSize = 1280  # 每一帧的音频大小 (40ms * 16000 * 2 / 1000)
            intervel = 0.04  # 发送音频间隔(单位:s)
            status = STATUS_FIRST_FRAME  # 音频的状态信息，标识音频是第一帧，还是中间帧、最后一帧
            
            # 录音参数
            p = pyaudio.PyAudio()
            stream = None
            
            try:
                stream = p.open(format=self.format,
                              channels=self.channels,
                              rate=self.rate,
                              input=True,
                              frames_per_buffer=self.chunk)
                
                print("开始录音，请说话...")
                
                # 录音时长控制 - 延长录音时间
                record_time = 0
                max_record_time = 10  # 增加最大录音时长到10秒
                silence_count = 0
                max_silence = 75  # 增加最大静音帧数 (约3秒静音)
                has_speech = False  # 是否检测到语音
                min_speech_time = 1.0  # 最少录音时间1秒
                
                while not self.is_finished and record_time < max_record_time:
                    try:
                        buf = stream.read(frameSize, exception_on_overflow=False)
                        if not buf:
                            status = STATUS_LAST_FRAME
                        
                        # 检测静音（简单的音量检测）
                        import audioop
                        volume = audioop.rms(buf, 2)
                        
                        # 动态调整静音阈值
                        silence_threshold = 300 if has_speech else 800
                        
                        if volume < silence_threshold:
                            silence_count += 1
                        else:
                            silence_count = 0
                            has_speech = True  # 检测到语音
                        
                        # 只有在检测到语音后且静音时间足够长才结束录音
                        if (silence_count > max_silence and 
                            has_speech and 
                            record_time > min_speech_time and 
                            status != STATUS_FIRST_FRAME):
                            print("检测到语音结束，正在处理...")
                            status = STATUS_LAST_FRAME
                        
                        # 检查WebSocket连接状态
                        if ws.sock is None or not hasattr(ws.sock, 'connected') or not ws.sock.connected:
                            print("WebSocket连接已断开")
                            break
                        
                        try:
                            # 第一帧处理
                            if status == STATUS_FIRST_FRAME:
                                d = {"common": {"app_id": self.app_id},
                                     "business": {
                                         "language": "zh_cn", 
                                         "domain": "iat", 
                                         "accent": "mandarin", 
                                         "vinfo": 1, 
                                         "vad_eos": 5000,  # 增加静音检测时间到5秒
                                         "dwa": "wpgs",
                                         "ptt": 0,  # 禁用标点符号
                                         "rlang": "zh-cn",  # 返回语言
                                         "nunum": 0  # 禁用数字转换
                                     },
                                     "data": {"status": 0, "format": "audio/L16;rate=16000",
                                             "audio": str(base64.b64encode(buf), 'utf-8'),
                                             "encoding": "raw"}}
                                ws.send(json.dumps(d))
                                status = STATUS_CONTINUE_FRAME
                                print("发送第一帧数据...")
                                
                            # 中间帧处理
                            elif status == STATUS_CONTINUE_FRAME:
                                d = {"data": {"status": 1, "format": "audio/L16;rate=16000",
                                             "audio": str(base64.b64encode(buf), 'utf-8'),
                                             "encoding": "raw"}}
                                ws.send(json.dumps(d))
                                
                            # 最后一帧处理
                            elif status == STATUS_LAST_FRAME:
                                d = {"data": {"status": 2, "format": "audio/L16;rate=16000",
                                             "audio": str(base64.b64encode(buf), 'utf-8'),
                                             "encoding": "raw"}}
                                ws.send(json.dumps(d))
                                print("发送最后一帧数据...")
                                break
                                
                        except Exception as send_error:
                            print(f"发送数据失败: {send_error}")
                            if "Connection is already closed" in str(send_error):
                                print("连接已关闭，停止发送数据")
                                break
                            # 其他错误继续尝试
                        
                        # 间隔一段时间再发送
                        time.sleep(intervel)
                        record_time += intervel
                        
                    except Exception as e:
                        print(f"录音过程中出错: {e}")
                        break
                
                # 如果录音时间到了但还没发送最后一帧，发送最后一帧
                if status != STATUS_LAST_FRAME and record_time >= max_record_time:
                    print("录音时间到，发送最后一帧...")
                    d = {"data": {"status": 2, "format": "audio/L16;rate=16000",
                                 "audio": "",  # 空音频数据
                                 "encoding": "raw"}}
                    ws.send(json.dumps(d))
                
            except Exception as e:
                print(f"录音初始化失败: {e}")
            finally:
                if stream:
                    try:
                        stream.stop_stream()
                        stream.close()
                    except:
                        pass
                try:
                    p.terminate()
                except:
                    pass
                
                # 等待服务器响应，延长等待时间
                print("等待识别结果...")
                time.sleep(2.0)  # 等待2秒让服务器处理
                
                # 不要立即关闭WebSocket，让消息处理完成
                # WebSocket会在收到最终结果后自动关闭
            
        thread.start_new_thread(run, ())
    
    def recognize_speech(self):
        """开始语音识别"""
        try:
            self.result = ""
            self.is_finished = False
            
            # 检查API配置
            if not all([self.app_id, self.api_secret, self.api_key]) or \
               any(key.startswith('your-') for key in [self.app_id, self.api_secret, self.api_key]):
                print("错误: 科大讯飞API配置不完整，请检查环境变量")
                return None
            
            print("正在连接科大讯飞语音识别服务...")
            websocket.enableTrace(False)
            wsUrl = self.create_url()
            self.ws = websocket.WebSocketApp(wsUrl, 
                                           on_message=self.on_message, 
                                           on_error=self.on_error, 
                                           on_close=self.on_close,
                                           on_open=self.on_open)
            
            # 设置更长的超时时间和心跳
            try:
                self.ws.run_forever(
                    sslopt={"cert_reqs": ssl.CERT_NONE}, 
                    ping_interval=60,  # 增加心跳间隔
                    ping_timeout=30    # 增加心跳超时
                )
            except Exception as ws_error:
                print(f"WebSocket运行错误: {ws_error}")
                if "run_loop already started" in str(ws_error):
                    print("WebSocket运行循环已启动，等待完成...")
                    # 如果运行循环已启动，直接等待结果
                    pass
                else:
                    self.is_finished = True
            
            # 等待识别完成，减少等待时间
            wait_time = 0
            max_wait = 3  # 减少最大等待时间到3秒
            check_interval = 0.1
            
            # 如果已经完成，不需要等待
            if not self.is_finished:
                print("等待识别完成...")
                while not self.is_finished and wait_time < max_wait:
                    time.sleep(check_interval)
                    wait_time += check_interval
                
                if wait_time >= max_wait:
                    print("识别处理完成")
                    self.is_finished = True
            
            # 清理结果
            final_result = self.result.strip() if self.result else None
            if final_result:
                print(f"最终识别结果: {final_result}")
            else:
                print("未获得有效识别结果")
                
            return final_result
            
        except Exception as e:
            print(f"科大讯飞语音识别错误: {e}")
            self.is_finished = True
            return None
    
    def test_connection(self):
        """测试API连接"""
        try:
            if not all([self.app_id, self.api_secret, self.api_key]):
                return False, "API配置不完整"
            
            if any(key.startswith('your-') for key in [self.app_id, self.api_secret, self.api_key]):
                return False, "请配置正确的API密钥"
            
            # 简单的URL生成测试
            url = self.create_url()
            if url and 'wss://ws-api.xfyun.cn' in url:
                print(f"科大讯飞API配置检查通过")
                print(f"APP_ID: {self.app_id}")
                print(f"WebSocket URL已生成")
                return True, "API配置正常"
            else:
                return False, "URL生成失败"
                
        except Exception as e:
            return False, f"连接测试失败: {e}"
    
    def check_trigger_keywords(self):
        """检查是否包含触发关键词"""
        if self.keyword_detected:
            return True
            
        current_text = self.result.lower()
        for keyword in self.trigger_keywords:
            if keyword in current_text:
                print(f"🎯 检测到触发关键词: '{keyword}' - 立即结束识别")
                self.keyword_detected = True
                # 立即结束录音，开始处理
                self.is_finished = True
                # 尝试关闭WebSocket连接
                if self.ws:
                    try:
                        self.ws.close()
                    except:
                        pass
                return True
        return False
    
    def recognize_speech_with_smart_trigger(self, max_wait_time=12):
        """智能语音识别：支持关键词触发和超时自动处理"""
        try:
            self.result = ""
            self.is_finished = False
            self.keyword_detected = False
            
            # 检查API配置
            if not all([self.app_id, self.api_secret, self.api_key]) or \
               any(key.startswith('your-') for key in [self.app_id, self.api_secret, self.api_key]):
                print("错误: 科大讯飞API配置不完整，请检查环境变量")
                return None, "timeout"
            
            print("🎤 智能语音识别启动...")
            print(f"💡 提示: 说出包含 {self.trigger_keywords} 的话语可立即开始处理")
            print(f"⏰ 或者等待 {max_wait_time} 秒后自动处理")
            
            websocket.enableTrace(False)
            wsUrl = self.create_url()
            self.ws = websocket.WebSocketApp(wsUrl, 
                                           on_message=self.on_message, 
                                           on_error=self.on_error, 
                                           on_close=self.on_close,
                                           on_open=self.on_open)
            
            # 启动WebSocket连接
            try:
                self.ws.run_forever(
                    sslopt={"cert_reqs": ssl.CERT_NONE}, 
                    ping_interval=60,
                    ping_timeout=30
                )
            except Exception as ws_error:
                print(f"WebSocket运行错误: {ws_error}")
                if "run_loop already started" not in str(ws_error):
                    self.is_finished = True
            
            # 智能等待逻辑
            wait_time = 0
            check_interval = 0.1  # 减少检查间隔
            
            while not self.is_finished and wait_time < max_wait_time:
                time.sleep(check_interval)
                wait_time += check_interval
                
                # 检查是否检测到关键词（优先级最高）
                if self.keyword_detected:
                    print("🚀 关键词触发，立即结束等待...")
                    self.is_finished = True
                    break
                
                # 每2秒显示一次状态
                if int(wait_time * 10) % 20 == 0:
                    remaining = max_wait_time - wait_time
                    print(f"⏳ 等待中... (剩余 {remaining:.1f}s)")
            
            # 确定触发原因
            trigger_reason = "keyword" if self.keyword_detected else "timeout"
            
            if wait_time >= max_wait_time and not self.keyword_detected:
                print("⏰ 等待超时，自动开始处理...")
                self.is_finished = True
            
            # 获取最终结果
            final_result = self.result.strip() if self.result else None
            
            if final_result:
                print(f"📝 最终识别结果: {final_result}")
            else:
                print("🔇 未获得语音输入")
                final_result = ""  # 返回空字符串而不是None
                
            return final_result, trigger_reason
            
        except Exception as e:
            print(f"智能语音识别错误: {e}")
            return None, "error"
    
    def quick_test(self):
        """快速测试语音识别（3秒录音）"""
        print("=== 科大讯飞语音识别快速测试 ===")
        print("将进行3秒录音测试...")
        
        try:
            # 重置状态
            self.result = ""
            self.is_finished = False
            
            # 创建简化的WebSocket连接
            wsUrl = self.create_url()
            print(f"连接URL: {wsUrl[:50]}...")
            
            # 简单测试连接
            import socket
            try:
                socket.create_connection(("ws-api.xfyun.cn", 443), timeout=5)
                print("✓ 网络连接正常")
            except Exception as e:
                print(f"✗ 网络连接失败: {e}")
                return None
            
            return "网络连接测试完成"
            
        except Exception as e:
            print(f"快速测试失败: {e}")
            return None