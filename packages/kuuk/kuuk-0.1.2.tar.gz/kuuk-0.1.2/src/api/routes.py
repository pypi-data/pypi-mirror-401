import logging

from pydantic_core import ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse
from entities.stage import Stage
from server.database import db
from api.serializers.register import StageSchema

logger = logging.getLogger("app")


async def register_entity(request: Request):
    data = await request.json()
    try:
        serializer = StageSchema(**data)
        new_stage = Stage(**serializer.model_dump())
        new_stage.save(db.get_session())
        return JSONResponse({"status": "registered",
                            "data": serializer.model_dump_json()}
                            )
    except ValidationError as e:
        return JSONResponse({"error": e.errors()}, status_code=400)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)


async def health(request: Request):
    return JSONResponse({"status": "ok"})