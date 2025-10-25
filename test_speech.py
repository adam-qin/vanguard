#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

# 设置环境变量
os.environ['DASHSCOPE_API_KEY'] = 'sk-9bf124f946124600b9d70824998dc2a2'
os.environ['AMAP_API_KEY'] = '95fd23e5ff3e8d97d46b5c07f5077a4e'
os.environ['USE_XFYUN_ASR'] = 'false'  # 暂时禁用科大讯飞，使用Google ASR

from speech_handler import SpeechHandler

def test_speech_recognition():
    print("=== 语音识别测试 ===")
    
    try:
        speech_handler = SpeechHandler()
        
        # 测试麦克风
        print("1. 测试麦克风...")
        if speech_handler.test_microphone():
            print("✓ 麦克风测试成功")
        else:
            print("✗ 麦克风测试失败")
            return
        
        # 测试语音识别
        print("\n2. 测试语音识别...")
        print("请说话（比如：从北京到上海导航）...")
        
        text = speech_handler.listen_for_speech()
        
        if text:
            print(f"✓ 识别成功: {text}")
            
            # 测试语音播报
            print("\n3. 测试语音播报...")
            speech_handler.speak(f"您说的是: {text}")
            
        else:
            print("✗ 语音识别失败")
    
    except Exception as e:
        print(f"测试过程中出错: {e}")

if __name__ == "__main__":
    test_speech_recognition()