from fastapi import FastAPI, Request

app = FastAPI()

storage = []


@app.post("/push")
async def push(request: Request):
    data = await request.json()
    storage.append(data)
    return {"ok": True}


@app.get("/get")
async def get():
    return {
        "count": len(storage),
        "data": storage
    }


@app.get("/ping")
async def ping():
    return {"status": "alive"}
