@echo off
chcp 65001 >nul
title 快速安装 - 高德地图语音导航助手

echo 快速安装高德地图语音导航助手
echo ==========================================

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python
    pause
    exit /b 1
)

echo 成功: Python检查通过

REM 安装依赖
echo 正在安装依赖包...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo 错误: 依赖安装失败
    pause
    exit /b 1
)

echo 成功: 依赖安装完成

REM 创建配置文件
if not exist .env (
    if exist .env.example (
        copy .env.example .env >nul
        echo 成功: 已创建 .env 配置文件
    )
)

echo.
echo 安装完成！
echo.
echo 下一步操作:
echo 1. 编辑 .env 文件，填入API密钥
echo 2. 运行程序: python main.py
echo 3. 或使用启动脚本: start.bat
echo.
pause