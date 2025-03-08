from fastapi import FastAPI
from search import router as search_router

app = FastAPI()

@app.get("/")
async def root():
    return {"Summer": "Holiday"}

app.include_router(search_router)