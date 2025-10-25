#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time

# 设置环境变量
os.environ['USE_XFYUN_ASR'] = 'true'

def diagnose_audio_system():
    """诊断音频系统 - 使用优化TTS引擎"""
    print("=== 音频系统诊断 ===")
    
    try:
        from tts_engine import TTSEngine
        
        # 1. 检查TTS引擎
        print("\n1. 检查TTS引擎...")
        engine = TTSEngine()
        
        # 2. 检查引擎信息
        print(f"\n2. {engine.get_engine_info()}")
        available_engines = engine.get_available_engines()
        print(f"   可用引擎: {available_engines}")
        
        if not available_engines:
            print("   ❌ 未找到可用的TTS引擎")
            return False
        
        # 3. 测试当前引擎播报
        print(f"\n3. 测试当前引擎 ({engine.current_engine}) 播报...")
        test_messages = [
            "音频测试一",
            "音频测试二", 
            "音频测试三"
        ]
        
        for i, msg in enumerate(test_messages, 1):
            print(f"   测试 {i}: {msg}")
            try:
                success = engine.speak(msg)
                if success:
                    print(f"   ✅ 测试 {i} 完成")
                else:
                    print(f"   ❌ 测试 {i} 失败")
                time.sleep(0.5)
                
            except Exception as e:
                print(f"   ❌ 测试 {i} 异常: {e}")
        
        # 4. 测试引擎切换
        print(f"\n4. 测试引擎切换...")
        for engine_name in available_engines:
            if engine_name != engine.current_engine:
                print(f"   切换到引擎: {engine_name}")
                if engine.switch_engine(engine_name):
                    success = engine.speak(f"现在使用{engine_name}引擎")
                    if success:
                        print(f"   ✅ {engine_name} 引擎测试成功")
                    else:
                        print(f"   ❌ {engine_name} 引擎播报失败")
                else:
                    print(f"   ❌ 切换到{engine_name}失败")
                time.sleep(0.5)
        
        # 5. 测试多引擎实例
        print(f"\n5. 测试多引擎实例...")
        for i in range(3):
            try:
                print(f"   创建引擎实例 {i+1}")
                test_engine = TTSEngine()
                
                msg = f"多引擎测试 {i+1}"
                print(f"   播报: {msg}")
                success = test_engine.speak(msg)
                
                if success:
                    print(f"   ✅ 引擎 {i+1} 测试完成")
                else:
                    print(f"   ❌ 引擎 {i+1} 测试失败")
                
                # 清理资源
                test_engine.cleanup()
                time.sleep(0.3)
                
            except Exception as e:
                print(f"   ❌ 引擎 {i+1} 测试异常: {e}")
        
        print("\n=== 诊断完成 ===")
        return True
        
    except Exception as e:
        print(f"❌ 诊断过程出错: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_system_audio():
    """测试系统音频"""
    print("\n=== 系统音频测试 ===")
    
    try:
        # 尝试播放系统提示音
        import winsound
        print("播放系统提示音...")
        winsound.Beep(1000, 500)  # 1000Hz, 500ms
        print("✅ 系统音频正常")
        return True
        
    except Exception as e:
        print(f"❌ 系统音频测试失败: {e}")
        return False

if __name__ == "__main__":
    # 测试系统音频
    test_system_audio()
    
    # 诊断TTS
    diagnose_audio_system()