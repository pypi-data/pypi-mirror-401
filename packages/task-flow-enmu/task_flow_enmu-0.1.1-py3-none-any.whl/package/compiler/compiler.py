from package.provider.todo.todo_regex import TodoPlusRegexes
from package.provider.todo.todo_ast import AST
from package.ir import Task, Priority, Type
from functools import cached_property
import logging
import dateparser
from datetime import datetime


class Compiler:

    def compile(self, file_path: str, pid: str, is_agenda: Type):
        lines = self.get_lines(file_path)
        return self.parse(lines, file_tag=pid, is_agenda=is_agenda)

    def get_lines(self, file_name: str):
        try:
            with open(file_name, "r", encoding="utf-8") as file:
                lines = file.readlines()
                return lines
        except FileNotFoundError:
            logging.error("找到文件")
        except Exception:
            logging.error("读取文件时发生未知错误")

    def parse(self, lines: list[str], file_tag: str, is_agenda: Type) -> list[Task]:
        ast = AST()
        tasks: list[Task] = []
        for i, line in enumerate(lines):
            projects: list[str] = []
            task = Task()
            is_todo = self.regexs.todo.search(line)
            is_closing = not self.regexs.todo_done.search(
                line
            ) and not self.regexs.todo_cancelled.search(line)

            if is_todo and is_closing:
                task.file_tag = file_tag
                task.is_agenda = is_agenda
                task.description = self.parse_desc(line)
                task.tags = self.parse_tag(line)
                task.priority = self.parse_priority(line)
                task.due = self.parse_due_time(line, is_agenda)
                # task.entry = self.parse_general_due_time(str(datetime.today()))

                def find_all_project(line_map):
                    level = line_map["level"]
                    line = line_map["line"]

                    if self.regexs.project.search(line):
                        projects.insert(0, f'"{line.strip().replace(":", "")}"')

                    if level == 0:
                        return False
                    return True

                ast.walk(
                    lines=lines,
                    call_back=find_all_project,
                    line_nr=i,
                    direction=-1,
                    strictly_monotonic=True,
                )

                clean_projects = [p.strip("\"'") for p in projects]
                task.project = ".".join(clean_projects)

                tasks.append(task)
        return tasks

    def parse_tag(self, line: str) -> list[str]:
        if self.regexs.tag_normal.search(line):
            tags_all = self.regexs.tag_normal.findall(line)
            tags_strip = map(lambda tag: tag.strip().replace("@", ""), tags_all)
            tags = [
                tag
                for tag in tags_strip
                if not self.regexs.due_general.search(tag)
                and self.regexs.due_natural.search(tag)
            ]
            return tags
        return []

    def parse_desc(self, line: str) -> str:
        todo = self.regexs.tag.sub("", line)
        if "☐" in todo or "`" in todo or "~" in todo:
            todo = todo.strip().replace("☐ ", "").replace("`", "").replace("~", "")
        return todo

    def parse_priority(self, line) -> str:
        if self.regexs.tag_special.search(line):
            special_tag = self.regexs.tag_special.findall(line)
            return next((p for t in special_tag if (p := Priority.from_str(t))), "")
        return ""

    def parse_due_time(self, line, is_agenda: Type) -> str:
        due_general_tag = self.regexs.due_general.findall(line)
        due_natural_tag = self.regexs.due_natural.findall(line)
        if is_agenda.value == "agenda":
            return self.parse_general_due_time(str(datetime.today()))

        if due_natural_tag:
            return self.parse_natural_due_time(due_natural_tag[0])

        if due_general_tag:
            return self.parse_general_due_time(due_general_tag[0])

        return ""

    def parse_natural_due_time(self, natural_str: str):
        if not natural_str:
            return None
        text = natural_str.strip().lower()
        if text == "someday":
            return None
        if text == "eod":
            now = datetime.now()
            eod_time = now.replace(hour=23, minute=59, second=59, microsecond=0)
            return eod_time.strftime("%Y%m%dT%H%M%SZ")
        dt = dateparser.parse(
            text,
            languages=["en", "zh"],
            settings={
                "PREFER_DATES_FROM": "future",
                "RETURN_AS_TIMEZONE_AWARE": True,
                "RELATIVE_BASE": datetime.now(),
            },
        )

        if dt:
            return dt.strftime("%Y%m%dT%H%M%SZ")
        else:
            print(f"无法解析日期: {natural_str}")
            return None

    def parse_general_due_time(self, general_str: str):
        if not general_str:
            return None

        dt = datetime.strptime(general_str, "%Y-%m-%d %H:%M:%S.%f")
        dt = dt.replace(hour=23, minute=59, second=59)
        return dt.strftime("%Y%m%dT%H%M%SZ")

    @cached_property
    def regexs(self):
        return TodoPlusRegexes()
