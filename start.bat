@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
title 高德地图语音导航助手

echo.
echo ==========================================
echo     高德地图语音导航助手
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

REM 检查.env文件是否存在
echo.
echo 📋 检查环境配置文件...
if not exist ".env" (
    echo ❌ 未找到 .env 配置文件
    echo.
    if exist ".env.example" (
        echo 💡 发现 .env.example 文件
        set /p copy_env="是否复制 .env.example 为 .env? (y/n): "
        if /i "!copy_env!"=="y" (
            copy ".env.example" ".env" >nul
            echo ✅ 已复制 .env.example 为 .env
            echo ⚠️ 请编辑 .env 文件，填入实际的API密钥
            echo    然后重新运行此脚本
            pause
            exit /b 0
        )
    )
    echo.
    echo 请创建 .env 文件并配置以下环境变量:
    echo   DASHSCOPE_API_KEY=your_dashscope_api_key
    echo   AMAP_API_KEY=your_amap_api_key
    echo   OPENAI_BASE_URL=your_qiniu_mcp_server_url
    echo   OPENAI_API_KEY=your_qiniu_mcp_api_key
    echo.
    pause
    exit /b 1
)

echo ✅ 找到 .env 配置文件

REM 从.env文件加载环境变量
echo 🔧 加载环境变量...
for /f "usebackq tokens=1,2 delims==" %%a in (".env") do (
    set "line=%%a"
    REM 跳过注释行和空行
    if not "!line:~0,1!"=="#" if not "!line!"=="" (
        set "%%a=%%b"
        REM 显示非敏感的环境变量
        echo    ✓ %%a
    )
)

echo ✅ 环境变量加载完成

REM 检查基础依赖
echo.
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
) else (
    echo ✅ 基础依赖检查通过
)

REM 启动程序
echo.
echo 🚀 启动高德地图语音导航助手...
echo ==========================================
echo.

python main.py

echo.
echo ==========================================
echo 程序已退出
echo ==========================================

REM 询问是否重新启动
echo.
set /p restart="是否重新启动程序? (y/n): "
if /i "%restart%"=="y" goto :start_program
if /i "%restart%"=="yes" goto :start_program

echo 👋 再见!
pause
exit /b 0

:start_program
echo.
echo 🔄 重新启动程序...
python main.py
goto :end_program

:end_program
echo.
set /p restart="是否再次重新启动程序? (y/n): "
if /i "%restart%"=="y" goto :start_program
if /i "%restart%"=="yes" goto :start_program

echo 👋 再见!
pause