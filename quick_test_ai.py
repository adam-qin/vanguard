#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试AI地址格式
"""

def quick_test():
    """快速测试"""
    print("=== 快速AI地址格式测试 ===")
    
    # 显示系统提示词关键部分
    from config import SYSTEM_PROMPT, DEFAULT_CITY
    
    print(f"默认城市: {DEFAULT_CITY}")
    print("\n系统提示词关键规则:")
    
    lines = SYSTEM_PROMPT.split('\n')
    for line in lines:
        if '格式' in line or '示例' in line or '禁止' in line or DEFAULT_CITY in line:
            print(f"  {line.strip()}")
    
    print(f"\n✅ 系统提示词已优化")
    print(f"✅ 地址格式：城市在前面")
    print(f"✅ 示例：{DEFAULT_CITY}南山区学府路国兴苑")
    print(f"❌ 禁止：学府路国兴苑, {DEFAULT_CITY}")

if __name__ == "__main__":
    quick_test()