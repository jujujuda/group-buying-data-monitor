#!/usr/bin/env python3
"""
飞书通知模块
"""

import json
import requests
from datetime import datetime

class FeishuNotifier:
    """飞书通知"""
    
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url
    
    def send_text(self, text):
        """发送文本消息"""
        payload = {
            'msg_type': 'text',
            'content': {
                'text': text
            }
        }
        
        return self._send(payload)
    
    def send_card(self, title, data):
        """发送卡片消息"""
        # 构建卡片内容
        lines = [f"**{title}**"]
        
        for platform, info in data.get('platforms', {}).items():
            line = f"- **{platform}**: "
            details = []
            if 'comments' in info:
                details.append(f"评论{info['comments']}")
            if 'rating' in info:
                details.append(f"评分{info['rating']}")
            if 'orders' in info:
                details.append(f"订单{info['orders']}")
            line += ", ".join(details)
            lines.append(line)
        
        lines.append(f"\n总评论: {data.get('total_comments', 0)}")
        lines.append(f"平均评分: {data.get('avg_rating', 0)}")
        lines.append(f"总订单: {data.get('total_orders', 0)}")
        
        text = "\n".join(lines)
        
        return self.send_text(text)
    
    def send_alert(self, message):
        """发送告警"""
        alert_text = f"⚠️ 告警: {message}"
        return self.send_text(alert_text)
    
    def _send(self, payload):
        """发送请求"""
        try:
            response = requests.post(
                self.webhook_url,
                headers={'Content-Type': 'application/json'},
                data=json.dumps(payload),
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('code') == 0:
                    return {'success': True}
                else:
                    return {'success': False, 'error': result.get('msg')}
            else:
                return {'success': False, 'error': f"HTTP {response.status_code}"}
        
        except Exception as e:
            return {'success': False, 'error': str(e)}


def main():
    """测试"""
    # 注意：需要替换为真实的Webhook URL
    webhook_url = "YOUR_FEISHU_WEBHOOK_URL"
    
    if webhook_url == "YOUR_FEISHU_WEBHOOK_URL":
        print("请配置飞书Webhook URL")
        return
    
    notifier = FeishuNotifier(webhook_url)
    
    # 测试数据
    test_data = {
        'platforms': {
            '大众点评': {'comments': 128, 'rating': 4.5},
            '抖音': {'comments': 256, 'rating': 4.8},
            '美团': {'orders': 520, 'rating': 4.6}
        },
        'total_comments': 384,
        'avg_rating': 4.63,
        'total_orders': 520
    }
    
    result = notifier.send_card("数据日报", test_data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
