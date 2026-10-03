from fastapi import FastAPI
from api.routers.workouts import router as workouts_router

app = FastAPI(
    title="RepWise API",
    version="0.1.0"
)


app.include_router(workouts_router)


@app.get("/")
def home():
    return {"message": "RepWise API is running"}