# 配置文件
import os

# AI模型配置 - 阿里千问
DASHSCOPE_API_KEY = os.getenv('DASHSCOPE_API_KEY', 'sk-xxx')
QWEN_MODEL = 'qwen-max'

# 高德地图配置
AMAP_API_KEY = os.getenv('AMAP_API_KEY', 'xxx')

# 高德MCP服务器配置
AMAP_MCP_BASE_URL = f'https://mcp.amap.com/mcp?key={AMAP_API_KEY}'
MCP_REQUEST_TIMEOUT = 10  # MCP请求超时时间（秒）

# 语音识别配置
SPEECH_RECOGNITION_LANGUAGE = 'zh-CN'
SPEECH_TIMEOUT = 5  # 语音输入超时时间（秒）

# 科大讯飞语音识别配置
XFYUN_APP_ID = os.getenv('XFYUN_APP_ID', 'your-xfyun-app-id')
XFYUN_API_SECRET = os.getenv('XFYUN_API_SECRET', 'your-xfyun-api-secret')
XFYUN_API_KEY = os.getenv('XFYUN_API_KEY', 'your-xfyun-api-key')
USE_XFYUN_ASR = os.getenv('USE_XFYUN_ASR', 'true').lower() == 'true'

# 导航模式配置
NAVIGATION_MODE = os.getenv('NAVIGATION_MODE', 'browser')  # 'browser' 或 'mcp'
BROWSER_NAVIGATION_ENABLED = True

# 系统提示词
SYSTEM_PROMPT = """
你是一个导航助手，负责解析用户的导航需求。
用户会说出从A地到B地的导航请求，你需要提取出起点和终点信息。

请严格按照以下JSON格式返回，不要包含任何其他文字：
{
    "origin": "起点地址",
    "destination": "终点地址",
    "action": "navigation"
}

规则：
1. 如果用户没有明确说明起点，使用"当前位置"作为起点
2. 地址要尽可能具体和准确
3. 只返回JSON格式，不要添加解释文字
4. 如果无法解析，返回：{"error": "无法解析导航请求"}
5. 如果起点或终点当中不存在具体的城市，请从存在的地址当中自动提取加入
6. 当前默认位置为深圳市
"""