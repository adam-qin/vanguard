import speech_recognition as sr
import threading
from config import SPEECH_RECOGNITION_LANGUAGE, SPEECH_TIMEOUT, USE_XFYUN_ASR
from xfyun_asr import XfyunASR
from tts_engine import TTSEngine

class SpeechHandler:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # 使用优化后的TTS引擎
        self.tts_engine = TTSEngine()
        
        # 初始化科大讯飞ASR
        self.xfyun_asr = XfyunASR() if USE_XFYUN_ASR else None
        self.use_xfyun = USE_XFYUN_ASR
        
        # 调整麦克风（仅在使用Google ASR时需要）
        if not self.use_xfyun:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
        
        print(f"🔊 {self.tts_engine.get_engine_info()}")
    
    def listen_for_speech(self):
        """监听语音输入"""
        if self.use_xfyun and self.xfyun_asr:
            result = self._listen_with_xfyun()
            # 如果返回的是元组（包含触发原因），直接返回
            if isinstance(result, tuple):
                return result
            else:
                return result, "unknown"
        else:
            result = self._listen_with_google()
            return result, "google" if result else "no_speech"
    
    def _listen_with_xfyun(self):
        """使用科大讯飞语音识别"""
        try:
            print("使用科大讯飞智能语音识别...")
            text, trigger_reason = self.xfyun_asr.recognize_speech_with_smart_trigger()
            
            if trigger_reason == "keyword":
                print("🎯 关键词触发模式")
            elif trigger_reason == "timeout":
                print("⏰ 超时自动触发模式")
            elif trigger_reason == "error":
                print("❌ 识别出错，切换到Google语音识别...")
                return self._listen_with_google()
            
            if text and len(text.strip()) > 0:
                print(f"✅ 识别结果: {text}")
                return text, trigger_reason
            else:
                print("🔇 未识别到语音内容，切换到Google语音识别...")
                google_result = self._listen_with_google()
                return google_result, "google_fallback" if google_result else "no_speech"
                
        except Exception as e:
            print(f"科大讯飞语音识别错误: {e}")
            print("自动切换到Google语音识别...")
            google_result = self._listen_with_google()
            return google_result, "google_fallback" if google_result else "error"
    
    def _listen_with_google(self):
        """使用Google语音识别（备选方案）"""
        try:
            print("🎤 Google语音识别，请说话...")
            with self.microphone as source:
                # 监听语音，增加超时时间用于确认
                audio = self.recognizer.listen(source, timeout=8, phrase_time_limit=10)
            
            print("正在识别...")
            # 使用Google语音识别
            text = self.recognizer.recognize_google(audio, language=SPEECH_RECOGNITION_LANGUAGE)
            print(f"✅ Google识别结果: {text}")
            return text
            
        except sr.WaitTimeoutError:
            print("⏰ Google语音输入超时")
            return None
        except sr.UnknownValueError:
            print("🔇 Google无法识别语音")
            return None
        except sr.RequestError as e:
            print(f"❌ Google语音识别服务错误: {e}")
            return None
    
    def speak(self, text):
        """文字转语音 - 使用优化的多引擎TTS"""
        try:
            success = self.tts_engine.speak(text)
            if success:
                print("✅ 播报完成")
                # 短暂延迟确保播报完成
                import time
                time.sleep(0.1)
            else:
                print("❌ 播报失败")
                # 尝试切换引擎重试
                print("🔄 尝试切换引擎重试...")
                if self.tts_engine.switch_engine():
                    success = self.tts_engine.speak(text)
                    if success:
                        print("✅ 切换引擎后播报成功")
                    else:
                        print(f"📢 所有引擎失败，控制台输出: {text}")
                else:
                    print(f"📢 无可用引擎，控制台输出: {text}")
        except Exception as e:
            print(f"❌ 语音播报异常: {e}")
            # 备选方案：控制台输出
            print(f"📢 播报内容: {text}")
    

    

    
    def test_microphone(self):
        """测试麦克风是否可用"""
        try:
            if self.use_xfyun and self.xfyun_asr:
                # 测试科大讯飞API连接
                success, message = self.xfyun_asr.test_connection()
                if success:
                    print("科大讯飞语音识别API连接正常")
                    return True
                else:
                    print(f"科大讯飞API测试失败: {message}")
                    print("将使用Google语音识别作为备选")
                    self.use_xfyun = False
            
            # 测试Google语音识别的麦克风
            with self.microphone as source:
                print("测试麦克风...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("麦克风测试成功")
            return True
            
        except Exception as e:
            print(f"麦克风测试失败: {e}")
            return False
    
    def test_tts(self):
        """测试TTS引擎"""
        try:
            print("=== TTS引擎测试 ===")
            print(f"{self.tts_engine.get_engine_info()}")
            
            # 获取可用引擎
            available = self.tts_engine.get_available_engines()
            print(f"📋 可用引擎: {available}")
            
            # 测试播报
            test_success = self.tts_engine.speak("TTS引擎测试成功")
            if test_success:
                print("✅ TTS引擎测试通过")
                return True
            else:
                print("❌ TTS引擎测试失败")
                return False
                
        except Exception as e:
            print(f"❌ TTS测试异常: {e}")
            return False
    
    def switch_tts_engine(self, engine_name: str = None):
        """切换TTS引擎"""
        try:
            if self.tts_engine.switch_engine(engine_name):
                print(f"✅ TTS引擎切换成功")
                return True
            else:
                print(f"❌ TTS引擎切换失败")
                return False
        except Exception as e:
            print(f"❌ 切换TTS引擎异常: {e}")
            return False
    
    def cleanup(self):
        """清理资源"""
        try:
            if hasattr(self, 'tts_engine') and self.tts_engine:
                self.tts_engine.cleanup()
                print("🧹 SpeechHandler资源清理完成")
        except Exception as e:
            print(f"⚠️ SpeechHandler清理资源时出错: {e}")
    
    def __del__(self):
        """析构函数"""
        self.cleanup()