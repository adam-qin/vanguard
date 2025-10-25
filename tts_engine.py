#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import tempfile
import time
import hashlib
from typing import Optional, Dict, Any

class TTSEngine:
    """多引擎语音播报类 - 优化版"""
    
    def __init__(self):
        self.engines = ['sapi', 'edge_tts', 'pyttsx3']
        self.current_engine = None
        self.engine_cache = {}  # 引擎实例缓存
        self.audio_cache = {}   # 音频文件缓存
        self.cache_dir = tempfile.mkdtemp(prefix="tts_cache_")
        self.test_engines()
    
    def test_engines(self):
        """测试可用的TTS引擎"""
        print("🔍 测试可用的TTS引擎...")
        
        for engine in self.engines:
            if self._test_engine(engine):
                self.current_engine = engine
                print(f"✅ 选择引擎: {engine}")
                break
        
        if not self.current_engine:
            print("❌ 未找到可用的TTS引擎")
            self.current_engine = 'fallback'
    
    def _test_engine(self, engine_name: str) -> bool:
        """测试单个引擎"""
        try:
            if engine_name == 'sapi':
                return self._test_sapi()
            elif engine_name == 'edge_tts':
                return self._test_edge_tts()
            elif engine_name == 'pyttsx3':
                return self._test_pyttsx3()
            return False
        except Exception as e:
            print(f"   ❌ {engine_name} 测试失败: {e}")
            return False
    
    def _test_sapi(self) -> bool:
        """测试Windows SAPI"""
        try:
            import win32com.client
            sapi = win32com.client.Dispatch("SAPI.SpVoice")
            # 不实际播放，只测试创建
            print("   ✅ Windows SAPI 可用")
            return True
        except Exception:
            print("   ❌ Windows SAPI 不可用")
            return False
    
    def _test_edge_tts(self) -> bool:
        """测试Edge TTS"""
        try:
            import edge_tts
            print("   ✅ Edge TTS 可用")
            return True
        except Exception:
            print("   ❌ Edge TTS 不可用")
            return False
    
    def _test_pyttsx3(self) -> bool:
        """测试pyttsx3"""
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.stop()
            print("   ✅ pyttsx3 可用")
            return True
        except Exception:
            print("   ❌ pyttsx3 不可用")
            return False
    
    def speak(self, text: str) -> bool:
        """语音播报"""
        print(f"🔊 [{self.current_engine}] 播报: {text}")
        
        try:
            if self.current_engine == 'sapi':
                return self._speak_sapi(text)
            elif self.current_engine == 'edge_tts':
                return self._speak_edge_tts(text)
            elif self.current_engine == 'pyttsx3':
                return self._speak_pyttsx3(text)
            else:
                # 备选方案：控制台输出
                print(f"📢 播报内容: {text}")
                return True
        except Exception as e:
            print(f"❌ 播报失败: {e}")
            # 尝试下一个引擎
            return self._try_next_engine(text)
    
    def _speak_sapi(self, text: str) -> bool:
        """使用Windows SAPI播报 - 优化版"""
        try:
            import win32com.client
            
            # 使用缓存的SAPI实例
            if 'sapi' not in self.engine_cache:
                sapi = win32com.client.Dispatch("SAPI.SpVoice")
                
                # 优化语音参数
                sapi.Rate = 1   # 稍快语速 (-10 到 10)
                sapi.Volume = 95  # 稍低音量避免失真
                
                # 选择最佳中文语音
                voices = sapi.GetVoices()
                best_voice = None
                
                # 优先级：中文女声 > 中文男声 > 默认
                for voice in voices:
                    desc = voice.GetDescription().lower()
                    if 'chinese' in desc or 'zh-cn' in desc or 'mandarin' in desc:
                        if 'female' in desc or 'xiaoxiao' in desc or 'yaoyao' in desc:
                            best_voice = voice
                            break
                        elif not best_voice:  # 备选中文男声
                            best_voice = voice
                
                if best_voice:
                    sapi.Voice = best_voice
                    print(f"🎤 使用语音: {best_voice.GetDescription()}")
                
                self.engine_cache['sapi'] = sapi
            
            sapi = self.engine_cache['sapi']
            
            # 同步播报，确保完成
            sapi.Speak(text, 0)  # 0 = 同步模式
            print("✅ SAPI播报完成")
            return True
            
        except Exception as e:
            print(f"❌ SAPI播报失败: {e}")
            # 清除缓存的实例
            if 'sapi' in self.engine_cache:
                del self.engine_cache['sapi']
            return False
    
    def _speak_edge_tts(self, text: str) -> bool:
        """使用Edge TTS播报 - 优化版"""
        try:
            import edge_tts
            import asyncio
            import pygame
            
            # 检查缓存
            text_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
            cache_path = os.path.join(self.cache_dir, f"edge_{text_hash}.mp3")
            
            async def _async_speak():
                # 如果缓存存在，直接使用
                if not os.path.exists(cache_path):
                    # 使用高质量中文语音
                    voice = "zh-CN-XiaoxiaoNeural"  # 中文女声，自然度高
                    
                    # 生成语音，添加语音参数优化
                    communicate = edge_tts.Communicate(
                        text, 
                        voice,
                        rate="+10%",    # 稍快语速
                        volume="+0%"    # 正常音量
                    )
                    
                    await communicate.save(cache_path)
                    print(f"💾 缓存语音: {cache_path}")
                
                # 初始化pygame音频
                if not pygame.mixer.get_init():
                    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=1024)
                
                # 播放音频
                pygame.mixer.music.load(cache_path)
                pygame.mixer.music.play()
                
                # 等待播放完成，添加超时保护
                timeout = time.time() + 30  # 30秒超时
                while pygame.mixer.music.get_busy() and time.time() < timeout:
                    time.sleep(0.05)  # 更短的检查间隔
                
                if time.time() >= timeout:
                    pygame.mixer.music.stop()
                    print("⚠️ 播放超时，强制停止")
            
            # 运行异步函数
            try:
                asyncio.run(_async_speak())
            except RuntimeError:
                # 如果已有事件循环，使用新线程
                import threading
                import concurrent.futures
                
                def run_in_thread():
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        loop.run_until_complete(_async_speak())
                    finally:
                        loop.close()
                
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(run_in_thread)
                    future.result(timeout=35)  # 35秒总超时
            
            print("✅ Edge TTS播报完成")
            return True
            
        except Exception as e:
            print(f"❌ Edge TTS播报失败: {e}")
            return False
    
    def _speak_pyttsx3(self, text: str) -> bool:
        """使用pyttsx3播报 - 优化版"""
        try:
            import pyttsx3
            
            # 使用缓存的引擎实例
            if 'pyttsx3' not in self.engine_cache:
                engine = pyttsx3.init()
                
                # 优化参数
                engine.setProperty('rate', 160)    # 稍快语速
                engine.setProperty('volume', 0.85) # 稍低音量
                
                # 选择最佳中文语音
                voices = engine.getProperty('voices')
                best_voice = None
                
                if voices:
                    for voice in voices:
                        voice_name = voice.name.lower()
                        voice_id = voice.id.lower()
                        
                        # 优先选择中文语音
                        if any(keyword in voice_name or keyword in voice_id 
                               for keyword in ['chinese', 'zh', 'mandarin', 'china']):
                            # 优先女声
                            if any(keyword in voice_name 
                                   for keyword in ['female', 'woman', 'xiaoxiao', 'yaoyao']):
                                best_voice = voice
                                break
                            elif not best_voice:
                                best_voice = voice
                
                if best_voice:
                    engine.setProperty('voice', best_voice.id)
                    print(f"🎤 使用pyttsx3语音: {best_voice.name}")
                
                self.engine_cache['pyttsx3'] = engine
            
            engine = self.engine_cache['pyttsx3']
            
            # 清除之前的队列
            engine.stop()
            
            # 播报
            engine.say(text)
            engine.runAndWait()
            
            print("✅ pyttsx3播报完成")
            return True
            
        except Exception as e:
            print(f"❌ pyttsx3播报失败: {e}")
            # 清除缓存的实例
            if 'pyttsx3' in self.engine_cache:
                try:
                    self.engine_cache['pyttsx3'].stop()
                except:
                    pass
                del self.engine_cache['pyttsx3']
            return False
    
    def _try_next_engine(self, text: str) -> bool:
        """尝试下一个可用引擎"""
        current_index = self.engines.index(self.current_engine) if self.current_engine in self.engines else -1
        
        for i in range(current_index + 1, len(self.engines)):
            engine_name = self.engines[i]
            print(f"🔄 尝试切换到 {engine_name}")
            
            if self._test_engine(engine_name):
                self.current_engine = engine_name
                return self.speak(text)
        
        # 所有引擎都失败，使用备选方案
        print(f"📢 所有TTS引擎都失败，控制台输出: {text}")
        return True
    
    def get_engine_info(self) -> str:
        """获取当前引擎信息"""
        cache_info = f"缓存: {len(self.engine_cache)}个引擎, {len(self.audio_cache)}个音频"
        return f"当前TTS引擎: {self.current_engine} ({cache_info})"
    
    def cleanup(self):
        """清理资源"""
        try:
            # 停止pyttsx3引擎
            if 'pyttsx3' in self.engine_cache:
                try:
                    self.engine_cache['pyttsx3'].stop()
                except:
                    pass
            
            # 停止pygame
            try:
                import pygame
                if pygame.mixer.get_init():
                    pygame.mixer.quit()
            except:
                pass
            
            # 清理缓存目录
            import shutil
            if os.path.exists(self.cache_dir):
                try:
                    shutil.rmtree(self.cache_dir)
                    print(f"🧹 清理缓存目录: {self.cache_dir}")
                except:
                    pass
            
            self.engine_cache.clear()
            self.audio_cache.clear()
            
        except Exception as e:
            print(f"⚠️ 清理资源时出错: {e}")
    
    def __del__(self):
        """析构函数"""
        self.cleanup()
    
    def switch_engine(self, engine_name: str = None) -> bool:
        """手动切换引擎"""
        if engine_name and engine_name in self.engines:
            if self._test_engine(engine_name):
                old_engine = self.current_engine
                self.current_engine = engine_name
                print(f"🔄 引擎切换: {old_engine} → {engine_name}")
                return True
            else:
                print(f"❌ 引擎 {engine_name} 不可用")
                return False
        else:
            # 自动切换到下一个可用引擎
            return self._try_next_engine("测试")
    
    def get_available_engines(self) -> list:
        """获取所有可用引擎列表"""
        available = []
        for engine in self.engines:
            if self._test_engine(engine):
                available.append(engine)
        return available