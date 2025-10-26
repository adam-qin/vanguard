# 高德地图语音导航助手启动脚本 (PowerShell版本)
# 设置控制台编码
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$Host.UI.RawUI.WindowTitle = "高德地图语音导航助手"

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "     高德地图语音导航助手" -ForegroundColor Yellow
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# 检查Python
Write-Host "🔍 检查Python环境..." -ForegroundColor Blue
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ $pythonVersion" -ForegroundColor Green
    } else {
        throw "Python not found"
    }
} catch {
    Write-Host "❌ 未找到Python，请先安装Python 3.7+" -ForegroundColor Red
    Write-Host "   下载地址: https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "按回车键退出"
    exit 1
}

# 检查项目目录
if (-not (Test-Path "main.py")) {
    Write-Host "❌ 请在项目根目录运行此脚本" -ForegroundColor Red
    Write-Host "   当前目录: $PWD" -ForegroundColor Yellow
    Read-Host "按回车键退出"
    exit 1
}

Write-Host "✅ 项目目录检查通过" -ForegroundColor Green

# 检查.env文件
Write-Host ""
Write-Host "📋 检查环境配置文件..." -ForegroundColor Blue

if (-not (Test-Path ".env")) {
    Write-Host "❌ 未找到 .env 配置文件" -ForegroundColor Red
    
    if (Test-Path ".env.example") {
        Write-Host "💡 发现 .env.example 文件" -ForegroundColor Yellow
        $copyEnv = Read-Host "是否复制 .env.example 为 .env? (y/n)"
        
        if ($copyEnv -eq "y" -or $copyEnv -eq "Y") {
            Copy-Item ".env.example" ".env"
            Write-Host "✅ 已复制 .env.example 为 .env" -ForegroundColor Green
            Write-Host "⚠️ 请编辑 .env 文件，填入实际的API密钥" -ForegroundColor Yellow
            Write-Host "   然后重新运行此脚本" -ForegroundColor Yellow
            Read-Host "按回车键退出"
            exit 0
        }
    }
    
    Write-Host ""
    Write-Host "请创建 .env 文件并配置以下环境变量:" -ForegroundColor Yellow
    Write-Host "  DASHSCOPE_API_KEY=your_dashscope_api_key" -ForegroundColor Gray
    Write-Host "  AMAP_API_KEY=your_amap_api_key" -ForegroundColor Gray
    Write-Host "  OPENAI_BASE_URL=your_qiniu_mcp_server_url" -ForegroundColor Gray
    Write-Host "  OPENAI_API_KEY=your_qiniu_mcp_api_key" -ForegroundColor Gray
    Read-Host "按回车键退出"
    exit 1
}

Write-Host "✅ 找到 .env 配置文件" -ForegroundColor Green

# 加载.env文件中的环境变量
Write-Host "🔧 加载环境变量..." -ForegroundColor Blue

try {
    $envContent = Get-Content ".env" -ErrorAction Stop
    $loadedVars = 0
    
    foreach ($line in $envContent) {
        $line = $line.Trim()
        
        # 跳过注释行和空行
        if ($line -and -not $line.StartsWith("#")) {
            if ($line -match "^([^=]+)=(.*)$") {
                $key = $matches[1].Trim()
                $value = $matches[2].Trim()
                
                # 移除引号
                if ($value.StartsWith('"') -and $value.EndsWith('"')) {
                    $value = $value.Substring(1, $value.Length - 2)
                } elseif ($value.StartsWith("'") -and $value.EndsWith("'")) {
                    $value = $value.Substring(1, $value.Length - 2)
                }
                
                # 设置环境变量
                [Environment]::SetEnvironmentVariable($key, $value, "Process")
                
                # 显示非敏感的环境变量
                if ($key -notmatch "KEY|SECRET|TOKEN") {
                    Write-Host "   ✓ $key" -ForegroundColor Gray
                } else {
                    Write-Host "   ✓ $key (已设置)" -ForegroundColor Gray
                }
                
                $loadedVars++
            }
        }
    }
    
    Write-Host "✅ 成功加载 $loadedVars 个环境变量" -ForegroundColor Green
    
} catch {
    Write-Host "❌ 加载环境变量失败: $($_.Exception.Message)" -ForegroundColor Red
    Read-Host "按回车键退出"
    exit 1
}

# 检查基础依赖
Write-Host ""
Write-Host "📦 检查基础依赖..." -ForegroundColor Blue

try {
    python -c "import requests, asyncio" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ 基础依赖检查通过" -ForegroundColor Green
    } else {
        Write-Host "❌ 缺少基础依赖包" -ForegroundColor Red
        Write-Host "🔧 正在安装依赖..." -ForegroundColor Yellow
        
        pip install -r requirements.txt
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ 依赖安装失败，请手动运行: pip install -r requirements.txt" -ForegroundColor Red
            Read-Host "按回车键退出"
            exit 1
        }
        Write-Host "✅ 依赖安装完成" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ 依赖检查失败" -ForegroundColor Red
    Read-Host "按回车键退出"
    exit 1
}

# 启动程序
Write-Host ""
Write-Host "🚀 启动高德地图语音导航助手..." -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

try {
    python main.py
} catch {
    Write-Host "❌ 程序运行出错: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "程序已退出" -ForegroundColor Yellow
Write-Host "==========================================" -ForegroundColor Cyan

# 询问是否重新启动
Write-Host ""
$restart = Read-Host "是否重新启动程序? (y/n)"
if ($restart -eq "y" -or $restart -eq "Y") {
    Write-Host ""
    Write-Host "🔄 重新启动程序..." -ForegroundColor Blue
    python main.py
}

Write-Host "👋 再见!" -ForegroundColor Green
Read-Host "按回车键退出"