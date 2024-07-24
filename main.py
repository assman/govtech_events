import helpers
from models import NewEvent, UpdateEvent

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health-check")
async def health_check():
    return {"status": "running"}


@app.get("/events")
async def retrieve_events(handled: bool | None = None):
    events = await helpers.get_all_events(handled)

    return events


@app.get("/events/count")
async def count_events(handled: bool | None = None):
    event_count = await helpers.count_devents(handled)

    response = {"count": event_count}

    return response


@app.get("/events/{event_uuid}")
async def retrieve_event(event_uuid: str):
    event = await helpers.get_one_event(event_uuid)

    return event


@app.post("/events")
async def create_event(event: NewEvent):
    created_event_id = await helpers.create_new_event(event)

    response = {"message": "JSON object successfully processed", "id": created_event_id}

    return response


@app.patch("/events/{event_uuid}")
async def update_event(event_uuid, event: UpdateEvent):
    updated_document = await helpers.update_event_remarks(event_uuid, event)

    return updated_document
