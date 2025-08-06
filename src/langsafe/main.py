from fastapi import FastAPI
from langsafe.api.routes import router
from langsafe.config import setup_ngrok

from langsafe.preload_asset import preload_asset
from ql_tracker.initialize import initialize

app = FastAPI(title="Langsafe Scanner")
app.include_router(router)
preload_asset()
url = setup_ngrok()
initialize(
    api_key="api_key_for_saving",
    host="https://689340e2e93cb765abe7b5cc--ql-tracker-dash.netlify.app"
)

