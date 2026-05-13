from fastapi import FastAPI
from routes import router

import routes

app = FastAPI()
app.include_router(router)