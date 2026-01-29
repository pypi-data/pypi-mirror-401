import re
from typing import Dict, Pattern, Optional


class DateRegexPatterns:
    """
    集中管理正则组件，防止重复定义
    【修改说明】：移除了 [a-z]* 这种贪婪匹配，改为显式全称或缩写。
    彻底解决 'mark', 'money', 'june's' 等普通单词被误判为日期的问题。
    """

    # 1. 星期 (Strict matching)
    # 逻辑：匹配全称(monday) 或 缩写(mon) 或 带点缩写(mon.)
    WEEKDAYS = (
        r"(?:"
        r"mondays?|mon\.?|"
        r"tuesdays?|tue\.?|"
        r"wednesdays?|wed\.?|"
        r"thursdays?|thu\.?|thur\.?|"
        r"fridays?|fri\.?|"
        r"saturdays?|sat\.?|"
        r"sundays?|sun\.?"
        r")"
    )

    # 2. 月份 (Strict matching)
    # 逻辑：匹配全称(march) 或 缩写(mar) 或 带点缩写(mar.)
    MONTHS = (
        r"(?:"
        r"january|jan\.?|"
        r"february|feb\.?|"
        r"march|mar\.?|"  # <--- 关键修复：只认 mar 或 march
        r"april|apr\.?|"
        r"may\.?|"  # May 比较短，通常不缩写，但匹配 may. 也可以
        r"june|jun\.?|"
        r"july|jul\.?|"
        r"august|aug\.?|"
        r"september|sept?\.?|"  # 同时兼容 sep 和 sept
        r"october|oct\.?|"
        r"november|nov\.?|"
        r"december|dec\.?"
        r")"
    )

    # 3. 修饰词 (保持原样，没问题)
    MODIFIERS = r"(?:next|last|this|prev|previous)"

    # 4. 单位 (保持原样，没问题)
    # 注意：d, m, y 这种单字母单位最好配合数字使用，但在 get_general_date_regex 里的组合逻辑应该处理好了
    UNITS = r"(?:d|w|m|y|h|min|day|week|month|year|hour|minute)s?"


class TodoPlusRegexes:
    """
    Todo+ 正则表达式集合

    所有正则表达式都使用 re.MULTILINE 和 re.IGNORECASE 标志（如适用）
    """

    def __init__(self, archive_name: str = "Archive", special_tags: list = None):  # type: ignore
        """
        初始化正则表达式

        Args:
            archive_name: 归档项目名称（默认："Archive"）
            special_tags: 特殊标签列表（默认：['critical', 'high', 'low', 'today']）
        """
        if special_tags is None:
            special_tags = ["critical", "high", "low", "medium", "today"]

        self.archive_name = archive_name
        self.special_tags = special_tags

        # 初始化所有正则表达式
        self._init_regexes()

    def _init_regexes(self):
        """初始化所有正则表达式"""

        # ========================================
        # 基础正则（2个）
        # ========================================

        # 永远不匹配的正则表达式（占位符）
        self.impossible = re.compile(r"(?=a)b", re.MULTILINE)

        # 匹配空行或只包含空白的行
        self.empty = re.compile(r"^\s*$")

        # ========================================
        # TODO 相关正则（8个）
        # ========================================

        # 匹配所有 TODO 项（未完成 + 已完成 + 已取消）
        # 匹配：☐ Task、✔ Task、✘ Task、[x] Task
        self.todo = re.compile(
            r"^[^\S\n]*((?!--|––|——)(?:[-❍❑■⬜□☐▪▫–—≡→›✘xX✔✓☑+]|\[[ xX+-]?\])\s[^\n]*)",
            re.MULTILINE,
        )

        # 匹配 TODO 符号部分（用于符号替换）
        self.todo_symbol = re.compile(
            r"^[^\S\n]*(?!--|––|——)([-❍❑■⬜□☐▪▫–—≡→›✘xX✔✓☑+]|\[[ xX+-]?\])\s"
        )

        # 匹配未完成的 TODO
        # 匹配：☐ Task、[ ] Task
        # 不匹配：☐ Task @done、✔ Task
        self.todo_box = re.compile(
            r"^[^\S\n]*((?!--|––|——)(?:[-❍❑■⬜□☐▪▫–—≡→›]|\[ ?\])\s"
            r"(?![^\n]*[^a-zA-Z0-9]@(?:done|cancelled)(?:(?:\([^)]*\))|(?![a-zA-Z])))[^\n]*)",
            re.MULTILINE,
        )

        # 匹配已开始的 TODO（包含 @started 标签）
        # 用途：显示计时器
        self.todo_box_started = re.compile(
            r"^[^\S\n]*((?!--|––|——)(?:[-❍❑■⬜□☐▪▫–—≡→›]|\[ ?\])\s"
            r"(?=[^\n]*[^a-zA-Z0-9]@started(?:(?:\([^)]*\))|(?![a-zA-Z])))[^\n]*)",
            re.MULTILINE,
        )

        # 匹配已完成的 TODO
        # 两种方式：1. 符号：✔ Task  2. 标签：☐ Task @done
        self.todo_done = re.compile(
            r"^[^\S\n]*((?!--|––|——)(?:"
            r"(?:(?:[✔✓☑+]|\[[xX+]\])\s[^\n]*)|"
            r"(?:(?:[-❍❑■⬜□☐▪▫–—≡→›]|\[ ?\])\s[^\n]*[^a-zA-Z0-9]@done"
            r"(?:(?:\([^)]*\))|(?![a-zA-Z]))[^\n]*)))",
            re.MULTILINE,
        )

        # 匹配已取消的 TODO
        # 两种方式：1. 符号：✘ Task  2. 标签：☐ Task @cancelled
        self.todo_cancelled = re.compile(
            r"^[^\S\n]*((?!--|––|——)(?:"
            r"(?:(?:[✘xX]|\[-\])\s[^\n]*)|"
            r"(?:(?:[-❍❑■⬜□☐▪▫–—≡→›]|\[ ?\])\s[^\n]*[^a-zA-Z0-9]@cancelled"
            r"(?:(?:\([^)]*\))|(?![a-zA-Z]))[^\n]*)))",
            re.MULTILINE,
        )

        # 匹配所有已结束的 TODO（已完成 + 已取消）
        # 用途：归档操作
        self.todo_finished = re.compile(
            r"^[^\S\n]*((?!--|––|——)(?:"
            r"(?:(?:[✔✓☑+✘xX]|\[[xX+-]\])\s[^\n]*)|"
            r"(?:(?:[-❍❑■⬜□☐▪▫–—≡→›]|\[ ?\])\s[^\n]*[^a-zA-Z0-9]@(?:done|cancelled)"
            r"(?:(?:\([^)]*\))|(?![a-zA-Z]))[^\n]*)))",
            re.MULTILINE,
        )

        # 注意：todoEmbedded 需要从配置动态生成，这里设为 None
        self.todo_embedded = None

        # ========================================
        # 项目相关正则（4个）
        # ========================================

        # 匹配项目行（以冒号结尾）
        # 匹配：Todo:、Work:、Shopping:
        self.project = re.compile(
            r"^(?![^\S\n]*(?!--|––|——)(?:[-❍❑■⬜□☐▪▫–—≡→›✘xX✔✓☑+]|\[[ xX+-]?\])\s[^\n]*)"
            r"[^\S\n]*(.+:)[^\S\n]*(?:(?=@[^\s*~(]+(?:://[^\s*~(:]+)?(?:\([^)]*\))?)|$)",
            re.MULTILINE,
        )

        # 拆分项目行的各部分
        # 捕获组：[1]=缩进, [2]=项目名, [3]=冒号后的内容
        self.project_parts = re.compile(r"(\s*)(.+):(.*)")

        # 匹配归档项目（动态生成，基于配置的归档名称）
        self.archive = re.compile(
            r"^(?![^\S\n]*(?!--|––|——)(?:[-❍❑■⬜□☐▪▫–—≡→›✘xX✔✓☑+]|\[[ xX+-]?\])\s[^\n]*)"
            rf"([^\S\n]*{re.escape(self.archive_name)}:.*$)",
            re.MULTILINE,
        )

        # 匹配注释行（既不是 TODO，也不是项目，也不是空行）
        self.comment = re.compile(
            r"^(?!\s*$)"
            r"(?![^\S\n]*(?!--|––|——)(?:[-❍❑■⬜□☐▪▫–—≡→›✘xX✔✓☑+]|\[[ xX+-]?\])\s[^\n]*)"
            r"(?![^\S\n]*.+:[^\S\n]*(?:(?=@[^\s*~(]+(?:://[^\s*~(:]+)?(?:\([^)]*\))?)|$))"
            r"[^\S\n]*([^\n]+)",
            re.MULTILINE,
        )

        # ========================================
        # 标签相关正则（9个）
        # ========================================

        # 匹配所有标签（@开头）
        # 匹配：@high、@done(2024-01-01)、@url://example.com
        self.tag = re.compile(
            r"(?:^|[^a-zA-Z0-9`])(@[^\s*~(]+(?:://[^\s*~(:]+)?(?:\([^)]*\))?)",
            re.MULTILINE,
        )

        # 匹配特殊标签（动态生成，基于配置的特殊标签列表）
        tags_pattern = "|".join(re.escape(tag) for tag in self.special_tags)
        self.tag_special = re.compile(
            rf"(?:^|[^a-zA-Z0-9])@({tags_pattern})(?:(?:\([^)]*\))|(?![a-zA-Z]))",
            re.MULTILINE,
        )

        # 匹配特殊标签或普通标签
        special_patterns = "|".join(
            rf"(@{re.escape(tag)}(?:(?:\([^)]*\))|(?![a-zA-Z])))"
            for tag in self.special_tags
        )
        self.tag_special_normal = re.compile(
            rf"(?:^|[^a-zA-Z0-9])(?:{special_patterns}|"
            r"(@[^\s*~(]+(?:://[^\s*~(:]+)?(?:(?:\([^)]*\))|(?![a-zA-Z]))))",
            re.MULTILINE,
        )

        # 匹配普通标签（排除特殊标签和系统标签）
        excluded_tags = "|".join(re.escape(tag) for tag in self.special_tags)
        self.tag_normal = re.compile(
            rf"(?:^|[^a-zA-Z0-9])@(?!{excluded_tags}|created|done|cancelled|started|lasted|wasted|est|medium|\d)"
            r"[^\s*~(:]+(?:://[^\s*~(:]+)?(?:\([^)]*\))?"
        )

        # 匹配创建时间标签
        # 匹配：@created、@created(2024-01-01)
        # 捕获组[1]：括号内的时间值
        self.tag_created = re.compile(
            r"(?:^|[^a-zA-Z0-9])@created(?:(?:\(([^)]*)\))|(?![a-zA-Z]))"
        )

        # 匹配开始时间标签
        # 匹配：@started、@started(2024-01-01 10:00)
        # 捕获组[1]：括号内的时间值
        self.tag_started = re.compile(
            r"(?:^|[^a-zA-Z0-9])@started(?:(?:\(([^)]*)\))|(?![a-zA-Z]))"
        )

        # 匹配完成/取消时间标签
        # 匹配：@done、@cancelled、@done(2024-01-01)
        # 捕获组[1]：括号内的时间值
        self.tag_finished = re.compile(
            r"(?:^|[^a-zA-Z0-9])@(?:done|cancelled)(?:(?:\(([^)]*)\))|(?![a-zA-Z]))"
        )

        # 匹配持续时间标签
        # 匹配：@lasted(2h30m)、@wasted(1h)
        # 捕获组[1]：括号内的时间值
        self.tag_elapsed = re.compile(
            r"(?:^|[^a-zA-Z0-9])@(?:lasted|wasted)(?:(?:\(([^)]*)\))|(?![a-zA-Z]))"
        )

        # 匹配时间估算标签
        # 两种格式：@est(2h) 或 @2h
        # 捕获组[1]：@est()的时间, 捕获组[2]：@时间的时间
        self.tag_estimate = re.compile(r"(?:^|[^a-zA-Z0-9])@est\(([^)]*)\)|@(\d\S+)")

        # ========================================
        # 格式化正则（5个）
        # ========================================

        # 匹配所有格式化文本
        # 匹配：`code`、*bold*、_italic_、~strikethrough~
        self.formatted = re.compile(
            r"(?:^|[^a-zA-Z0-9])(?:(`[^\n`]*`)|(\*[^\n*]+\*)|(_[^\n_]+_)|(~[^\n~]+~))(?![a-zA-Z])",
            re.MULTILINE,
        )

        # 匹配代码格式
        # 匹配：`code`、`variable`
        self.formatted_code = re.compile(
            r"(?:^|[^a-zA-Z0-9])(`[^\n`]*`)(?![a-zA-Z])", re.MULTILINE
        )

        # 匹配粗体格式
        # 匹配：*bold*、*important*
        self.formatted_bold = re.compile(
            r"(?:^|[^a-zA-Z0-9])(\*[^\n*]+\*)(?![a-zA-Z])", re.MULTILINE
        )

        # 匹配斜体格式
        # 匹配：_italic_、_emphasis_
        self.formatted_italic = re.compile(
            r"(?:^|[^a-zA-Z0-9])(_[^\n_]+_)(?![a-zA-Z])", re.MULTILINE
        )

        # 匹配删除线格式
        # 匹配：~deleted~、~obsolete~
        self.formatted_strikethrough = re.compile(
            r"(?:^|[^a-zA-Z0-9])(~[^\n~]+~)(?![a-zA-Z])", re.MULTILINE
        )

        self.due_natural = self.get_natural_tag_regex()
        self.due_general = self.get_general_date_regex()

    def get_natural_tag_regex(self):
        # 引用公共组件
        P = DateRegexPatterns()

        # 组合目标：星期 | 月份 | 单位
        targets = f"(?:{P.WEEKDAYS}|{P.MONTHS}|{P.UNITS})"

        # 逻辑：@ + 修饰词 + "+" + 目标
        # 注意：这里强制中间必须是 "+" 号
        pattern = re.compile(rf"@({P.MODIFIERS}\+{targets})\b", re.IGNORECASE)

        return pattern

    def get_general_date_regex(self):
        # 特殊关键词
        keywords = (
            r"(?:today|tomorrow|yesterday|now|someday|later|eod|eow|eom|eoy|soc|eoc)"
        )

        P = DateRegexPatterns()

        pattern = re.compile(
            rf"""
            \b (
                {keywords}
                |
                [+-]?\s*\d+\s*{P.UNITS}
                |
                (?:{P.WEEKDAYS}|{P.MONTHS})
                |
                \d{{4}}-\d{{1,2}}-\d{{1,2}}
                |\d{{1,2}}/\d{{1,2}}(?:/\d{{2,4}})?
                |
                \d+(?:st|nd|rd|th)\s+{P.WEEKDAYS}
            ) \b
        """,
            re.IGNORECASE | re.VERBOSE,
        )

        return pattern

    def get_all_regexes(self) -> Dict[str, Optional[Pattern]]:
        """
        获取所有正则表达式的字典

        Returns:
            包含所有正则表达式的字典
        """
        return {
            # 基础正则
            "impossible": self.impossible,
            "empty": self.empty,
            # TODO 相关
            "todo": self.todo,
            "todo_symbol": self.todo_symbol,
            "todo_box": self.todo_box,
            "todo_box_started": self.todo_box_started,
            "todo_done": self.todo_done,
            "todo_cancelled": self.todo_cancelled,
            "todo_finished": self.todo_finished,
            "todo_embedded": self.todo_embedded,
            # 项目相关
            "project": self.project,
            "project_parts": self.project_parts,
            "archive": self.archive,
            "comment": self.comment,
            # 标签相关
            "tag": self.tag,
            "tag_special": self.tag_special,
            "tag_special_normal": self.tag_special_normal,
            "tag_normal": self.tag_normal,
            "tag_created": self.tag_created,
            "tag_started": self.tag_started,
            "tag_finished": self.tag_finished,
            "tag_elapsed": self.tag_elapsed,
            "tag_estimate": self.tag_estimate,
            # 格式化相关
            "formatted": self.formatted,
            "formatted_code": self.formatted_code,
            "formatted_bold": self.formatted_bold,
            "formatted_italic": self.formatted_italic,
            "formatted_strikethrough": self.formatted_strikethrough,
            "due_natural": self.due_natural,
            "due_general": self.due_general,
        }
