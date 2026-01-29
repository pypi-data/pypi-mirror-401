from pydantic import BaseModel, ConfigDict, Field, field_serializer
from typing import Optional, List
from datetime import datetime
from enum import Enum
import uuid
import logging


class TaskStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    DELETED = "deleted"
    WAITING = "waiting"
    RECURRING = "recurring"

    @classmethod
    def list_active(cls):
        return [cls.PENDING, cls.WAITING]

    @classmethod
    def list_closed(cls):
        return [cls.COMPLETED, cls.DELETED]


class Priority(Enum):
    HIGH = "H"
    MEDIUM = "M"
    LOW = "L"

    @classmethod
    def from_str(cls, label: str) -> str:
        try:
            return cls[label.upper()].value
        except KeyError:
            logging.warning(f"警告: 未知的优先级 '{label}'，已默认为 LOW")
            return ""


class Type(Enum):
    PROJECT = "project"
    AGENDA = "agenda"


class Task(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()))
    id: Optional[str] = None
    description: str = ""
    status: TaskStatus = TaskStatus.PENDING
    project: Optional[str] = None
    priority: Optional[Priority] = None
    tags: List[str] = Field(default_factory=list)
    entry: datetime = Field(default_factory=datetime.now)
    due: Optional[datetime] = None
    wait: Optional[datetime] = None
    end: Optional[datetime] = None
    start: Optional[datetime] = None
    modified: Optional[datetime] = None
    scheduled: Optional[datetime] = None
    depends: Optional[str] = None
    annotations: List[str] = Field(default_factory=list)
    file_tag: Optional[str] = None
    is_agenda: Type = Field(default=Type.PROJECT)

    @field_serializer("due", "entry", "start", "end")
    def serialize_dates(self, v, _info):
        if v == "":
            return None
        return v
