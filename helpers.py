from models import NewEvent

import uuid

from pymongo import DESCENDING
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.exceptions import HTTPException
from starlette.status import (
    HTTP_404_NOT_FOUND,
)

mongo_db_connection_url = "mongodb+srv://admin:Abc123456789@govtech.sxclkgn.mongodb.net/?retryWrites=true&w=majority&appName=govtech"

mongo_db_async_client = AsyncIOMotorClient(mongo_db_connection_url)

dev_db = mongo_db_async_client.dev

events_collection = dev_db.events


async def count_devents(handled):
    filters = {}

    if handled is not None:
        filters["handled"] = handled

    result = await events_collection.count_documents(filters)

    return result


async def get_all_events(handled):
    result = []

    filters = {}

    if handled is not None:
        filters["handled"] = handled

    events = events_collection.find(filters).sort("detection_time", DESCENDING)
    for event in await events.to_list(length=10):
        result.append(event)

    return result


async def get_one_event(event_id):
    result = await events_collection.find_one({"_id": event_id})

    if not result:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="Requested event does not exist"
        )

    return result


async def create_new_event(event: NewEvent):
    new_event = {
        "_id": str(uuid.uuid4()),
        "event_type": event.event_type,
        "system_id": event.system_id,
        "detection_time": event.detection_time,
        "image_data": event.image_data,
        "video_data": event.video_data,
        "location": {"lat": event.location.lat, "lng": event.location.lng},
        "handled": False,
        "remarks": "no_remarks",
    }

    result = await events_collection.insert_one(new_event)

    return result.inserted_id


async def update_event_remarks(event_id, updated_remarks):
    result = await events_collection.update_one(
        {"_id": event_id},
        {"$set": {"remarks": updated_remarks.remarks, "handled": True}},
    )

    if result.modified_count == 0:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="The event does not exist"
        )

    updated_document = await events_collection.find_one({"_id": event_id})

    return updated_document
