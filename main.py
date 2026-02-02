from fastapi import FastAPI, Request
import time, json

app = FastAPI()

storage_path = "storage"
connected_users = []

@app.post("/push")
async def push(request: Request):
    client_ip = request.client.host
#    print(client_ip)

    if client_ip not in connected_users:
        return {"status": "You need to be logged in", "code": 0}

    data = await request.json()

    full_data = {
        "date": time.time(),
        "client_ip": client_ip,
        "data": data,
        "code": 1
    }

    with open(storage_path + "//" + str(time.time()) + ".json", "w", encoding="utf-8") as f:
        json.dump(full_data, f, ensure_ascii=False, indent=4)

    return {"status": "OK", "code": 1}


@app.get("/ping")
async def ping():
    return {"status": "alive", "code": 2}

@app.get("/connect")
async def connect(request: Request):

    client_ip = request.client.host
    connected_users.append(client_ip)
    return {"status": "OK", "code": 3}



