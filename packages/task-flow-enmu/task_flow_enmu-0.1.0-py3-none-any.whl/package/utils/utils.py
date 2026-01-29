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
