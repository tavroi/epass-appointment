from Utils.config import *
from fastapi.security import OAuth2PasswordBearer
from Appointment import router as appointment
from Officers import router as officials

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app.include_router(appointment, prefix=BASE_ENDPOINT)
app.include_router(officials, prefix=BASE_ENDPOINT)


@app.get(f'{BASE_ENDPOINT}/health', tags=['health_check'])
async def check_health():
    return JSONResponse(content={"status": "Ok"}, status_code=HTTP_200_OK)


if __name__ == "__main__":
    if IS_LOCAL:
        uvicorn.run("main:app", host="localhost", port=8080, reload=True)
    else:
        uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)


