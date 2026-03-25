from fastapi import FastAPI

from app.api import meals, health
from app.database import init_db

app = FastAPI(title="Meal Service", version="0.1.0")


@app.on_event("startup")
async def startup_event():
    await init_db()


app.include_router(meals.router)
app.include_router(health.router)
