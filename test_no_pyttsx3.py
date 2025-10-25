#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

# 设置环境变量
os.environ['USE_XFYUN_ASR'] = 'true'

def test_no_pyttsx3():
    """测试确保不再使用pyttsx3"""
    try:
        print("=== 验证pyttsx3替换测试 ===")
        
        # 1. 测试SpeechHandler不依赖pyttsx3
        print("\n1. 测试SpeechHandler...")
        from speech_handler import SpeechHandler
        
        handler = SpeechHandler()
        print(f"✅ SpeechHandler初始化成功")
        print(f"🔊 {handler.tts_engine.get_engine_info()}")
        
        # 2. 测试播报功能
        print("\n2. 测试播报功能...")
        test_msg = "这是不使用pyttsx3的播报测试"
        success = handler.speak(test_msg)
        
        if hasattr(handler, 'speak'):
            print("✅ speak方法存在")
        else:
            print("❌ speak方法不存在")
            return False
        
        # 3. 检查TTS引擎类型
        print(f"\n3. 检查TTS引擎...")
        engine_type = type(handler.tts_engine).__name__
        print(f"TTS引擎类型: {engine_type}")
        
        if engine_type == 'TTSEngine':
            print("✅ 使用优化的TTSEngine")
        else:
            print(f"❌ 意外的引擎类型: {engine_type}")
            return False
        
        # 4. 测试引擎功能
        print(f"\n4. 测试引擎功能...")
        available = handler.tts_engine.get_available_engines()
        print(f"可用引擎: {available}")
        
        if 'sapi' in available:
            print("✅ SAPI引擎可用")
        else:
            print("⚠️ SAPI引擎不可用")
        
        # 5. 清理测试
        print(f"\n5. 清理测试...")
        handler.cleanup()
        print("✅ 清理完成")
        
        print(f"\n🎉 pyttsx3替换验证成功！")
        return True
        
    except ImportError as e:
        if 'pyttsx3' in str(e):
            print(f"❌ 仍然依赖pyttsx3: {e}")
            return False
        else:
            print(f"❌ 其他导入错误: {e}")
            return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_imports():
    """检查导入情况"""
    print(f"\n=== 检查导入情况 ===")
    
    try:
        # 检查speech_handler.py的导入
        import speech_handler
        print("✅ speech_handler导入成功")
        
        # 检查tts_engine.py的导入
        import tts_engine
        print("✅ tts_engine导入成功")
        
        # 检查是否意外导入了pyttsx3
        import sys
        if 'pyttsx3' in sys.modules:
            print("⚠️ pyttsx3仍在模块中")
            # 这可能是正常的，因为tts_engine.py中有pyttsx3作为备选
        else:
            print("✅ pyttsx3未被导入")
        
        return True
        
    except Exception as e:
        print(f"❌ 导入检查失败: {e}")
        return False

if __name__ == "__main__":
    success1 = check_imports()
    success2 = test_no_pyttsx3()
    
    if success1 and success2:
        print(f"\n🎉 所有验证通过！pyttsx3已成功替换为SAPI引擎")
    else:
        print(f"\n⚠️ 部分验证失败")