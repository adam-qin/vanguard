@echo off
chcp 65001 >nul
title 高德地图语音导航助手
echo.
echo ========================================
echo    高德地图语音导航助手
echo ========================================
echo.

REM 检查环境变量文件
if exist .env (
    echo 正在加载环境变量...
    for /f "usebackq tokens=1,2 delims==" %%a in (".env") do (
        if not "%%a"=="" if not "%%a"=="#" (
            set "%%a=%%b"
            echo 设置环境变量: %%a
        )
    )
    echo 环境变量加载完成
    echo.
) else (
    echo 警告: 未找到.env配置文件
    echo 请确保API密钥已正确配置
    echo.
)

REM 显示当前配置
echo 当前配置:
echo - 导航模式: %NAVIGATION_MODE%
echo - AI模型: %QWEN_MODEL%
echo - 语音语言: %SPEECH_RECOGNITION_LANGUAGE%
echo.

echo 正在启动程序...
echo.

REM 启动程序
D:\Program\python.exe main.py

echo.
echo ========================================
echo 程序已退出，按任意键关闭窗口...
echo ========================================
pause >nul