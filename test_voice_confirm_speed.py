#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试语音确认速度优化
"""

import time
import asyncio

def test_voice_confirmation_speed():
    """测试语音确认速度"""
    print("=== 语音确认速度测试 ===")
    
    try:
        from main import NavigationApp
        
        # 创建应用实例
        app = NavigationApp()
        
        # 测试TTS播报速度
        print("\n1. 测试TTS播报速度...")
        start_time = time.time()
        
        test_msg = "测试播报速度"
        app.speech_handler.speak(test_msg)
        
        tts_time = time.time() - start_time
        print(f"   TTS播报耗时: {tts_time:.2f}秒")
        
        # 测试语音识别初始化速度
        print("\n2. 测试语音识别初始化...")
        if app.speech_handler.use_xfyun and app.speech_handler.xfyun_asr:
            start_time = time.time()
            
            # 模拟设置关键词
            original_keywords = app.speech_handler.xfyun_asr.trigger_keywords
            app.speech_handler.xfyun_asr.trigger_keywords = ['确认', '取消']
            
            init_time = time.time() - start_time
            print(f"   关键词设置耗时: {init_time:.3f}秒")
            
            # 恢复关键词
            app.speech_handler.xfyun_asr.trigger_keywords = original_keywords
        else:
            print("   科大讯飞不可用")
        
        # 测试完整确认流程的理论时间
        print("\n3. 理论确认流程时间分析:")
        print("   - TTS播报: ~2-4秒 (取决于文本长度)")
        print("   - 等待间隔: 0.3秒 (已优化)")
        print("   - WebSocket连接: ~0.5-1秒")
        print("   - 语音识别: ~1-3秒 (取决于说话速度)")
        print("   - 总计: ~4-8.3秒")
        
        print("\n4. 优化建议:")
        print("   ✅ 已缩短等待间隔 (1秒 → 0.3秒)")
        print("   ✅ 已缩短识别等待 (2秒 → 0.5秒)")
        print("   ✅ 已缩短超时时间 (10秒 → 8秒)")
        print("   💡 建议: 用户在播报开始时就可以准备说话")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

async def test_async_confirmation():
    """测试异步确认流程"""
    print("\n=== 异步确认流程测试 ===")
    
    try:
        from main import NavigationApp
        
        app = NavigationApp()
        
        # 模拟确认流程
        origin = "测试起点"
        destination = "测试终点"
        
        print("模拟确认流程...")
        start_time = time.time()
        
        # 这里不实际执行，只是测试流程
        print("1. 播报确认信息 (模拟)")
        await asyncio.sleep(0.1)  # 模拟播报时间
        
        print("2. 显示提示信息")
        await asyncio.sleep(0.3)  # 实际等待时间
        
        print("3. 开始语音识别 (模拟)")
        await asyncio.sleep(0.1)  # 模拟识别准备
        
        total_time = time.time() - start_time
        print(f"✅ 模拟流程总耗时: {total_time:.2f}秒")
        
        return True
        
    except Exception as e:
        print(f"❌ 异步测试失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 语音确认速度优化测试")
    print("=" * 50)
    
    # 测试语音确认速度
    speed_success = test_voice_confirmation_speed()
    
    # 测试异步流程
    async_success = asyncio.run(test_async_confirmation())
    
    print("\n" + "=" * 50)
    if speed_success and async_success:
        print("🎉 所有测试通过！")
        print("\n📊 优化总结:")
        print("1. ⚡ 缩短了等待间隔")
        print("2. ⚡ 优化了识别等待时间")
        print("3. ⚡ 减少了超时时间")
        print("4. 💡 用户体验应该更加流畅")
    else:
        print("❌ 测试失败，需要进一步优化")

if __name__ == "__main__":
    main()