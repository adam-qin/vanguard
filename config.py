# 配置文件 - 统一从环境变量读取所有配置
import os

# 确保环境变量已加载
from env_loader import load_environment
load_environment()

# AI模型配置 - 阿里千问
DASHSCOPE_API_KEY = os.getenv('DASHSCOPE_API_KEY', '')
QWEN_MODEL = os.getenv('QWEN_MODEL', 'qwen-max')

# 高德地图配置
AMAP_API_KEY = os.getenv('AMAP_API_KEY', '')
AMAP_API_BASE_URL = os.getenv('AMAP_API_BASE_URL', 'https://restapi.amap.com/v3')
AMAP_REQUEST_TIMEOUT = int(os.getenv('AMAP_REQUEST_TIMEOUT', '10'))

# 语音识别配置
SPEECH_RECOGNITION_LANGUAGE = os.getenv('SPEECH_RECOGNITION_LANGUAGE', 'zh-CN')
SPEECH_TIMEOUT = int(os.getenv('SPEECH_TIMEOUT', '5'))

# 科大讯飞语音识别配置
XFYUN_APP_ID = os.getenv('XFYUN_APP_ID', '')
XFYUN_API_SECRET = os.getenv('XFYUN_API_SECRET', '')
XFYUN_API_KEY = os.getenv('XFYUN_API_KEY', '')
USE_XFYUN_ASR = os.getenv('USE_XFYUN_ASR', 'true').lower() == 'true'

# 七牛云MCP配置
OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL', '')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
MCP_MODEL = os.getenv('MCP_MODEL', 'deepseek-v3-tool')
USE_QINIU_MCP = os.getenv('USE_QINIU_MCP', 'false').lower() == 'true'

# 导航模式配置
NAVIGATION_MODE = os.getenv('NAVIGATION_MODE', 'browser')
BROWSER_NAVIGATION_ENABLED = os.getenv('BROWSER_NAVIGATION_ENABLED', 'true').lower() == 'true'

# 默认城市配置
DEFAULT_CITY = os.getenv('DEFAULT_CITY', '深圳市')

# 系统提示词
SYSTEM_PROMPT = f"""
你是一个导航助手，负责解析用户的导航需求。
用户会说出从A地到B地的导航请求，你需要提取出起点和终点信息。

请严格按照以下JSON格式返回，不要包含任何其他文字：
{{
    "origin": "起点地址",
    "destination": "终点地址",
    "action": "navigation"
}}

地址格式规则：
1. 如果用户没有明确说明起点，使用"当前位置"作为起点
2. 地址必须采用"城市+区域+具体地址"的格式
3. 如果地址中缺少城市信息，必须在最前面加上"{DEFAULT_CITY}"
4. 正确格式示例：
   - "{DEFAULT_CITY}南山区学府路国兴苑"
   - "{DEFAULT_CITY}深圳湾科技生态园"
   - "{DEFAULT_CITY}福田区市民中心"
5. 错误格式（禁止使用）：
   - "学府路国兴苑, {DEFAULT_CITY}"
   - "南山区学府路国兴苑, {DEFAULT_CITY}"
6. 只返回JSON格式，不要添加解释文字
7. 如果无法解析，返回：{{"error": "无法解析导航请求"}}

当前默认城市：{DEFAULT_CITY}
"""

# 配置验证函数
def validate_config():
    """验证关键配置项"""
    missing_configs = []
    
    if not DASHSCOPE_API_KEY:
        missing_configs.append('DASHSCOPE_API_KEY')
    
    if not AMAP_API_KEY and not (OPENAI_BASE_URL and OPENAI_API_KEY):
        missing_configs.append('AMAP_API_KEY 或 七牛云MCP配置')
    
    if USE_XFYUN_ASR and not all([XFYUN_APP_ID, XFYUN_API_SECRET, XFYUN_API_KEY]):
        missing_configs.append('科大讯飞语音配置 (XFYUN_*)')
    
    return missing_configs

# 获取配置摘要
def get_config_summary():
    """获取配置摘要"""
    return {
        'ai_model': QWEN_MODEL,
        'default_city': DEFAULT_CITY,
        'navigation_mode': NAVIGATION_MODE,
        'speech_language': SPEECH_RECOGNITION_LANGUAGE,
        'use_xfyun_asr': USE_XFYUN_ASR,
        'use_qiniu_mcp': USE_QINIU_MCP,
        'browser_navigation': BROWSER_NAVIGATION_ENABLED,
        'dashscope_configured': bool(DASHSCOPE_API_KEY),
        'amap_configured': bool(AMAP_API_KEY),
        'qiniu_mcp_configured': bool(OPENAI_BASE_URL and OPENAI_API_KEY),
        'xfyun_configured': bool(XFYUN_APP_ID and XFYUN_API_SECRET and XFYUN_API_KEY)
    }