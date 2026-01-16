# 小红书笔记提取器 - 设备重试机制使用指南

## 功能概述

小红书笔记提取器现在支持设备重试机制。当某个设备需要登录时，系统会自动尝试连接其他可用设备，直到找到无需登录的设备或所有设备都尝试过为止。

## 使用方式

### 1. 使用便捷函数（推荐）

```python
from xhs_note_extractor import extract_note_from_url

# 直接提取笔记数据
result = extract_note_from_url("https://www.xiaohongshu.com/explore/你的笔记ID")

if result:
    print("成功提取笔记数据")
    print(f"作者: {result['author_name']}")
    print(f"点赞数: {result['likes']}")
    print(f"图片数: {len(result['image_urls'])}")
else:
    print("所有设备都需要登录，提取失败")
```

### 2. 使用类实例

```python
from xhs_note_extractor import XHSNoteExtractor

# 创建提取器实例
extractor = XHSNoteExtractor()

# 显示可用设备
print(f"可用设备: {extractor.available_devices}")

# 提取笔记数据
result = extractor.extract_note_data(url="https://www.xiaohongshu.com/explore/你的笔记ID")

if result:
    print("成功提取笔记数据")
else:
    print("所有设备都需要登录，提取失败")
```

### 3. 手动切换设备

```python
from xhs_note_extractor import XHSNoteExtractor

extractor = XHSNoteExtractor()

# 查看当前设备
print(f"当前设备: {extractor.device.serial}")

# 手动切换到下一个设备
success = extractor.switch_to_next_device()
if success:
    print(f"已切换到设备: {extractor.device.serial}")
```

## 工作原理

1. **设备发现**: 初始化时自动检测所有通过ADB连接的Android设备
2. **登录检测**: 在提取笔记时检测是否需要登录
3. **自动重试**: 如果需要登录，自动尝试下一个可用设备
4. **循环尝试**: 依次尝试所有可用设备
5. **结果返回**: 成功则返回数据，失败则返回None

## 注意事项

- 确保所有设备都已通过USB调试连接并授权
- 设备需要安装小红书APP
- 如果所有设备都需要登录，则返回None而不是抛出异常
- 设备切换时会自动重启小红书APP

## 测试脚本

运行测试脚本验证设备重试功能：

```bash
python xhs_note_extractor/test_device_retry.py
```

## 故障排除

1. **无法发现设备**：
   - 检查USB连接
   - 确保ADB调试已开启
   - 运行 `adb devices` 验证设备连接

2. **设备切换失败**：
   - 检查设备是否仍然连接
   - 确保小红书APP在设备上已安装

3. **返回None**：
   - 所有设备都需要登录
   - 尝试手动登录某个设备后再试