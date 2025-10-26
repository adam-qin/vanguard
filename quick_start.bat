@echo off
chcp 65001 >nul
cls
echo.
echo ==========================================
echo     高德地图语音导航助手 - 快速启动
echo ==========================================
echo.

REM 设置环境变量
set "DASHSCOPE_API_KEY=sk-xxx"
set "AMAP_API_KEY=xxx"
set "QWEN_MODEL=qwen-max"
set "SPEECH_RECOGNITION_LANGUAGE=zh-CN"
set "SPEECH_TIMEOUT=5"
set "NAVIGATION_MODE=browser"

REM 科大讯飞语音识别配置（暂时使用默认值，需要用户配置）
set "XFYUN_APP_ID=f5df0409"
set "XFYUN_API_SECRET=xxx"
set "XFYUN_API_KEY=xxx"
set "USE_XFYUN_ASR=true"



echo 环境变量已设置:
echo ✓ DASHSCOPE_API_KEY: %DASHSCOPE_API_KEY:~0,20%...
echo ✓ AMAP_API_KEY: %AMAP_API_KEY:~0,20%...
echo ✓ 导航模式: %NAVIGATION_MODE%
echo ✓ AI模型: %QWEN_MODEL%
echo ✓ 语音识别: %USE_XFYUN_ASR% (科大讯飞)
echo.

echo 正在启动程序...
echo.

REM 启动程序
D:\Program\python.exe main.py

echo.
echo ==========================================
echo 程序已退出
echo ==========================================

pause
