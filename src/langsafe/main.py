import os

from fastapi import FastAPI
from langsafe.api.routes import router
from langsafe.config import setup_ngrok, PORT
import uvicorn

from langsafe.preload_asset import preload_asset

app = FastAPI(title="Langsafe Scanner")
app.include_router(router)
# preload_asset()


if __name__ == "__main__":
    setup_ngrok()
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)
