# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from .._utils import PropertyInfo
from .._models import BaseModel
from .task_message import TaskMessage
from .task_message_delta import TaskMessageDelta
from .task_message_content import TaskMessageContent

__all__ = [
    "TaskMessageUpdate",
    "StreamTaskMessageStart",
    "StreamTaskMessageDelta",
    "StreamTaskMessageFull",
    "StreamTaskMessageDone",
]


class StreamTaskMessageStart(BaseModel):
    """Event for starting a streaming message"""

    content: TaskMessageContent
    """Content type for storing raw Claude SDK messages."""

    index: Optional[int] = None

    parent_task_message: Optional[TaskMessage] = None
    """Represents a message in the agent system.

    This entity is used to store messages in MongoDB, with each message associated
    with a specific task.
    """

    type: Literal["start"] = "start"


class StreamTaskMessageDelta(BaseModel):
    """Event for streaming chunks of content"""

    delta: Optional[TaskMessageDelta] = None
    """Delta for text updates"""

    index: Optional[int] = None

    parent_task_message: Optional[TaskMessage] = None
    """Represents a message in the agent system.

    This entity is used to store messages in MongoDB, with each message associated
    with a specific task.
    """

    type: Literal["delta"] = "delta"


class StreamTaskMessageFull(BaseModel):
    """Event for streaming the full content"""

    content: TaskMessageContent
    """Content type for storing raw Claude SDK messages."""

    index: Optional[int] = None

    parent_task_message: Optional[TaskMessage] = None
    """Represents a message in the agent system.

    This entity is used to store messages in MongoDB, with each message associated
    with a specific task.
    """

    type: Literal["full"] = "full"


class StreamTaskMessageDone(BaseModel):
    """Event for indicating the task is done"""

    index: Optional[int] = None

    parent_task_message: Optional[TaskMessage] = None
    """Represents a message in the agent system.

    This entity is used to store messages in MongoDB, with each message associated
    with a specific task.
    """

    type: Literal["done"] = "done"


TaskMessageUpdate: TypeAlias = Annotated[
    Union[StreamTaskMessageStart, StreamTaskMessageDelta, StreamTaskMessageFull, StreamTaskMessageDone],
    PropertyInfo(discriminator="type"),
]
