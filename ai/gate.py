from ai.config import AI_FOR_HOMEWORK
import requests

class Request:

    def __init__(self):
        self.settings = AI_FOR_HOMEWORK

    def make_request(self, data_text: str):

        server_ip = self.settings.get("server_address", "127.0.0.1")
        server_port = self.settings.get("server_port", "1234")  # LM Studio default
        system_instruction = self.settings.get("system_instruction", "")
        temperature = self.settings.get("temperature", 0)
        model_name = self.settings.get("model_name")

        main_url = f"http://{server_ip}:{server_port}/v1/chat/completions"

        data = {
            "model": model_name,
            "messages": [
                {
                    "role": "system",
                    "content": system_instruction
                },
                {
                    "role": "user",
                    "content": data_text
                }
            ],
            "temperature": temperature
        }

        response = requests.post(main_url, json=data)

        return response.json()

    def get_text(self, response):

        return response["choices"][0]["message"]["content"]