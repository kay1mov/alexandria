import requests

response = {
    "asd": 123
}

r = requests.post("https://alexandriatorch.onrender.com/push", json=response)
print(r.json())