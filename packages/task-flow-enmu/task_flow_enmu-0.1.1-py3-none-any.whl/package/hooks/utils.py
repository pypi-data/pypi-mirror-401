from datetime import datetime, timezone, timedelta
import platform
import os


def get_platform() -> str:
    if is_wsl():
        return "wsl"

    return platform.system()


def is_wsl() -> bool:
    if not os.path.exists("/proc/version"):
        return False
    try:
        with open("/proc/version", "r", encoding="utf-8") as f:
            if "microsoft" in f.read().lower():
                return True
    except Exception as e:
        pass

    return False


def convert_task_time(iso_str):
    # 1. 解析：对应 Taskwarrior 的格式 20251231T112041Z
    # %Y=4位年, %m=月, %d=日, T=字符T, %H=时, %M=分, %S=秒, Z=字符Z
    dt_obj = datetime.strptime(iso_str, "%Y%m%dT%H%M%SZ")

    # 2. 转换时区：Taskwarrior 给的是 UTC，我们要转成北京时间 (UTC+8)
    dt_obj = dt_obj.replace(tzinfo=timezone.utc)
    # 然后转成 UTC+8
    dt_local = dt_obj.astimezone(timezone(timedelta(hours=8)))

    # 3. 格式化：变成 25-12-31 20:16
    # %y=2位年, %m=月, %d=日, %H=24小时, %M=分
    return dt_local.strftime("%y-%m-%d %H:%M")


def convert_time_stamp(date_str):
    # 1. 解析
    dt_obj = datetime.strptime(date_str, "%y-%m-%d %H:%M")

    # 2. 强行指定这是北京时间 (UTC+8)
    # replace 不会改变时间数值，只是给它贴个标签说“我是+8区的时间”
    beijing_tz = timezone(timedelta(hours=8))
    dt_obj = dt_obj.replace(tzinfo=beijing_tz)

    # 3. 转成时间戳
    timestamp = dt_obj.timestamp()

    return timestamp


def get_timestamp_from_iso(iso_str):
    """把 Taskwarrior 的 UTC 时间 (20251231T120000Z) 转成时间戳"""
    if not iso_str:
        return 0.0
    try:
        if iso_str.endswith("Z"):
            fmt = "%Y%m%dT%H%M%SZ"
        else:
            fmt = "%Y%m%dT%H%M%S"
        dt = datetime.strptime(iso_str, fmt).replace(tzinfo=timezone.utc)
        return dt.timestamp()
    except:
        return 0.0


def get_timestamp_from_tag(tag_time_str):
    """把文件里的标签时间 (25-12-31 20:16) 转成时间戳"""
    # 假设你文件里的格式是 %y-%m-%d %H:%M (北京时间 UTC+8)
    try:
        dt = datetime.strptime(tag_time_str, "%y-%m-%d %H:%M")
        # 强行设为 UTC+8
        beijing_tz = timezone(timedelta(hours=8))
        dt = dt.replace(tzinfo=beijing_tz)
        return dt.timestamp()
    except:
        return 0.0


def format_duration(seconds):
    """把秒数 (3665) 变成 '1h 1m'"""
    if seconds < 0:
        return "0m"
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    if h > 0:
        return f"{int(h)}h {int(m)}m"
    else:
        return f"{int(m)}m"


def convert_task_time_to_string(iso_str):
    """(你的原函数) 把 UTC ISO 转成 25-12-31 20:16"""
    ts = get_timestamp_from_iso(iso_str)
    # 转回北京时间对象
    dt = datetime.fromtimestamp(ts, timezone(timedelta(hours=8)))
    return dt.strftime("%y-%m-%d %H:%M")
