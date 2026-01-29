import re
import json5
import yaml
from datetime import datetime, timezone, date
from zoneinfo import ZoneInfo
from package.hooks.task_logger import get_hook_logger
from package.hooks.utils import (
    get_platform,
    get_timestamp_from_iso,
    get_timestamp_from_tag,
    format_duration,
    convert_task_time_to_string,
)

from pathlib import Path

RE_STARTED = re.compile(r"@started\((\d{2}-\d{2}-\d{2}\s+\d{2}:\d{2})\)")
RE_DATE_TAG = re.compile(r"@\d{4}-\d{2}-\d{2}")
logger = get_hook_logger("OnModify")


def calc_duration_string(line, end_iso, tagname):
    match = RE_STARTED.search(line)
    if not match:
        return ""

    start_ts = get_timestamp_from_tag(match.group(1))
    end_ts = get_timestamp_from_iso(end_iso)

    if end_ts > start_ts:
        duration_text = format_duration(end_ts - start_ts)
        return f" {tagname}({duration_text})"
    return ""


def format_due_date(due_iso):
    if not due_iso:
        return None

    try:
        dt = datetime.strptime(due_iso, "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc)
        return dt.astimezone(ZoneInfo("Asia/Shanghai")).strftime("%Y-%m-%d")
    except Exception as e:
        logger.error(f"日期转换失败: {e}")
        return None


def handle_task_closing(line, new, config):
    if any(t in line for t in config["exclude"]):
        return False, line

    end_iso = new.get("end", "")
    end_str = convert_task_time_to_string(end_iso)
    duration_str = calc_duration_string(line, end_iso, config["dur_tag"])
    new_desc = line.replace("☐", config["icon"]).rstrip()
    new_line = f"{new_desc} {config['tag']}({end_str}){duration_str}\n"
    return True, new_line


def handle_task_start(line, new, _=None):
    if any(t in line for t in ["@started", "@done", "@cancelled"]):
        return False, line

    start_iso = new.get("start")
    if not start_iso:
        return False, line

    start_str = convert_task_time_to_string(start_iso)
    return True, f"{line.rstrip()} @started({start_str})\n"


def handle_task_due(line, new, _=None):
    if "@done" in line or "@cancelled" in line:
        return False, line

    due_date = format_due_date(new.get("due"))

    if not due_date:
        return False, line

    date_tag = f"@{due_date}"

    if RE_DATE_TAG.search(line):
        new_line = RE_DATE_TAG.sub(date_tag, line)
        return (new_line != line), new_line
    else:
        return True, f"{line.rstrip()} {date_tag}\n"


def process_line(line, new, mode):
    target_desc = new.get("description")

    if target_desc not in line:
        return False, line

    strategies = {
        "done": (
            handle_task_closing,
            {
                "icon": "✔",
                "tag": "@done",
                "dur_tag": "@last",
                "exclude": ["@done", "@cancelled"],
            },
        ),
        "cancel": (
            handle_task_closing,
            {
                "icon": "✘",
                "tag": "@cancelled",
                "dur_tag": "@waste",
                "exclude": ["@done", "@cancelled"],
            },
        ),
        "start": (handle_task_start, None),
        "due": (handle_task_due, None),
    }

    handler, config = strategies.get(mode, (None, None))

    if handler:
        return handler(line, new, config)
    return False, line


def update_file(new_str, mode, target_file):
    new = json5.loads(new_str)
    filetag = new.get("file_tag", "")
    if not filetag:
        return

    with open(target_file, "r", encoding="utf-8") as yf:
        path_obj = yaml.safe_load(yf)

    for s in path_obj["sources"]:
        if s["id"] == filetag:
            obj = s
            break

    if not obj:
        print("找不到指定项目")
        return
    os_name = str.lower(get_platform())
    p = obj["path"][os_name]
    if obj["type"] == "daily":
        today = date.today()
        month = f"{today.month:02d}"
        year = str(today.year)
        p = str(Path(p) / year / month / f"{today}.todo")

    if not p:
        return
    try:
        with open(p, "r", encoding="utf-8") as f:
            lines = f.readlines()
            modify_lines = []
            is_changed = False

            for line in lines:
                changed, new_line = process_line(line, new, mode)
                modify_lines.append(new_line)

                if changed:
                    is_changed = True
                    logger.debug("修改成功")

            if is_changed:
                with open(p, "w", encoding="utf-8") as nf:
                    nf.writelines(modify_lines)
                logger.debug("文件更新完成")
    except Exception as e:
        logger.error(f"处理失败: {e}", exc_info=True)
