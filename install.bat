@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
title 高德地图语音导航助手 - 环境安装

echo.
echo ==========================================
echo   高德地图语音导航助手 - 环境安装
echo ==========================================
echo.

REM 检查Python是否安装
echo 🔍 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到Python，请先安装Python 3.7+
    echo    下载地址: https://www.python.org/downloads/
    echo    或者检查Python是否已添加到系统PATH
    echo.
    pause
    exit /b 1
)

REM 显示Python版本
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python版本: %PYTHON_VERSION%

REM 检查pip
echo.
echo 🔍 检查pip包管理器...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip不可用，请检查Python安装
    pause
    exit /b 1
)
echo ✅ pip可用

REM 升级pip
echo.
echo 📦 升级pip到最新版本...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo ⚠️ pip升级失败，继续安装...
) else (
    echo ✅ pip升级成功
)

REM 安装核心依赖
echo.
echo 📦 安装核心依赖包...
echo.

echo 1/8 安装requests (HTTP请求库)...
python -m pip install "requests>=2.31.0"
if errorlevel 1 (
    echo ❌ requests安装失败
    goto :install_failed
)

echo 2/8 安装dashscope (阿里云千问API)...
python -m pip install "dashscope>=1.17.0"
if errorlevel 1 (
    echo ❌ dashscope安装失败
    goto :install_failed
)

echo 3/8 安装SpeechRecognition (语音识别)...
python -m pip install "SpeechRecognition>=3.8.0"
if errorlevel 1 (
    echo ❌ SpeechRecognition安装失败
    goto :install_failed
)

echo 4/8 安装websocket-client (科大讯飞语音)...
python -m pip install "websocket-client>=1.0.0"
if errorlevel 1 (
    echo ❌ websocket-client安装失败
    goto :install_failed
)

echo 5/8 安装python-dotenv (环境变量加载)...
python -m pip install "python-dotenv>=1.0.0"
if errorlevel 1 (
    echo ❌ python-dotenv安装失败
    goto :install_failed
)

REM Windows特定依赖
echo 6/8 安装pywin32 (Windows SAPI语音)...
python -m pip install "pywin32>=308"
if errorlevel 1 (
    echo ⚠️ pywin32安装失败，Windows SAPI语音功能可能不可用
)

REM 可选音频依赖
echo 7/8 安装pygame (音频播放)...
python -m pip install "pygame>=2.6.0"
if errorlevel 1 (
    echo ⚠️ pygame安装失败，Edge TTS功能可能不可用
)

echo 8/8 安装edge-tts (微软Edge语音)...
python -m pip install "edge-tts>=6.1.0"
if errorlevel 1 (
    echo ⚠️ edge-tts安装失败，Edge TTS功能可能不可用
)

REM 可选的pyaudio (科大讯飞语音录音)
echo.
echo 📦 安装可选依赖...
echo 安装pyaudio (科大讯飞语音录音)...
python -m pip install "pyaudio>=0.2.11"
if errorlevel 1 (
    echo ⚠️ pyaudio安装失败，科大讯飞语音功能可能不可用
    echo    如需使用科大讯飞语音，请手动安装pyaudio
)

echo.
echo ✅ 依赖包安装完成！

REM 创建环境配置文件
echo.
echo 🔧 创建环境配置文件...
if not exist .env (
    if exist .env.example (
        copy .env.example .env >nul
        echo ✅ 已复制 .env.example 为 .env
    ) else (
        echo # 高德地图语音导航助手配置文件 > .env
        echo # 请填入您的实际API密钥 >> .env
        echo. >> .env
        echo # 基础AI配置 ^(必需^) >> .env
        echo DASHSCOPE_API_KEY=your_dashscope_api_key >> .env
        echo. >> .env
        echo # 高德地图API配置 >> .env
        echo AMAP_API_KEY=your_amap_api_key >> .env
        echo. >> .env
        echo # 七牛云MCP配置 >> .env
        echo OPENAI_BASE_URL=https://your-qiniu-mcp-server.com >> .env
        echo OPENAI_API_KEY=your_qiniu_mcp_api_key >> .env
        echo USE_QINIU_MCP=false >> .env
        echo. >> .env
        echo # 语音识别配置 >> .env
        echo XFYUN_APP_ID=your_xfyun_app_id >> .env
        echo XFYUN_API_SECRET=your_xfyun_api_secret >> .env
        echo XFYUN_API_KEY=your_xfyun_api_key >> .env
        echo USE_XFYUN_ASR=true >> .env
        echo ✅ 已创建 .env 配置文件
    )
) else (
    echo ✅ .env 文件已存在
)

REM 测试安装
echo.
echo 🧪 测试安装结果...
python -c "
try:
    import requests, dashscope, speech_recognition, websocket
    print('✅ 核心依赖测试通过')
except ImportError as e:
    print(f'❌ 核心依赖测试失败: {e}')
    exit(1)

try:
    import win32com.client
    print('✅ Windows SAPI 可用')
except ImportError:
    print('⚠️ Windows SAPI 不可用')

try:
    import pygame, edge_tts
    print('✅ 音频功能可用')
except ImportError:
    print('⚠️ 部分音频功能不可用')

try:
    import pyaudio
    print('✅ 科大讯飞语音录音可用')
except ImportError:
    print('⚠️ 科大讯飞语音录音不可用')
"

if errorlevel 1 (
    echo.
    echo ❌ 安装测试失败，请检查错误信息
    goto :install_failed
)

echo.
echo ==========================================
echo 🎉 安装成功完成！
echo ==========================================
echo.
echo 📋 下一步操作：
echo 1. 编辑 .env 文件，填入您的实际API密钥
echo 2. 运行程序: python main.py
echo 3. 或使用启动脚本: start.bat
echo.
echo 📚 重要提示：
echo • DASHSCOPE_API_KEY 是必需的（阿里云通义千问）
echo • 至少配置一个导航API（高德API或七牛云MCP）
echo • 科大讯飞配置可选（用于语音识别）
echo.
echo 🔧 如遇问题，请运行: python test_config.py
echo.
pause
exit /b 0

:install_failed
echo.
echo ==========================================
echo ❌ 安装失败
echo ==========================================
echo.
echo 可能的解决方案：
echo 1. 检查网络连接
echo 2. 尝试使用国内镜像源：
echo    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple package_name
echo 3. 手动安装失败的包
echo 4. 检查Python版本是否兼容
echo.
pause
exit /b 1