import dashscope
import json
import re
from config import DASHSCOPE_API_KEY, QWEN_MODEL, SYSTEM_PROMPT

class AIProcessor:
    def __init__(self):
        dashscope.api_key = DASHSCOPE_API_KEY
    
    def process_navigation_request(self, user_input):
        """处理用户的导航请求"""
        try:
            from dashscope import Generation
            
            response = Generation.call(
                model=QWEN_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.3,
                max_tokens=200,
                result_format='message'
            )
            
            if response.status_code == 200:
                result_text = response.output.choices[0].message.content.strip()
                print(f"AI处理结果: {result_text}")
                
                # 尝试解析JSON
                try:
                    # 提取JSON部分（去除可能的markdown格式）
                    if '```json' in result_text:
                        json_start = result_text.find('{')
                        json_end = result_text.rfind('}') + 1
                        result_text = result_text[json_start:json_end]
                    elif result_text.startswith('```') and result_text.endswith('```'):
                        result_text = result_text.strip('`').strip()
                    
                    result = json.loads(result_text)
                    return result
                except json.JSONDecodeError:
                    # 如果不是标准JSON，尝试提取地址信息
                    return self._extract_addresses_fallback(user_input, result_text)
            else:
                print(f"千问API调用失败: {response.message}")
                return self._extract_addresses_fallback(user_input, "")
                
        except Exception as e:
            print(f"AI处理错误: {e}")
            return self._extract_addresses_fallback(user_input, "")
    
    def _extract_addresses_fallback(self, user_input, ai_response):
        """备用地址提取方法"""
        # 简单的正则表达式匹配
        patterns = [
            r'从(.+?)到(.+?)(?:导航|去|走)',
            r'去(.+?)(?:怎么走|导航)',
            r'(.+?)到(.+?)的路线',
            r'导航到(.+?)(?:去|走)?'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_input)
            if match:
                if len(match.groups()) == 2:
                    return {
                        "origin": match.group(1).strip(),
                        "destination": match.group(2).strip(),
                        "action": "navigation"
                    }
                elif len(match.groups()) == 1:
                    return {
                        "origin": "当前位置",
                        "destination": match.group(1).strip(),
                        "action": "navigation"
                    }
        
        # 如果都匹配不到，返回错误
        return {
            "error": "无法解析导航请求，请重新输入",
            "original_input": user_input
        }
    
    def validate_addresses(self, origin, destination):
        """验证地址有效性"""
        if not origin or not destination:
            return False, "起点或终点不能为空"
        
        if origin == destination:
            return False, "起点和终点不能相同"
        
        return True, "地址验证通过"