#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环境变量配置助手
帮助用户快速配置 .env 文件
"""

import os
import shutil
from typing import Dict, List

def create_env_file():
    """创建 .env 文件"""
    print("=== 高德地图语音导航助手 - 环境配置 ===")
    print()
    
    # 检查是否已存在 .env 文件
    if os.path.exists('.env'):
        print("发现现有的 .env 文件")
        choice = input("是否要备份现有文件并重新配置? (y/n): ").strip().lower()
        if choice in ['y', 'yes']:
            # 备份现有文件
            backup_name = '.env.backup'
            counter = 1
            while os.path.exists(backup_name):
                backup_name = f'.env.backup.{counter}'
                counter += 1
            
            shutil.copy('.env', backup_name)
            print(f"✅ 现有 .env 文件已备份为: {backup_name}")
        else:
            print("保持现有配置，退出设置")
            return
    
    # 配置项定义
    config_sections = {
        "基础AI配置": {
            "DASHSCOPE_API_KEY": {
                "description": "阿里云通义千问API密钥",
                "required": True,
                "example": "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
            }
        },
        "七牛云MCP配置": {
            "OPENAI_BASE_URL": {
                "description": "七牛云MCP服务器地址",
                "required": False,
                "example": "https://your-mcp-server.com"
            },
            "OPENAI_API_KEY": {
                "description": "七牛云MCP API密钥",
                "required": False,
                "example": "your-mcp-api-key"
            },
            "MCP_MODEL": {
                "description": "MCP模型名称",
                "required": False,
                "default": "deepseek-v3-tool"
            },
            "USE_QINIU_MCP": {
                "description": "是否启用七牛云MCP",
                "required": False,
                "default": "true",
                "type": "bool"
            }
        },
        "传统高德API配置": {
            "AMAP_API_KEY": {
                "description": "高德地图API密钥",
                "required": False,
                "example": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
            }
        },
        "语音识别配置": {
            "XFYUN_APP_ID": {
                "description": "科大讯飞应用ID",
                "required": False,
                "example": "xxxxxxxx"
            },
            "XFYUN_API_SECRET": {
                "description": "科大讯飞API密钥",
                "required": False,
                "example": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
            },
            "XFYUN_API_KEY": {
                "description": "科大讯飞API Key",
                "required": False,
                "example": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
            },
            "USE_XFYUN_ASR": {
                "description": "是否启用科大讯飞语音识别",
                "required": False,
                "default": "true",
                "type": "bool"
            }
        },
        "其他配置": {
            "QWEN_MODEL": {
                "description": "通义千问模型",
                "required": False,
                "default": "qwen-max"
            },
            "SPEECH_RECOGNITION_LANGUAGE": {
                "description": "语音识别语言",
                "required": False,
                "default": "zh-CN"
            },
            "SPEECH_TIMEOUT": {
                "description": "语音超时时间(秒)",
                "required": False,
                "default": "5"
            },
            "NAVIGATION_MODE": {
                "description": "导航模式",
                "required": False,
                "default": "browser"
            }
        }
    }
    
    # 收集配置
    env_content = []
    env_content.append("# 高德地图语音导航助手配置文件")
    env_content.append("# 自动生成于环境配置助手")
    env_content.append("")
    
    for section_name, section_config in config_sections.items():
        print(f"\n--- {section_name} ---")
        env_content.append(f"# {section_name}")
        
        for key, config in section_config.items():
            description = config.get("description", "")
            required = config.get("required", False)
            default = config.get("default", "")
            example = config.get("example", "")
            var_type = config.get("type", "string")
            
            # 显示配置项信息
            print(f"\n{key}:")
            print(f"  说明: {description}")
            if required:
                print("  状态: 必需")
            else:
                print("  状态: 可选")
            if default:
                print(f"  默认值: {default}")
            if example:
                print(f"  示例: {example}")
            
            # 获取用户输入
            if required:
                prompt = f"请输入 {key}"
            else:
                prompt = f"请输入 {key} (回车跳过)"
            
            if default:
                prompt += f" [默认: {default}]"
            
            prompt += ": "
            
            value = input(prompt).strip()
            
            # 处理默认值
            if not value and default:
                value = default
            
            # 处理布尔类型
            if var_type == "bool" and value:
                value = value.lower()
                if value in ['true', '1', 'yes', 'on']:
                    value = 'true'
                elif value in ['false', '0', 'no', 'off']:
                    value = 'false'
                else:
                    value = 'true'  # 默认为true
            
            # 添加到配置文件
            if value:
                env_content.append(f"{key}={value}")
            else:
                env_content.append(f"# {key}=")
        
        env_content.append("")
    
    # 写入 .env 文件
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write('\n'.join(env_content))
        
        print("\n✅ .env 文件创建成功!")
        print("📁 文件位置: .env")
        
        # 显示配置摘要
        print("\n📊 配置摘要:")
        with open('.env', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    if value:
                        # 隐藏敏感信息
                        if 'KEY' in key or 'SECRET' in key:
                            if len(value) > 12:
                                display_value = value[:4] + '...' + value[-4:]
                            else:
                                display_value = '***'
                        else:
                            display_value = value
                        print(f"  ✅ {key}: {display_value}")
                    else:
                        print(f"  ⚪ {key}: 未设置")
        
        print("\n🚀 配置完成! 现在可以运行程序:")
        print("   python main.py")
        
    except Exception as e:
        print(f"\n❌ 创建 .env 文件失败: {e}")

def validate_env_file():
    """验证 .env 文件配置"""
    if not os.path.exists('.env'):
        print("❌ .env 文件不存在")
        return False
    
    print("🔍 验证 .env 文件配置...")
    
    # 加载环境变量
    from env_loader import load_environment, EnvLoader
    load_environment()
    
    # 显示状态
    EnvLoader.print_env_status()
    
    # 检查关键配置
    issues = []
    
    # 检查基础配置
    if not os.getenv('DASHSCOPE_API_KEY'):
        issues.append("缺少 DASHSCOPE_API_KEY (必需)")
    
    # 检查MCP配置
    qiniu_url = os.getenv('OPENAI_BASE_URL')
    qiniu_key = os.getenv('OPENAI_API_KEY')
    amap_key = os.getenv('AMAP_API_KEY')
    
    if not qiniu_url or not qiniu_key:
        if not amap_key:
            issues.append("七牛云MCP和传统高德API都未配置，至少需要配置一个")
    
    if issues:
        print("\n⚠️ 发现配置问题:")
        for issue in issues:
            print(f"   - {issue}")
        return False
    else:
        print("\n✅ 配置验证通过!")
        return True

def main():
    """主函数"""
    print("高德地图语音导航助手 - 环境配置助手")
    print()
    print("选择操作:")
    print("1. 创建新的 .env 配置文件")
    print("2. 验证现有 .env 配置文件")
    print("3. 退出")
    
    choice = input("\n请选择 (1-3): ").strip()
    
    if choice == '1':
        create_env_file()
    elif choice == '2':
        validate_env_file()
    elif choice == '3':
        print("退出配置助手")
    else:
        print("无效选择")

if __name__ == "__main__":
    main()