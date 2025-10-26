@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
title 高德地图语音导航助手

echo 🚀 高德地图语音导航助手
echo ==========================================

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到Python
    pause
    exit /b 1
)

REM 检查.env文件
if not exist ".env" (
    echo ❌ 未找到 .env 配置文件
    if exist ".env.example" (
        echo 💡 复制 .env.example 为 .env...
        copy ".env.example" ".env" >nul
        echo ✅ 请编辑 .env 文件后重新运行
    )
    pause
    exit /b 1
)

REM 加载.env环境变量
echo 📋 加载环境变量...
for /f "usebackq tokens=1,2 delims==" %%a in (".env") do (
    set "line=%%a"
    if not "!line:~0,1!"=="#" if not "!line!"=="" (
        set "%%a=%%b"
    )
)

echo ✅ 环境变量已加载
echo.

REM 启动程序
python main.py

echo.
echo 程序已退出
pause