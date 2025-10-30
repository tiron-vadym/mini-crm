from enum import Enum

from pydantic import BaseModel


class BaseModelORM(BaseModel):
    model_config = {"from_attributes": True}


class Role(str, Enum):
    admin = "admin"
    worker = "worker"


class Status(str, Enum):
    new = "new"
    assigned = "assigned"
    in_progress = "in_progress"
    done = "done"
    cancelled = "cancelled"
