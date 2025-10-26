# 配置文件示例 (Python格式)
# 请复制此文件为 config.py 并填入您的实际配置
# 注意: 推荐使用 .env 文件进行配置

# 基础AI配置
DASHSCOPE_API_KEY = "your_dashscope_api_key_here"

# 七牛云MCP SERVER配置
OPENAI_BASE_URL = "your_qiniu_mcp_server_url_here"  # 例如: https://api.example.com
OPENAI_API_KEY = "your_qiniu_mcp_api_key_here"
MCP_MODEL = "deepseek-v3-tool"
USE_QINIU_MCP = True

# 传统高德地图API配置
AMAP_API_KEY = "your_amap_api_key_here"

# 语音配置
XFYUN_APP_ID = "your_xfyun_app_id_here"
XFYUN_API_SECRET = "your_xfyun_api_secret_here"
XFYUN_API_KEY = "your_xfyun_api_key_here"
USE_XFYUN_ASR = True

# 其他配置
QWEN_MODEL = "qwen-max"
SPEECH_RECOGNITION_LANGUAGE = "zh-CN"
SPEECH_TIMEOUT = 5
NAVIGATION_MODE = "browser"