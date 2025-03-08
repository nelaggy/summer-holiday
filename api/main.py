@app.get("/")
async def root():
    return {"Summer": "Holiday"}