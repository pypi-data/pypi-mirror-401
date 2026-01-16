#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
设备重试机制测试脚本

该脚本用于测试小红书笔记提取器的设备重试功能，
当某个设备需要登录时，会自动尝试其他设备。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from extractor import XHSNoteExtractor, extract_note_from_url
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_device_retry():
    """测试设备重试机制"""
    print("=" * 60)
    print("小红书笔记提取器 - 设备重试机制测试")
    print("=" * 60)
    
    # 测试URL（请替换为实际的小红书笔记URL）
    test_url = "https://www.xiaohongshu.com/explore/65a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0"
    
    try:
        # 方式1：使用便捷函数
        print("\n1. 使用便捷函数测试...")
        result = extract_note_from_url(test_url, enable_time_logging=True)
        
        if result:
            print(f"✓ 成功提取笔记数据")
            print(f"  作者: {result.get('author_name', '未知')}")
            print(f"  点赞数: {result.get('likes', '0')}")
            print(f"  收藏数: {result.get('collects', '0')}")
            print(f"  评论数: {result.get('comments', '0')}")
            print(f"  图片数: {len(result.get('image_urls', []))}")
            print(f"  正文预览: {result.get('content', '')[:100]}...")
        else:
            print("✗ 提取失败，所有设备都需要登录或不可用")
        
        # 方式2：使用类实例
        print("\n2. 使用类实例测试...")
        extractor = XHSNoteExtractor(enable_time_logging=True)
        
        # 显示可用设备
        print(f"可用设备: {extractor.available_devices}")
        
        result = extractor.extract_note_data(url=test_url)
        
        if result:
            print(f"✓ 成功提取笔记数据")
            print(f"  作者: {result.get('author_name', '未知')}")
            print(f"  点赞数: {result.get('likes', '0')}")
            print(f"  收藏数: {result.get('collects', '0')}")
            print(f"  评论数: {result.get('comments', '0')}")
            print(f"  图片数: {len(result.get('image_urls', []))}")
        else:
            print("✗ 提取失败，所有设备都需要登录或不可用")
            
    except Exception as e:
        print(f"✗ 测试过程中发生错误: {e}")
        logger.exception("测试异常")

def test_device_switching():
    """测试设备切换功能"""
    print("\n" + "=" * 60)
    print("设备切换功能测试")
    print("=" * 60)
    
    try:
        extractor = XHSNoteExtractor(enable_time_logging=True)
        
        print(f"初始设备: {extractor.device.serial if extractor.device else '无'}")
        print(f"可用设备列表: {extractor.available_devices}")
        
        if len(extractor.available_devices) > 1:
            print("\n测试设备切换...")
            success = extractor.switch_to_next_device()
            if success:
                print(f"✓ 成功切换到设备: {extractor.device.serial}")
            else:
                print("✗ 设备切换失败")
        else:
            print("只有一个或没有可用设备，无法测试切换功能")
            
    except Exception as e:
        print(f"✗ 测试过程中发生错误: {e}")
        logger.exception("测试异常")

if __name__ == "__main__":
    test_device_retry()
    test_device_switching()