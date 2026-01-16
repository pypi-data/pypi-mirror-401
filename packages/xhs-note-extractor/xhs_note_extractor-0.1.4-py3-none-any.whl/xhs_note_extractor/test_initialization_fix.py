#!/usr/bin/env python3
"""
测试设备重试机制的初始化修复
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from extractor import XHSNoteExtractor

def test_initialization():
    """测试初始化是否正常"""
    print("开始测试初始化...")
    
    try:
        # 测试初始化
        extractor = XHSNoteExtractor()
        print("✓ 初始化成功")
        
        # 测试属性是否存在adb connect 11.138.141.113:7121
        print(f"可用设备: {extractor.available_devices}")
        print(f"当前设备索引: {extractor.current_device_index}")
        print(f"设备对象: {extractor.device}")
        
        # 测试连接设备
        if extractor.connect_device():
            print("✓ 设备连接成功")
        else:
            print("⚠ 设备连接失败（可能无设备连接）")
            
        return True
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_initialization()
    if success:
        print("\n✓ 所有测试通过")
    else:
        print("\n✗ 测试失败")
        sys.exit(1)