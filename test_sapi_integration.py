#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time

# 设置环境变量
os.environ['USE_XFYUN_ASR'] = 'true'

def test_sapi_integration():
    """测试SAPI引擎集成"""
    try:
        print("=== SAPI引擎集成测试 ===")
        
        # 1. 测试TTS引擎
        print("\n1. 测试TTS引擎...")
        from tts_engine import TTSEngine
        
        tts = TTSEngine()
        print(f"{tts.get_engine_info()}")
        
        if tts.current_engine != 'sapi':
            print(f"⚠️ 当前引擎不是SAPI: {tts.current_engine}")
            if 'sapi' in tts.get_available_engines():
                print("🔄 切换到SAPI引擎...")
                tts.switch_engine('sapi')
            else:
                print("❌ SAPI引擎不可用")
                return False
        
        # 2. 测试SpeechHandler
        print("\n2. 测试SpeechHandler...")
        from speech_handler import SpeechHandler
        
        handler = SpeechHandler()
        
        # 3. 测试TTS功能
        print("\n3. 测试TTS功能...")
        handler.test_tts()
        
        # 4. 测试实际播报
        print("\n4. 测试实际播报...")
        test_messages = [
            "SAPI引擎集成测试开始",
            "正在测试语音播报功能",
            "即将导航从科技园到深圳南山海岸城",
            "请注意，前方路口左转",
            "已到达目的地，导航结束",
            "SAPI引擎集成测试完成"
        ]
        
        for i, msg in enumerate(test_messages, 1):
            print(f"\n--- 播报测试 {i}/6 ---")
            start_time = time.time()
            
            handler.speak(msg)
            
            duration = time.time() - start_time
            print(f"✅ 播报 {i} 完成 (耗时: {duration:.2f}秒)")
            
            # 短暂间隔
            time.sleep(0.8)
        
        # 5. 测试引擎切换
        print("\n5. 测试引擎切换...")
        available = handler.tts_engine.get_available_engines()
        print(f"可用引擎: {available}")
        
        for engine in available:
            if engine != handler.tts_engine.current_engine:
                print(f"\n🔄 切换到引擎: {engine}")
                if handler.switch_tts_engine(engine):
                    handler.speak(f"现在使用{engine}引擎播报")
                    time.sleep(1)
        
        # 6. 切换回SAPI
        print(f"\n6. 切换回SAPI引擎...")
        if handler.switch_tts_engine('sapi'):
            handler.speak("已切换回SAPI引擎")
        
        # 7. 清理测试
        print(f"\n7. 清理测试...")
        handler.cleanup()
        print("✅ 清理完成")
        
        print(f"\n🎉 SAPI引擎集成测试完成")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_performance():
    """测试性能"""
    try:
        print(f"\n=== 性能测试 ===")
        
        from speech_handler import SpeechHandler
        handler = SpeechHandler()
        
        # 测试连续播报性能
        test_text = "性能测试消息"
        times = []
        
        for i in range(5):
            print(f"性能测试 {i+1}/5")
            start_time = time.time()
            handler.speak(test_text)
            duration = time.time() - start_time
            times.append(duration)
            print(f"耗时: {duration:.2f}秒")
            time.sleep(0.3)
        
        avg_time = sum(times) / len(times)
        print(f"\n📊 平均播报时间: {avg_time:.2f}秒")
        print(f"📊 最快: {min(times):.2f}秒")
        print(f"📊 最慢: {max(times):.2f}秒")
        
        if avg_time < 2.0:
            print("✅ 性能良好")
        else:
            print("⚠️ 性能需要优化")
        
        handler.cleanup()
        return True
        
    except Exception as e:
        print(f"❌ 性能测试失败: {e}")
        return False

if __name__ == "__main__":
    success1 = test_sapi_integration()
    success2 = test_performance()
    
    if success1 and success2:
        print(f"\n🎉 所有测试通过！SAPI引擎集成成功")
    else:
        print(f"\n⚠️ 部分测试失败")