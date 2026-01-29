import logging
from package.provider.todo.todo_regex import TodoPlusRegexes
from package.ir.todo import Task


class AST:
    def __init__(self) -> None:
        self.indention = "  "

    def get_level(self, s: str) -> int:
        level = 0
        index = 0

        while index < len(s):
            # 结束索引应该是 index + 长度
            current_slice = s[index : index + len(self.indention)]

            if current_slice != self.indention:
                break
            level += 1
            index += len(self.indention)

        return level

    def walk(
        self,
        lines,
        call_back,
        line_nr=0,
        direction=1,
        skip_empty_lines=True,
        strictly_monotonic=False,
    ) -> None:
        # 1. 指针重置（防止文件被读取过一次后变空）
        if len(lines) == 0:
            logging.error("文件为空")
            return
        regexs = TodoPlusRegexes()
        line_count = len(lines)
        # 获取当前行
        start_line = lines[line_nr] if line_nr >= 0 else None
        # 获取当前行的起始缩进
        start_level = self.get_level(start_line) if start_line else -1

        # 获取上一次的缩进，获取下一行
        pre_level = start_level
        next_line = line_nr + direction

        while next_line >= 0 and next_line < line_count:
            # 获取下一行
            line = lines[next_line]
            # 如果开启了跳过空行则跳过
            if skip_empty_lines and regexs.empty.match(line):
                next_line += direction
                continue
            # 获取缩进
            level = self.get_level(line)
            if direction > 0 and level < start_level:
                break

            if strictly_monotonic and (
                (direction > 0 and level <= pre_level)
                or (direction < 0 and level >= pre_level)
            ):
                next_line += direction
                continue

            if (
                call_back(
                    {
                        "start_line": start_line,
                        "start_level": start_level,
                        "line": line,
                        "level": level,
                    }
                )
                == False
            ):
                break

            pre_level = level
            next_line += direction
