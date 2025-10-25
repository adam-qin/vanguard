#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time

# 设置环境变量
os.environ['USE_XFYUN_ASR'] = 'true'

def test_optimized_tts():
    """测试优化后的TTS引擎"""
    try:
        print("=== 优化TTS引擎测试 ===")
        
        from tts_engine import TTSEngine
        
        # 创建TTS引擎
        tts = TTSEngine()
        print(f"\n{tts.get_engine_info()}")
        
        # 获取可用引擎
        available = tts.get_available_engines()
        print(f"📋 可用引擎: {available}")
        
        # 测试消息
        test_messages = [
            "优化TTS引擎测试开始",
            "正在测试语音播报质量和稳定性",
            "即将导航从科技园到深圳南山海岸城，预计用时25分钟",
            "请注意，前方路口左转",
            "已到达目的地，导航结束",
            "优化TTS引擎测试完成"
        ]
        
        print(f"\n=== 测试当前引擎: {tts.current_engine} ===")
        
        for i, msg in enumerate(test_messages, 1):
            print(f"\n--- 测试 {i}/6 ---")
            start_time = time.time()
            
            success = tts.speak(msg)
            
            end_time = time.time()
            duration = end_time - start_time
            
            if success:
                print(f"✅ 测试 {i} 成功 (耗时: {duration:.2f}秒)")
            else:
                print(f"❌ 测试 {i} 失败 (耗时: {duration:.2f}秒)")
            
            # 短暂间隔
            time.sleep(0.5)
        
        # 测试引擎切换
        print(f"\n=== 测试引擎切换 ===")
        for engine in available:
            if engine != tts.current_engine:
                print(f"\n🔄 切换到引擎: {engine}")
                if tts.switch_engine(engine):
                    success = tts.speak(f"现在使用{engine}引擎播报")
                    if success:
                        print(f"✅ {engine} 引擎测试成功")
                    else:
                        print(f"❌ {engine} 引擎测试失败")
                    time.sleep(1)
        
        # 测试缓存效果
        print(f"\n=== 测试缓存效果 ===")
        test_text = "这是缓存测试消息"
        
        print("首次播报（生成缓存）:")
        start_time = time.time()
        tts.speak(test_text)
        first_duration = time.time() - start_time
        
        time.sleep(0.5)
        
        print("第二次播报（使用缓存）:")
        start_time = time.time()
        tts.speak(test_text)
        second_duration = time.time() - start_time
        
        print(f"📊 性能对比: 首次 {first_duration:.2f}s, 缓存 {second_duration:.2f}s")
        if second_duration < first_duration:
            print("✅ 缓存加速生效")
        
        # 清理测试
        print(f"\n=== 清理测试 ===")
        print(f"清理前: {tts.get_engine_info()}")
        tts.cleanup()
        print("✅ 清理完成")
        
        print(f"\n🎉 优化TTS引擎测试完成")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_speech_handler_integration():
    """测试与SpeechHandler的集成"""
    try:
        print(f"\n=== SpeechHandler集成测试 ===")
        
        from speech_handler import SpeechHandler
        handler = SpeechHandler()
        
        integration_messages = [
            "SpeechHandler集成测试",
            "语音识别和播报系统正常",
            "集成测试完成"
        ]
        
        for i, msg in enumerate(integration_messages, 1):
            print(f"\n--- 集成测试 {i}/3 ---")
            handler.speak(msg)
            time.sleep(0.8)
        
        print("✅ SpeechHandler集成测试完成")
        return True
        
    except Exception as e:
        print(f"❌ 集成测试失败: {e}")
        return False

if __name__ == "__main__":
    success1 = test_optimized_tts()
    success2 = test_speech_handler_integration()
    
    if success1 and success2:
        print(f"\n🎉 所有测试通过！")
    else:
        print(f"\n⚠️ 部分测试失败")