#!/usr/bin/env python3
# -*- coding: utf-8 -*-

print("正在检查依赖包...")

try:
    import speech_recognition
    print("✓ SpeechRecognition:", speech_recognition.__version__)
except ImportError as e:
    print("✗ SpeechRecognition 导入失败:", e)

try:
    import win32com.client
    print("✓ win32com.client (Windows SAPI): 已安装")
except ImportError as e:
    print("✗ win32com.client 导入失败:", e)

try:
    import edge_tts
    print("✓ edge_tts: 已安装")
except ImportError as e:
    print("✗ edge_tts 导入失败:", e)

try:
    import pygame
    print("✓ pygame: 已安装")
except ImportError as e:
    print("✗ pygame 导入失败:", e)

try:
    import dashscope
    print("✓ dashscope: 已安装")
except ImportError as e:
    print("✗ dashscope 导入失败:", e)

try:
    import requests
    print("✓ requests:", requests.__version__)
except ImportError as e:
    print("✗ requests 导入失败:", e)

try:
    import urllib3
    print("✓ urllib3:", urllib3.__version__)
except ImportError as e:
    print("✗ urllib3 导入失败:", e)

print("\n依赖检查完成！")