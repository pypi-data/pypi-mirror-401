import subprocess
import yaml
import json
import datetime
from package.compiler.compiler import Compiler
from package.utils.utils import get_platform
from package.ir.todo import Task, Type
from pathlib import Path


def run(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout


def get_file_path(target_path):
    with open(target_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        sources = config["sources"]
    return sources


def check_exist(desc: str, project) -> int:
    parts = ["task", "status:pending"]

    if desc:
        parts.append(f'description:"{desc}"')
    if project:
        parts.append(f"project:{project}")
    parts.append("count")
    cmd = " ".join(parts)

    result = subprocess.getoutput(cmd)
    return int(result) > 0


def assembly_cmd(tasks: list[Task]):
    formart_tasks = []
    for task in tasks:
        task_json = task.model_dump_json(exclude_none=True)
        task_dict = json.loads(task_json)

        cleaned_dict = {
            k: v for k, v in task_dict.items() if v not in ("", [], None) and k != "id"
        }
        formart_tasks.append(cleaned_dict)
    return formart_tasks


def add_task(target_file):
    sources = get_file_path(target_file)
    os_name = get_platform().lower()

    for source in sources:
        try:
            _process_single_source(source, os_name)
        except Exception as e:
            print(e)


def _process_single_source(source: dict, os_name: str):
    pid = source["id"]
    base_path = Path(source["path"][os_name])
    if source["type"] == "daily":
        today = datetime.date.today()
        file_path = base_path / str(today.year) / f"{today.month:02d}" / f"{today}.todo"
        agenda_type = Type.AGENDA
    else:
        file_path = base_path
        agenda_type = Type.PROJECT
    items = Compiler().compile(str(file_path), pid=pid, is_agenda=agenda_type)
    cmds = assembly_cmd(items)
    json_str = json.dumps(cmds, indent=2, ensure_ascii=False)
    importer(json_str)


def importer(json_str: str):
    try:
        result = subprocess.run(
            ["task", "import"],
            input=json_str,
            text=True,
            capture_output=True,
            check=True,
        )

        print("导入成功！")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("导入失败！")
        print("错误信息:", e.stderr)
