import re
from datetime import datetime, timedelta

def parse_time_to_timestamp_ms(time_str: str, now: datetime | None = None) -> int:
    if now is None:
        now = datetime.now()

    time_str = time_str.strip()
    # Remove common prefixes
    for prefix in ["编辑于", "发布于"]:
        if time_str.startswith(prefix):
            time_str = time_str[len(prefix):].strip()
    
    # Remove location suffix (e.g., "昨天 15:09重庆" -> "昨天 15:09")
    # Match common Chinese city/province names at the end
    import re as re_module
    time_str = re_module.sub(r'[\u4e00-\u9fa5]{2,4}$', '', time_str).strip()

    # 刚刚
    if time_str == "刚刚":
        dt = now

    # X分钟前
    elif match := re.match(r"(\d+)分钟前", time_str):
        dt = now - timedelta(minutes=int(match.group(1)))

    # X小时前
    elif match := re.match(r"(\d+)小时前", time_str):
        dt = now - timedelta(hours=int(match.group(1)))

    # X天前
    elif match := re.match(r"(\d+)天前", time_str):
        dt = now - timedelta(days=int(match.group(1)))

    # 昨天 HH:mm
    elif match := re.match(r"昨天\s*(\d{1,2}:\d{2})", time_str):
        dt = datetime.strptime(
            f"{(now - timedelta(days=1)).date()} {match.group(1)}",
            "%Y-%m-%d %H:%M"
        )

    # 前天 HH:mm
    elif match := re.match(r"前天\s*(\d{1,2}:\d{2})", time_str):
        dt = datetime.strptime(
            f"{(now - timedelta(days=2)).date()} {match.group(1)}",
            "%Y-%m-%d %H:%M"
        )

    # YYYY-MM-DD HH:mm
    elif re.match(r"\d{4}-\d{2}-\d{2}\s+\d{1,2}:\d{2}", time_str):
        dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M")

    # YYYY-MM-DD
    elif re.match(r"\d{4}-\d{2}-\d{2}", time_str):
        dt = datetime.strptime(time_str, "%Y-%m-%d")

    # ✅ 新增：MM-DD（默认当前年份）
    elif match := re.match(r"(\d{2})-(\d{2})", time_str):
        year = now.year
        month, day = map(int, match.groups())
        dt = datetime(year, month, day)

    # HH:mm（默认当天）
    elif re.match(r"\d{1,2}:\d{2}", time_str):
        dt = datetime.strptime(
            f"{now.date()} {time_str}",
            "%Y-%m-%d %H:%M"
        )

    else:
        raise ValueError(f"无法解析的时间格式: {time_str}")

    return int(dt.timestamp() * 1000)
