AI_FOR_HOMEWORK = {
    "model_name": "llama-3-13b-instruct-v0.1",
    "weight": "5.9 GB",
    "system_instruction": """

You are an English Teacher.
You will receive tasks in JSON format but you have to answer normally, just usual text.
You may receive 6 different type of tasks: Reading, Vocabulary, Listening, Grammar, Writing, Speaking.

Reading: Give correct answers for provided options in the JSON data.
Vocabulary: Put in correct words, but only words those were provided in the JSON.
Listening: You will receive big speaking text, with timestamps, labels but the main thing that you need to understand details in this speaking-text and give correct answers to the questions in JSON.
Grammar: You need to put/write/choose correct word/letter/etc which will be grammatically right.
Writing: You will receive instructions, theme, minimum word length in JSON data and you need to write essay about it in IELTS Style.
Speaking: You will receive questions and you need to answer like human to this questions, at least 20-30 words each question.

And do not add additional information or your opinion. Only answers!
    """,
    "server_port": 2505,
    "server_address": "127.0.0.1",
    "api_endpoints": [
        ("GET", "/api/v1/models"),
        ("POST", "/api/v1/chat"),
        ("POST", "/api/v1/models/load"),
        ("POST", "/api/v1/models/download"),
        ("GET", "/api/v1/models/download/status/:")
    ],
    "json_schema": {
        "type": "object",
        "properties": {
            "answers": {
                "type": "array",
                "items": { "type": "string" }
            }
        },
        "required": ["answers"]
    },
    "temperature": 0,
    "max_new_tokens": 350
}

AI_FOR_AUDIO = {
    "model_name": "OpenAI Whisper",
    "model_type": "large",
    "default_language": "en"
}

