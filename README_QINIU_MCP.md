# 七牛云高德MCP客户端使用说明

## 概述

本项目现在支持两种MCP客户端：
1. **七牛云MCP客户端** - 直接调用七牛云的高德MCP SERVER
2. **传统MCP客户端** - 使用本地AI处理 + 高德API

## 七牛云MCP客户端特点

- 🚀 **直接调用**: 跳过本地AI预处理，直接调用七牛云MCP SERVER
- 🎯 **精确坐标**: 通过MCP SERVER获取精确的经纬度坐标
- 🌐 **高德导航**: 自动构建高德地图导航URL并打开浏览器
- ⚡ **高效处理**: 减少本地计算，提高响应速度

## 环境配置

### 快速配置

使用配置助手快速设置环境变量：

```bash
python setup_env.py
```

### 手动配置

#### 方法1: 使用 .env 文件（推荐）

复制示例文件并编辑：

```bash
cp .env.example .env
# 然后编辑 .env 文件，填入实际的API密钥
```

.env 文件格式：

```bash
# 基础AI配置（必需）
DASHSCOPE_API_KEY=your_dashscope_api_key

# 七牛云MCP配置
OPENAI_BASE_URL=https://your-qiniu-mcp-server.com
OPENAI_API_KEY=your_qiniu_mcp_api_key
MCP_MODEL=deepseek-v3-tool
USE_QINIU_MCP=true

# 传统高德API配置（可选）
AMAP_API_KEY=your_amap_api_key

# 语音识别配置（可选）
XFYUN_APP_ID=your_xfyun_app_id
XFYUN_API_SECRET=your_xfyun_api_secret
XFYUN_API_KEY=your_xfyun_api_key
USE_XFYUN_ASR=true
```

#### 方法2: 系统环境变量

```bash
# 基础配置
export DASHSCOPE_API_KEY="your_dashscope_api_key"

# 七牛云MCP配置
export OPENAI_BASE_URL="https://your-qiniu-mcp-server.com"
export OPENAI_API_KEY="your_qiniu_mcp_api_key"
export MCP_MODEL="deepseek-v3-tool"
export USE_QINIU_MCP="true"

# 传统MCP配置（可选）
export AMAP_API_KEY="your_amap_api_key"
```

### 配置验证

验证配置是否正确：

```bash
python setup_env.py
# 选择选项 2 进行验证
```

或者直接测试七牛云MCP：

```bash
python test_qiniu_mcp.py
```

## 使用方法

### 1. 启动程序

```bash
python main.py
```

### 2. 选择MCP客户端

程序启动时会自动检测可用的MCP客户端：
- 如果七牛云MCP可用，优先使用
- 否则使用传统MCP作为备选

手动切换客户端：
```
输入 'client' 切换MCP客户端
```

### 3. 导航使用

#### 文字输入导航
```
> 从深圳湾科技生态园到学府路国兴苑
```

#### 语音输入导航
```
> voice
[语音输入] 从深圳湾科技生态园到学府路国兴苑
```

## API调用流程

### 七牛云MCP流程

```
用户输入 -> AI提取地址 -> 七牛云MCP SERVER -> 获取坐标 -> 构建导航URL -> 打开浏览器
```

### 传统MCP流程

```
用户输入 -> AI处理 -> 地址验证 -> 高德API -> 获取坐标 -> 构建导航URL -> 打开浏览器
```

## 七牛云MCP SERVER调用示例

### 请求格式

```bash
curl "$OPENAI_BASE_URL/v1/chat/completions" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $OPENAI_API_KEY" \
    -d '{
        "messages": [
            {
                "role": "user", 
                "content": "从深圳湾科技生态园导航到学府路国兴苑,给出源地址和目标地址的坐标"
            }
        ],
        "model": "deepseek-v3-tool"
    }'
```

### 响应格式

```json
{
    "choices": [{
        "message": {
            "content": "- 源地址（深圳湾科技生态园）的坐标：`113.952743,22.530351`\n- 目标地址（学府路国兴苑）的坐标：`113.919645,22.528367`",
            "tool_calls": [
                {
                    "function": {
                        "name": "maps_geo",
                        "arguments": "{\"address\": \"深圳湾科技生态园\"}"
                    }
                }
            ]
        }
    }],
    "tool_references": [
        {
            "content": "{\"content\":[{\"type\":\"text\",\"text\":\"{\\\"return\\\": [{\\\"location\\\": \\\"113.952743,22.530351\\\"}]}\"}]}"
        }
    ]
}
```

## 测试

### 测试七牛云MCP客户端

```bash
python test_qiniu_mcp.py
```

### 测试内容

1. MCP SERVER连接测试
2. 坐标获取测试
3. 导航URL构建测试
4. 完整导航流程测试
5. 客户端信息显示

## 故障排除

### 常见问题

1. **MCP SERVER连接失败**
   - 检查 `OPENAI_BASE_URL` 和 `OPENAI_API_KEY` 是否正确
   - 确认网络连接正常
   - 验证MCP SERVER服务状态

2. **坐标获取失败**
   - 检查地址名称是否准确
   - 确认MCP SERVER的maps_geo工具可用
   - 查看详细错误日志

3. **浏览器导航失败**
   - 确认系统默认浏览器设置
   - 检查高德地图URL格式
   - 验证坐标格式正确性

### 日志分析

程序会输出详细的执行日志：
- `🌐 调用七牛云MCP SERVER获取坐标...` - MCP调用开始
- `✅ 起点坐标: xxx,xxx` - 坐标获取成功
- `🔗 构建高德地图导航URL...` - URL构建过程
- `🌐 打开浏览器导航...` - 浏览器启动

## 配置文件

复制 `config_example.py` 为 `config.py` 并填入实际配置：

```python
# 七牛云MCP SERVER配置
OPENAI_BASE_URL = "https://your-mcp-server.com"
OPENAI_API_KEY = "your_api_key"

# 传统高德API配置（可选）
AMAP_API_KEY = "your_amap_key"

# 基础AI配置
DASHSCOPE_API_KEY = "your_dashscope_key"
```

## 性能优势

### 七牛云MCP vs 传统MCP

| 特性 | 七牛云MCP | 传统MCP |
|------|-----------|---------|
| 响应速度 | 快 | 中等 |
| 坐标精度 | 高 | 中等 |
| 网络依赖 | 低 | 高 |
| 本地计算 | 少 | 多 |
| 配置复杂度 | 低 | 中等 |

## 更新日志

- **v2.0** - 添加七牛云MCP客户端支持
- **v1.0** - 基础传统MCP功能