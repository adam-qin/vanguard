@echo off
echo 正在安装高德地图语音导航助手...
echo.

REM 检查Python是否安装
D:\Program\python.exe --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请检查D:\Program\python.exe是否存在
    pause
    exit /b 1
)

echo 1. 安装Python依赖包...
D:\Program\python.exe -m pip install -r requirements.txt
if errorlevel 1 (
    echo 错误: 依赖包安装失败
    pause
    exit /b 1
)

echo.
echo 2. 安装uv包管理器...
D:\Program\python.exe -m pip install uv
if errorlevel 1 (
    echo 警告: uv安装失败，请手动安装
)

echo.
echo 3. 创建环境变量配置文件...
if not exist .env (
    echo # 请填入您的API密钥 > .env
    echo DASHSCOPE_API_KEY=your-dashscope-api-key >> .env
    echo AMAP_API_KEY=your-amap-api-key >> .env
    echo.
    echo 已创建 .env 文件，请编辑并填入您的API密钥
)

echo.
echo 安装完成！
echo.
echo 使用前请确保：
echo 1. 编辑 .env 文件，填入正确的API密钥
echo 2. 确保麦克风设备正常工作
echo 3. 确保网络连接正常
echo.
echo 运行程序: python main.py
echo.
pause