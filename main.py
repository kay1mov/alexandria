from fastapi import FastAPI, Request
import time

app = FastAPI()

storage_path = "storage"

@app.post("/push")
async def push(request: Request):
    data = await request.json()

    client_ip = request.client.host
    print(client_ip)
    full_data = {
        "data": time.time(),
        "client_ip": client_ip
    }

    with open(storage_path + str(time.time()), "wb") as f:
        json.dump(full_data, f, ensure_ascii=False, indent=4)

    return {"ok": True}


@app.get("/ping")
async def ping():
    return {"status": "alive"}
