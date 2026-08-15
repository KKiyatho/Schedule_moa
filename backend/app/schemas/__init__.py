"""
Pydantic Schemas for API request/response validation
Import all schema classes from individual modules
"""

# User schemas
from app.schemas.user import (
    UserBase,
    UserCreate,
    UserLogin,
    UserUpdate,
    UserResponse,
    UserWithCalendars,
    TokenResponse,
)

# Calendar schemas
from app.schemas.calendar import (
    CalendarBase,
    CalendarCreate,
    CalendarUpdate,
    CalendarResponse,
    CalendarWithItems,
)

# Schedule Item schemas
from app.schemas.schedule_item import (
    ScheduleItemBase,
    ScheduleItemCreate,
    ScheduleItemUpdate,
    ScheduleItemResponse,
    ScheduleItemListResponse,
    ScheduleItemBulkCreate,
    TagResponse,
)

# Document schemas
from app.schemas.document import (
    DocumentBase,
    DocumentCreate,
    DocumentResponse,
    DocumentWithItems,
    DocumentProcessingRequest,
    DocumentProcessingResponse,
)

# Tag schemas
from app.schemas.tag import (
    TagBase,
    TagCreate,
    TagUpdate,
    TagResponse as TagResponseSchema,
)

__all__ = [
    # User
    "UserBase",
    "UserCreate",
    "UserLogin",
    "UserUpdate",
    "UserResponse",
    "UserWithCalendars",
    "TokenResponse",
    # Calendar
    "CalendarBase",
    "CalendarCreate",
    "CalendarUpdate",
    "CalendarResponse",
    "CalendarWithItems",
    # Schedule Item
    "ScheduleItemBase",
    "ScheduleItemCreate",
    "ScheduleItemUpdate",
    "ScheduleItemResponse",
    "ScheduleItemListResponse",
    "ScheduleItemBulkCreate",
    "TagResponse",
    # Document
    "DocumentBase",
    "DocumentCreate",
    "DocumentResponse",
    "DocumentWithItems",
    "DocumentProcessingRequest",
    "DocumentProcessingResponse",
    # Tag
    "TagBase",
    "TagCreate",
    "TagUpdate",
]
