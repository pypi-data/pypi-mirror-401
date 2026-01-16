"""
数字格式转换工具
"""

def parse_count_to_int(count_str: str) -> int:
    """
    将小红书的互动数字符串转换为整数
    
    支持格式:
    - "3.1万" -> 31000
    - "3.1w" / "3.1W" -> 31000
    - "1234" -> 1234
    - "12.5万" -> 125000
    
    Args:
        count_str: 数字字符串
        
    Returns:
        int: 转换后的整数
    """
    if not count_str or count_str == "0":
        return 0
    
    count_str = count_str.strip()
    
    # 处理 "万" 或 "w/W"
    if '万' in count_str:
        num_part = count_str.replace('万', '').strip()
        try:
            return int(float(num_part) * 10000)
        except ValueError:
            return 0
    elif 'w' in count_str.lower():
        num_part = count_str.lower().replace('w', '').strip()
        try:
            return int(float(num_part) * 10000)
        except ValueError:
            return 0
    else:
        # 普通数字
        try:
            return int(float(count_str))
        except ValueError:
            return 0
