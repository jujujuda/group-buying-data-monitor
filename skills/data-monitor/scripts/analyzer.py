#!/usr/bin/env python3
"""
数据分析模块
数据清洗、趋势分析、异常检测
"""

import json
from datetime import datetime
from collections import defaultdict

class DataAnalyzer:
    """数据分析器"""
    
    def __init__(self):
        self.history = defaultdict(list)
    
    def clean_data(self, raw_data):
        """数据清洗"""
        cleaned = {}
        
        for platform, data in raw_data.items():
            if isinstance(data, dict) and 'error' not in data:
                cleaned[platform] = data
        
        return cleaned
    
    def analyze_trends(self, data):
        """趋势分析"""
        trends = {}
        
        for platform, current in data.items():
            history = self.history[platform]
            
            if history:
                last = history[-1]
                
                # 计算变化
                changes = {}
                for key in ['comments', 'rating', 'orders']:
                    if key in current and key in last:
                        curr_val = current.get(key, 0)
                        last_val = last.get(key, 0)
                        if isinstance(curr_val, (int, float)) and isinstance(last_val, (int, float)):
                            change = ((curr_val - last_val) / last_val * 100) if last_val else 0
                            changes[key] = f"{change:+.1f}%"
                
                trends[platform] = changes
            
            # 保存到历史
            history.append(current)
        
        return trends
    
    def detect_anomalies(self, data):
        """异常检测"""
        anomalies = []
        
        for platform, current in data.items():
            # 简单规则：评论数突然变化超过50%
            history = self.history.get(platform, [])
            if len(history) >= 2:
                last = history[-1]
                curr_comments = current.get('comments', 0)
                last_comments = last.get('comments', 0)
                
                if last_comments > 0:
                    change = abs(curr_comments - last_comments) / last_comments
                    if change > 0.5:
                        anomalies.append({
                            'platform': platform,
                            'type': 'comments_spike',
                            'current': curr_comments,
                            'last': last_comments,
                            'change': f"{change*100:.1f}%"
                        })
        
        return anomalies
    
    def generate_summary(self, data, trends=None, anomalies=None):
        """生成摘要"""
        summary = {
            'timestamp': datetime.now().isoformat(),
            'platforms': {},
            'total_comments': 0,
            'avg_rating': 0,
            'total_orders': 0
        }
        
        ratings = []
        
        for platform, d in data.items():
            platform_summary = {}
            
            if 'comments' in d:
                summary['total_comments'] += d['comments']
                platform_summary['comments'] = d['comments']
            
            if 'rating' in d:
                ratings.append(float(d['rating']))
                platform_summary['rating'] = d['rating']
            
            if 'orders' in d:
                summary['total_orders'] += d['orders']
                platform_summary['orders'] = d['orders']
            
            if platform_summary:
                summary['platforms'][platform] = platform_summary
        
        if ratings:
            summary['avg_rating'] = round(sum(ratings) / len(ratings), 2)
        
        if trends:
            summary['trends'] = trends
        
        if anomalies:
            summary['anomalies'] = anomalies
        
        return summary
    
    def analyze(self, raw_data):
        """完整分析流程"""
        # 1. 清洗数据
        data = self.clean_data(raw_data)
        
        # 2. 趋势分析
        trends = self.analyze_trends(data)
        
        # 3. 异常检测
        anomalies = self.detect_anomalies(data)
        
        # 4. 生成摘要
        summary = self.generate_summary(data, trends, anomalies)
        
        return summary


if __name__ == '__main__':
    # 测试
    test_data = {
        'dianping': {'comments': 128, 'rating': 4.5, 'rank': 3},
        'douyin': {'comments': 256, 'rating': 4.8},
        'meituan': {'orders': 520, 'conversion': '12%', 'rating': 4.6},
    }
    
    analyzer = DataAnalyzer()
    result = analyzer.analyze(test_data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
