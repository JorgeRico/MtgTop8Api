from fastapi.responses import JSONResponse
from fastapi import HTTPException, Request

async def notFound(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code = exc.status_code,
        content = {
            "detail": [
                {
                    "type": "error",
                    "loc": [
                        "path",
                        "id"
                    ],
                    "msg": f"Not found",
                    "input": ""
                }
            ]
        }
    )