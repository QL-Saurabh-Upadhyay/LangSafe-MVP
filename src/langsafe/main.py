from fastapi import FastAPI
from langsafe.api.routes import router
from langsafe.config import setup_ngrok

from langsafe.preload_asset import preload_asset

app = FastAPI(title="Langsafe Scanner")
app.include_router(router)
preload_asset()
setup_ngrok()

