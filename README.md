# 高德地图语音导航助手

基于高德地图MCP Server的Python程序，支持文字和语音输入，通过AI大模型解析用户需求并自动调用高德地图进行导航。

## 功能特性

- 🎤 **语音输入支持**: 使用麦克风进行语音输入
- 💬 **文字输入支持**: 支持键盘文字输入
- 🤖 **AI智能解析**: 使用阿里千问qwen-max模型解析用户导航需求
- 🌐 **浏览器导航**: 直接调用浏览器打开高德地图并自动进入导航状态
- 🗺️ **MCP Server集成**: 备选的MCP Server调用方式
- 🔊 **语音反馈**: 文字转语音播报操作结果
- ⚙️ **双模式支持**: 支持浏览器导航和MCP服务器导航两种模式

## 系统要求

- Python 3.8+
- Windows 10/11
- 麦克风设备（语音输入）
- 网络连接

## 安装步骤

### 1. 克隆项目
```bash
git clone <repository-url>
cd amap-voice-navigation
```

### 2. 安装Python依赖
```bash
pip install -r requirements.txt
```

### 3. 安装uv和uvx（用于MCP Server）
```bash
# 使用pip安装uv
pip install uv

# 或者从官网下载安装
# https://docs.astral.sh/uv/getting-started/installation/
```

### 4. 设置环境变量
创建 `.env` 文件或设置系统环境变量：

```bash
# 阿里千问API密钥
set DASHSCOPE_API_KEY=your-dashscope-api-key

# 高德地图API密钥
set AMAP_API_KEY=your-amap-api-key

# 科大讯飞语音API密钥
set XFYUN_APP_ID=your-xfyun-app-id
set XFYUN_API_SECRET=your-xfyun-api-secret
set XFYUN_API_KEY=your-xfyun-api-key
```

#### 获取API密钥：
- **阿里千问API**: 访问 [阿里云百炼平台](https://bailian.console.aliyun.com/) 获取DashScope API Key
- **高德地图API**: 访问 [高德开放平台](https://lbs.amap.com/dev/key/app)
- **科大讯飞语音API**: 访问 [科大讯飞开放平台](https://www.xfyun.cn/) 获取语音识别API密钥

## 使用方法

### 启动程序
```bash
python main.py
```

### 使用示例

#### 文字输入示例：
```
> 从北京到上海导航
> 去天安门怎么走
> 导航到首都机场
```

#### 语音输入：
```
> voice
[程序会提示开始语音输入]
说话: "从家里到公司导航"
```

#### 切换导航模式：
```
> mode
[选择浏览器导航或MCP服务器导航]
```

#### 导航模式说明：
- **浏览器导航模式** (推荐): 直接调用系统默认浏览器打开高德地图，自动构建导航URL并进入导航状态
- **MCP服务器模式**: 通过MCP Server调用高德地图API（需要额外配置）

### 支持的输入格式

- "从A到B导航"
- "去A怎么走"
- "导航到A"
- "A到B的路线"
- "我要去A"

## 项目结构

```
amap-voice-navigation/
├── main.py              # 主程序入口
├── config.py            # 配置文件
├── speech_handler.py    # 语音处理模块
├── ai_processor.py      # AI处理模块
├── mcp_client.py        # MCP客户端
├── browser_navigator.py # 浏览器导航模块
├── requirements.txt     # Python依赖
├── setup.py            # 安装脚本
├── install.bat         # Windows安装脚本
├── run.bat             # Windows运行脚本
└── README.md           # 说明文档
```

## 配置说明

### config.py 主要配置项：

- `DASHSCOPE_API_KEY`: 阿里千问API密钥
- `QWEN_MODEL`: 使用的AI模型（默认: qwen-max）
- `AMAP_API_KEY`: 高德地图API密钥
- `SPEECH_RECOGNITION_LANGUAGE`: 语音识别语言（默认: zh-CN）
- `SPEECH_TIMEOUT`: 语音输入超时时间（默认: 5秒）

## 故障排除

### 常见问题

1. **麦克风不工作**
   - 检查麦克风权限设置
   - 确认麦克风设备正常工作
   - 尝试重新安装pyaudio

2. **语音识别失败**
   - 检查网络连接
   - 确认语音清晰度
   - 调整麦克风音量

3. **MCP Server启动失败**
   - 确认uv和uvx已正确安装
   - 检查高德地图API密钥是否有效
   - 查看网络连接状态

4. **AI处理失败**
   - 检查阿里千问API密钥是否有效
   - 确认API配额是否充足
   - 检查网络连接

### 依赖安装问题

如果遇到pyaudio安装问题，可以尝试：

```bash
# Windows
pip install pipwin
pipwin install pyaudio

# 或者下载预编译的wheel文件
pip install https://download.lfd.uci.edu/pythonlibs/archived/pyaudio-0.2.11-cp39-cp39-win_amd64.whl
```

## 开发说明

### 扩展功能

1. **添加新的输入格式**: 修改 `ai_processor.py` 中的正则表达式
2. **支持更多导航模式**: 在 `mcp_client.py` 中添加新的导航模式
3. **添加语音命令**: 扩展 `speech_handler.py` 的功能

### 测试

```bash
# 测试麦克风
python -c "from speech_handler import SpeechHandler; sh = SpeechHandler(); sh.test_microphone()"

# 测试AI处理
python -c "from ai_processor import AIProcessor; ai = AIProcessor(); print(ai.process_navigation_request('从北京到上海'))"
```

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request来改进这个项目。

## 联系方式

如有问题，请通过以下方式联系：
- 邮箱: qinxiuke@qiniu.com

- GitHub Issues: [项目Issues页面]
