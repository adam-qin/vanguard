from setuptools import setup, find_packages

setup(
    name="amap-voice-navigation",
    version="1.0.0",
    description="基于高德地图MCP Server的语音导航助手",
    author="Your Name",
    author_email="qinxiuke@qiniu.com",
    packages=find_packages(),
    install_requires=[
        "SpeechRecognition>=3.8.0",
        "edge-tts>=6.1.0",
        "pygame>=2.6.0",
        "pywin32>=308",
        "dashscope>=1.17.0",
        "requests>=2.31.0",
        "pyaudio>=0.2.11",
        "urllib3>=2.0.0",
        "websocket-client>=1.0.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)