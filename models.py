from enum import Enum
from datetime import datetime

from typing import Optional
from pydantic import BaseModel


class EventTypeEnum(str, Enum):
    line_crossing = "line_crossing"
    depression = "depression"
    unknown = "unknown"


class RemarksEnum(str, Enum):
    no_remarks = "no_remarks"
    false_positive = "false_positive"
    duplicate = "duplicate"
    needs_further_review = "needs_further_review"


class EventLocation(BaseModel):
    lat: float
    lng: float


class NewEvent(BaseModel):
    event_type: EventTypeEnum
    system_id: str
    detection_time: Optional[datetime] = None
    image_data: Optional[str] = None
    video_data: Optional[str] = None
    location: Optional[EventLocation] = None


class UpdateEvent(BaseModel):
    remarks: RemarksEnum
