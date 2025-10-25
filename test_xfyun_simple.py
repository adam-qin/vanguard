#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time

# 设置环境变量
os.environ['XFYUN_APP_ID'] = 'f5df0409'
os.environ['XFYUN_API_SECRET'] = 'YTgwNDFmYzc2MmVjMDQ0NDQ0OWQyNmJm'
os.environ['XFYUN_API_KEY'] = '654d10ef61d2357133a93d84e6278628'
os.environ['USE_XFYUN_ASR'] = 'true'

def test_xfyun_connection():
    """测试科大讯飞连接"""
    try:
        from xfyun_asr import XfyunASR
        
        print("=== 科大讯飞语音识别测试 ===")
        
        # 创建ASR实例
        asr = XfyunASR()
        
        # 测试API配置
        print("1. 测试API配置...")
        success, message = asr.test_connection()
        if success:
            print(f"✓ {message}")
        else:
            print(f"✗ {message}")
            return False
        
        # 快速测试
        print("\n2. 快速连接测试...")
        result = asr.quick_test()
        if result:
            print(f"✓ {result}")
        else:
            print("✗ 快速测试失败")
        
        print("\n3. 语音识别测试...")
        print("请说话（测试用）...")
        
        # 进行语音识别
        text = asr.recognize_speech()
        
        if text:
            print(f"✓ 识别成功: {text}")
            return True
        else:
            print("✗ 识别失败或无结果")
            return False
            
    except Exception as e:
        print(f"测试过程中出错: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_speech_handler():
    """测试语音处理器"""
    try:
        from speech_handler import SpeechHandler
        
        print("\n=== 语音处理器测试 ===")
        
        handler = SpeechHandler()
        
        # 测试麦克风
        print("1. 测试麦克风...")
        if handler.test_microphone():
            print("✓ 麦克风测试成功")
        else:
            print("✗ 麦克风测试失败")
            return False
        
        # 测试语音识别
        print("\n2. 测试语音识别...")
        print("请说话...")
        
        text = handler.listen_for_speech()
        
        if text:
            print(f"✓ 识别成功: {text}")
            
            # 测试语音播报
            print("\n3. 测试语音播报...")
            handler.speak(f"识别结果是: {text}")
            
            return True
        else:
            print("✗ 语音识别失败")
            return False
            
    except Exception as e:
        print(f"语音处理器测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("开始语音识别系统测试...\n")
    
    # 测试科大讯飞直接调用
    xfyun_success = test_xfyun_connection()
    
    print("\n" + "="*50 + "\n")
    
    # 测试语音处理器
    handler_success = test_speech_handler()
    
    print("\n" + "="*50)
    print("测试结果总结:")
    print(f"科大讯飞直接调用: {'✓ 成功' if xfyun_success else '✗ 失败'}")
    print(f"语音处理器: {'✓ 成功' if handler_success else '✗ 失败'}")
    
    if xfyun_success or handler_success:
        print("\n至少一种语音识别方式可用，系统可以正常工作！")
    else:
        print("\n所有语音识别方式都失败，请检查配置和网络连接。")