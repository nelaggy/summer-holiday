from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/search")
async def search(q: str = Query(..., min_length=1, title="Search Query")):
    # Simulated search results
    results = [
        {"id": 1, "name": "Result 1"},
        {"id": 2, "name": "Result 2"},
    ]
    
    return {"query": q, "results": results}