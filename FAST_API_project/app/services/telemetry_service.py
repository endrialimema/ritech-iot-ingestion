from typing_extensions import Literal

from ..db.mongodb import db

async def create_telemetry(data):    
    
    print("INSERT CALLED", data.dict())
    result = await db.telemetry.insert_one(data.dict())
    print("INSERT DONE", result.inserted_id)
    return {"id": str(result.inserted_id)}