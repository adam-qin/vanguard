@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
title 高德地图语音导航助手 - 快速启动
cls

echo.
echo ==========================================
echo     高德地图语音导航助手 - 快速启动
echo ==========================================
echo.

REM 检查Python是否安装
echo 🔍 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到Python，请先安装Python 3.7+
    echo    下载地址: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM 显示Python版本
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python版本: %PYTHON_VERSION%

REM 检查是否在正确的目录
if not exist "main.py" (
    echo ❌ 请在项目根目录运行此脚本
    echo    当前目录: %CD%
    echo.
    pause
    exit /b 1
)

echo ✅ 项目目录检查通过
echo.

REM 检查.env文件是否存在
echo 🔍 检查环境配置...
if not exist ".env" (
    echo ⚠️ 未找到 .env 配置文件
    echo.
    echo 请选择以下操作:
    echo 1. 使用配置助手创建 .env 文件
    echo 2. 手动复制 .env.example 为 .env
    echo 3. 使用内置环境变量继续运行
    echo 4. 退出
    echo.
    set /p choice="请选择 (1-4): "
    
    if "!choice!"=="1" (
        echo.
        echo 🚀 启动配置助手...
        python setup_env.py
        if not exist ".env" (
            echo ❌ 配置助手未成功创建 .env 文件
            pause
            exit /b 1
        )
        echo ✅ .env 文件创建成功
    ) else if "!choice!"=="2" (
        if exist ".env.example" (
            copy ".env.example" ".env" >nul
            echo ✅ 已复制 .env.example 为 .env
            echo ⚠️ 请编辑 .env 文件，填入实际的API密钥
            echo    然后重新运行此脚本
            pause
            exit /b 0
        ) else (
            echo ❌ 未找到 .env.example 文件
            pause
            exit /b 1
        )
    ) else if "!choice!"=="3" (
        echo.
        echo 🔧 使用内置环境变量...
        goto SET_BUILTIN_ENV
    ) else (
        echo 退出程序
        exit /b 0
    )
) else (
    echo ✅ 找到 .env 配置文件
)

REM 如果有.env文件，使用Python加载环境变量
if exist ".env" (
    echo 📋 加载 .env 文件中的环境变量...
    goto START_PROGRAM
)

:SET_BUILTIN_ENV
echo.
echo 🔧 设置内置环境变量...

REM 基础AI配置
set "DASHSCOPE_API_KEY=sk-9bf124f946124600b9d70824998dc2a2"

REM 七牛云MCP配置
set "OPENAI_BASE_URL=https://openai.qiniu.com/v1/agent/instance/e033cb8893314147ad1488d92011ecd1"
set "OPENAI_API_KEY=sk-0863c31c6dbb697ed6d832e773a6ab6043d4e98d9cd2be952d6f16af10271058"
set "MCP_MODEL=deepseek-v3-tool"
set "USE_QINIU_MCP=true"

REM 传统高德API配置
set "AMAP_API_KEY=95fd23e5ff3e8d97d46b5c07f5077a4e"

REM 语音识别配置
set "XFYUN_APP_ID=f5df0409"
set "XFYUN_API_SECRET=YTgwNDFmYzc2MmVjMDQ0NDQ0OWQyNmJm"
set "XFYUN_API_KEY=654d10ef61d2357133a93d84e6278628"
set "USE_XFYUN_ASR=true"

REM 其他配置
set "QWEN_MODEL=qwen-max"
set "SPEECH_RECOGNITION_LANGUAGE=zh-CN"
set "SPEECH_TIMEOUT=5"
set "NAVIGATION_MODE=browser"

echo.
echo 📊 环境变量配置状态:
echo   ✅ DASHSCOPE_API_KEY: %DASHSCOPE_API_KEY:~0,8%...
echo   ⚠️ OPENAI_BASE_URL: %OPENAI_BASE_URL% (需要配置)
echo   ⚠️ OPENAI_API_KEY: %OPENAI_API_KEY% (需要配置)
echo   ✅ AMAP_API_KEY: %AMAP_API_KEY:~0,8%...
echo   ✅ 导航模式: %NAVIGATION_MODE%
echo   ✅ AI模型: %QWEN_MODEL%
echo   ✅ 语音识别: %USE_XFYUN_ASR% (科大讯飞)
echo.

:START_PROGRAM
REM 检查基础依赖
echo 📦 检查基础依赖...
python -c "import requests, asyncio" 2>nul
if errorlevel 1 (
    echo ❌ 缺少基础依赖包
    echo 🔧 正在安装依赖...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ 依赖安装失败，请手动运行: pip install -r requirements.txt
        pause
        exit /b 1
    )
    echo ✅ 依赖安装完成
)

echo ✅ 基础依赖检查通过
echo.

REM 启动程序
echo 🚀 启动高德地图语音导航助手...
echo ==========================================
echo.

REM 优先使用start.py启动（包含更好的错误处理）
if exist "start.py" (
    python start.py
) else (
    REM 如果start.py不存在，直接启动main.py
    python main.py
)

echo.
echo ==========================================
echo 程序已退出
echo ==========================================

REM 询问是否重新启动
echo.
set /p restart="是否重新启动程序? (y/n): "
if /i "%restart%"=="y" goto START_PROGRAM
if /i "%restart%"=="yes" goto START_PROGRAM

echo 👋 再见!
pause