# 高德地图语音导航助手

一个基于AI的智能语音导航助手，支持七牛云MCP SERVER和传统高德API两种模式。

## ✨ 特性

- 🎤 **智能语音识别** - 支持科大讯飞和Google语音识别
- 🗺️ **双模式导航** - 七牛云MCP模式 + 传统MCP模式
- 🚀 **七牛云MCP** - 直接调用MCP SERVER获取坐标
- 🔄 **传统MCP** - 调用高德API获取坐标，通过浏览器打开导航
- 🎯 **精确定位** - 获取精确经纬度坐标
- 🔧 **灵活配置** - 支持多种配置方式

## 语音导航的商业价值：

- 提升用户体验
- 操作便捷：用户只需说出需求，无需手动输入或查找菜单，尤其在开车、忙碌等场景下更安全、高效。
- 快速响应：能快速识别用户意图，精准提供导航或相关服务，减少等待时间，提高服务满意度。
- 数据价值挖掘
- 分析用户行为：采集并分析用户的需求和行为数据，帮助了解用户痛点，为产品优化和服务改进提供依据。
- 拓展业务合作
- 多服务整合：可连接各类生活服务，如旅游、餐饮、家政等，实现多业务整合，为用户提供一站式解决方案，同时为企业带来更多合作机会和收入来源。

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

#### 方法1: 使用配置助手（推荐）

```bash
python setup_env.py
```

#### 方法2: 手动配置

```bash
cp .env.example .env
# 编辑 .env 文件，填入实际的API密钥
```

### 3. 启动程序

```bash
# 使用启动脚本（推荐）
python start.py

# 或直接运行主程序
python main.py

# Windows用户可以双击
start.bat
```

## 📋 环境变量配置

### 必需配置

```bash
# 基础AI配置（必需）
DASHSCOPE_API_KEY=your_dashscope_api_key
```

### 七牛云MCP配置

```bash
# 七牛云MCP SERVER配置
OPENAI_BASE_URL=https://your-qiniu-mcp-server.com
OPENAI_API_KEY=your_qiniu_mcp_api_key
MCP_MODEL=deepseek-v3-tool
USE_QINIU_MCP=true
```

### 传统高德API配置（备选）

```bash
# 传统高德地图API配置
AMAP_API_KEY=your_amap_api_key
```

### 语音识别配置（可选）

```bash
# 科大讯飞语音识别配置
XFYUN_APP_ID=your_xfyun_app_id
XFYUN_API_SECRET=your_xfyun_api_secret
XFYUN_API_KEY=your_xfyun_api_key
USE_XFYUN_ASR=true
```

## 🎯 使用方法

### 文字输入导航

```
> 从深圳湾科技生态园到学府路国兴苑
```

### 语音输入导航

```
> voice
[语音输入] 从深圳湾科技生态园到学府路国兴苑
```

### 切换导航客户端

```
> client
# 选择七牛云MCP模式或传统MCP模式
```

## 🔧 架构说明

### 七牛云MCP模式

```
用户输入 → AI提取地址 → 七牛云MCP SERVER → 获取坐标 → 构建导航URL → 打开浏览器
```

**特点:**
- ⚡ 响应快速 - 直接调用MCP SERVER
- 🎯 坐标精确 - 专业地理编码服务
- 🌐 网络依赖低 - 单次API调用
- 🔧 配置简单 - 只需MCP SERVER配置

### 传统MCP模式

```
用户输入 → AI处理 → 地址验证 → 高德API → 获取坐标 → 构建导航URL → 打开浏览器
```

**特点:**
- 🔄 兼容性好 - 使用成熟的高德API
- 📊 功能丰富 - 支持多种地理编码选项
- 🛠️ 可定制性强 - 可配置API参数
- 🌐 浏览器导航 - 自动打开高德地图导航

## 🧪 测试

### 测试七牛云MCP客户端

```bash
python test_qiniu_mcp.py
```

### 验证环境配置

```bash
python setup_env.py
# 选择选项 2 进行验证
```

### 测试环境变量加载

```bash
python env_loader.py
```

## 📁 项目结构

```
fellow-traveler/
├── main.py                 # 主程序入口
├── start.py                # 启动脚本
├── start.bat               # Windows启动脚本
├── qiniu_mcp_client.py     # 七牛云MCP客户端
├── mcp_client.py           # 传统MCP客户端
├── browser_navigator.py    # 浏览器导航模块
├── ai_processor.py         # AI处理模块
├── speech_handler.py       # 语音处理模块
├── env_loader.py           # 环境变量加载器
├── setup_env.py            # 环境配置助手
├── test_qiniu_mcp.py       # 七牛云MCP测试脚本
├── .env                    # 环境变量配置文件
├── .env.example            # 环境变量示例文件
├── config_example.py       # Python配置示例
├── requirements.txt        # 依赖包列表
├── README.md               # 项目说明
└── README_QINIU_MCP.md     # 七牛云MCP详细说明
```

## 🔍 故障排除

### 常见问题

1. **MCP SERVER连接失败**
   - 检查 `OPENAI_BASE_URL` 和 `OPENAI_API_KEY`
   - 确认网络连接正常
   - 验证MCP SERVER服务状态

2. **环境变量未加载**
   - 确认 `.env` 文件存在
   - 检查文件格式是否正确
   - 运行 `python env_loader.py` 测试

3. **语音识别失败**
   - 检查麦克风权限
   - 确认科大讯飞配置正确
   - 测试网络连接

4. **浏览器导航失败**
   - 确认默认浏览器设置
   - 检查高德地图URL格式
   - 验证坐标格式正确

### 获取帮助

- 查看详细日志输出
- 运行测试脚本诊断问题
- 检查环境变量配置
- 验证API密钥有效性

## 📊 性能对比

| 特性 | 七牛云MCP模式 | 传统MCP模式 |
|------|---------------|---------------|
| 响应速度 | ⚡ 快 | 🔄 中等 |
| 坐标精度 | 🎯 高 | 📍 中等 |
| 网络依赖 | 🌐 低 (单次调用) | 📡 中等 (多次调用) |
| 本地计算 | 💻 少 | 🖥️ 多 |
| 配置复杂度 | 🔧 低 | ⚙️ 中等 |
| 导航方式 | 🌐 浏览器打开 | 🌐 浏览器打开 |
| API依赖 | 📡 七牛云MCP | 🗺️ 高德API |

## 📝 更新日志

### v2.0.0
- ✨ 添加七牛云MCP客户端支持
- 🔧 新增环境变量加载器
- 🚀 添加配置助手和启动脚本
- 📊 改进错误处理和日志输出
- 🎯 优化用户体验

### v1.0.0
- 🎤 基础语音识别功能
- 🗺️ 传统高德API导航
- 🌐 浏览器导航支持

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📞 联系


如有问题，请提交Issue或联系开发团队。

