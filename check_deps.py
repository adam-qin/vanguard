#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
依赖检查脚本
验证所有必需的依赖是否正确安装
"""

import sys

def check_core_dependencies():
    """检查核心依赖"""
    print("=== 核心依赖检查 ===")
    
    core_deps = [
        ('requests', '网络请求库'),
        ('dashscope', '阿里云千问API'),
        ('speech_recognition', '语音识别'),
        ('websocket', '科大讯飞语音连接'),
        ('json', 'JSON处理'),
        ('os', '系统操作'),
        ('asyncio', '异步处理'),
    ]
    
    failed = []
    
    for module, description in core_deps:
        try:
            __import__(module)
            print(f"✅ {module:20} - {description}")
        except ImportError as e:
            print(f"❌ {module:20} - {description} (失败: {e})")
            failed.append(module)
    
    return len(failed) == 0, failed

def check_optional_dependencies():
    """检查可选依赖"""
    print("\n=== 可选依赖检查 ===")
    
    optional_deps = [
        ('win32com.client', 'Windows SAPI语音'),
        ('pygame', '音频播放'),
        ('edge_tts', 'Edge TTS语音'),
        ('pyaudio', '科大讯飞录音'),
        ('dotenv', '环境变量加载'),
    ]
    
    available = []
    
    for module, description in optional_deps:
        try:
            if module == 'dotenv':
                from dotenv import load_dotenv
            else:
                __import__(module)
            print(f"✅ {module:20} - {description}")
            available.append(module)
        except ImportError:
            print(f"⚠️ {module:20} - {description} (不可用)")
    
    return available

def check_environment_variables():
    """检查环境变量"""
    print("\n=== 环境变量检查 ===")
    
    try:
        # 尝试加载环境变量
        try:
            from dotenv import load_dotenv
            load_dotenv()
            print("✅ .env 文件加载成功")
        except:
            print("⚠️ .env 文件加载失败或不存在")
        
        import os
        
        # 检查关键环境变量
        env_vars = [
            ('DASHSCOPE_API_KEY', '阿里云千问API密钥', True),
            ('AMAP_API_KEY', '高德地图API密钥', False),
            ('OPENAI_BASE_URL', '七牛云MCP服务器', False),
            ('OPENAI_API_KEY', '七牛云MCP密钥', False),
            ('XFYUN_APP_ID', '科大讯飞应用ID', False),
        ]
        
        configured = 0
        
        for var, desc, required in env_vars:
            value = os.getenv(var, '')
            if value and not value.startswith('your_') and not value.startswith('your-'):
                print(f"✅ {var:20} - {desc}")
                configured += 1
            elif required:
                print(f"❌ {var:20} - {desc} (必需)")
            else:
                print(f"⚠️ {var:20} - {desc} (可选)")
        
        return configured > 0
        
    except Exception as e:
        print(f"❌ 环境变量检查失败: {e}")
        return False

def check_functionality():
    """检查功能可用性"""
    print("\n=== 功能可用性检查 ===")
    
    functions = []
    
    # 检查AI处理
    try:
        from config import DASHSCOPE_API_KEY
        if DASHSCOPE_API_KEY and not DASHSCOPE_API_KEY.startswith('your'):
            print("✅ AI处理功能 - 可用")
            functions.append('ai')
        else:
            print("❌ AI处理功能 - 需要配置DASHSCOPE_API_KEY")
    except:
        print("❌ AI处理功能 - 配置加载失败")
    
    # 检查导航功能
    try:
        from config import AMAP_API_KEY, OPENAI_BASE_URL, OPENAI_API_KEY
        if (AMAP_API_KEY and not AMAP_API_KEY.startswith('your')) or \
           (OPENAI_BASE_URL and OPENAI_API_KEY and not OPENAI_API_KEY.startswith('your')):
            print("✅ 导航功能 - 可用")
            functions.append('navigation')
        else:
            print("❌ 导航功能 - 需要配置高德API或七牛云MCP")
    except:
        print("❌ 导航功能 - 配置加载失败")
    
    # 检查语音功能
    try:
        import speech_recognition
        print("✅ 语音识别 - 可用")
        functions.append('speech')
    except:
        print("❌ 语音识别 - 不可用")
    
    # 检查TTS功能
    tts_available = False
    try:
        import win32com.client
        print("✅ Windows SAPI TTS - 可用")
        tts_available = True
    except:
        print("⚠️ Windows SAPI TTS - 不可用")
    
    try:
        import edge_tts
        import pygame
        print("✅ Edge TTS - 可用")
        tts_available = True
    except:
        print("⚠️ Edge TTS - 不可用")
    
    if tts_available:
        functions.append('tts')
    
    return functions

def main():
    """主函数"""
    print("🔍 高德地图语音导航助手 - 依赖检查")
    print("=" * 50)
    
    # 检查Python版本
    print(f"Python版本: {sys.version}")
    if sys.version_info < (3, 7):
        print("❌ 需要Python 3.7或更高版本")
        return False
    
    # 检查核心依赖
    core_ok, failed_core = check_core_dependencies()
    
    # 检查可选依赖
    available_optional = check_optional_dependencies()
    
    # 检查环境变量
    env_ok = check_environment_variables()
    
    # 检查功能
    functions = check_functionality()
    
    # 总结
    print("\n" + "=" * 50)
    print("📊 检查结果总结")
    print("=" * 50)
    
    if core_ok:
        print("✅ 核心依赖: 全部安装")
    else:
        print(f"❌ 核心依赖: 缺少 {', '.join(failed_core)}")
    
    print(f"📦 可选依赖: {len(available_optional)}/5 可用")
    
    if env_ok:
        print("✅ 环境变量: 已配置")
    else:
        print("❌ 环境变量: 需要配置")
    
    print(f"🎯 可用功能: {', '.join(functions) if functions else '无'}")
    
    # 给出建议
    print("\n💡 建议:")
    if not core_ok:
        print("1. 运行 install.bat 安装缺少的核心依赖")
    if not env_ok:
        print("2. 编辑 .env 文件，配置API密钥")
    if 'ai' not in functions:
        print("3. 配置 DASHSCOPE_API_KEY (必需)")
    if 'navigation' not in functions:
        print("4. 配置高德API或七牛云MCP (至少一个)")
    
    success = core_ok and env_ok and 'ai' in functions and 'navigation' in functions
    
    if success:
        print("\n🎉 所有检查通过！可以正常使用程序")
    else:
        print("\n⚠️ 存在问题，请按建议进行配置")
    
    return success

if __name__ == "__main__":
    try:
        success = main()
        input("\n按回车键退出...")
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n检查被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n检查过程出错: {e}")
        sys.exit(1)