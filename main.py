from ai.audio_to_text import Transcriber
from api.api import Auth
from bot.config import *
from ai.gate import Request

import json
import time
import requests


class App:

    def __init__(self):

        print("[INIT] Initializing App")

        self.auth = Auth()
        print("[INIT] Auth initialized:", self.auth)

        self.gate = Request()
        print("[INIT] Gate initialized:", self.gate)

        self.transcriber = Transcriber()
        print("[INIT] Transcriber initialized:", self.transcriber)

        self.available_homeworks = []

        print("[INIT] Loading homework base...")
        self.homework_base = self.load_homework_base()
        print("[INIT] Homework base loaded:", self.homework_base)

        self.level_id = 6
        print("[INIT] Level ID:", self.level_id)


    def load_homework_base(self):

        print("[LOAD] Opening homework base file:", homework_directory)

        with open(homework_directory, encoding='utf-8') as f:

            data = json.load(f)

            print("[LOAD] Homework base content:")
            print(data)

            return data


    def load_homeworks(self):

        print("[LOAD] Loading homeworks...")

        self.available_homeworks = [
            {'percentage': 32, 'strike_percentage': 0, 'passed': True, 'date': '2026-02-15', 'day_of_month': 15, 'week_day': 'S', 'is_current': False, 'unit': 8, 'subunit': 3, 'day_of_unit': 6},
            {'percentage': 0, 'strike_percentage': 0, 'passed': True, 'date': '2026-02-16', 'day_of_month': 16, 'week_day': 'M', 'is_current': False, 'unit': 8, 'subunit': 3, 'day_of_unit': 7},
            {'percentage': 19, 'strike_percentage': 19, 'passed': True, 'date': '2026-02-17', 'day_of_month': 17, 'week_day': 'T', 'is_current': False, 'unit': 9, 'subunit': 1, 'day_of_unit': 1},
            {'percentage': 0, 'strike_percentage': 0, 'passed': True, 'date': '2026-02-18', 'day_of_month': 18, 'week_day': 'W', 'is_current': False, 'unit': 9, 'subunit': 1, 'day_of_unit': 2},
            {'percentage': 0, 'strike_percentage': 0, 'passed': True, 'date': '2026-02-19', 'day_of_month': 19, 'week_day': 'T', 'is_current': True, 'unit': 9, 'subunit': 2, 'day_of_unit': 3},
        ]

        print("[LOAD] Homeworks loaded:")
        print(self.available_homeworks)


    def build_homework_table(self):

        print("[BUILD] Building homework table")

        table = {}

        for day in self.available_homeworks:

            print("[BUILD] Processing day:", day)

            table[day.get("date")] = {

                "passed": day["passed"],
                "day_of_month": day["day_of_month"],
                "week_day": day["week_day"],
                "is_current": day["is_current"],
                "unit": day["unit"],
                "subunit": day["subunit"],
                "day_of_unit": day["day_of_unit"],
                "date": day["date"]
            }

        print("[BUILD] Final table:")
        print(table)

        return table


    def get_uncompleted_homeworks(self):

        print("[CHECK] Checking uncompleted homeworks")

        if self.available_homeworks == []:

            print("[CHECK] Homeworks empty, loading...")

            self.load_homeworks()

        current_homeworks_table = self.build_homework_table()

        print("[CHECK] Current table:")
        print(current_homeworks_table)

        not_completed_homeworks = []

        for date in current_homeworks_table:

            print("[CHECK] Checking date:", date)

            if date not in self.homework_base.keys():

                print("[CHECK] Not completed:", date)

                not_completed_homeworks.append(
                    current_homeworks_table[date]
                )

            else:

                print("[CHECK] Already completed:", date)

        print("[CHECK] Final uncompleted list:")
        print(not_completed_homeworks)

        return not_completed_homeworks


    def download_listening_audio_file(self, response):

        print("[DOWNLOAD] Download listening audio")

        print("[DOWNLOAD] Response:")
        print(response)

        excs = response.get("exercises")

        link = None

        for exercise in excs:

            print("[DOWNLOAD] Checking exercise:", exercise)

            if exercise.get("exercise", {}).get("url"):

                link = exercise.get("exercise").get("url")

                print("[DOWNLOAD] Found link:", link)

                break

        if link is None:

            print("[ERROR] Audio link not found")

            return FileNotFoundError("Audio file not found")

        print("[DOWNLOAD] Downloading from:", link)

        filepath = audio_files_directory / f"audio_{time.time()}.mp3"

        print("[DOWNLOAD] Saving to:", filepath)

        with requests.get(link, stream=True) as r:

            print("[DOWNLOAD] Response status:", r.status_code)

            r.raise_for_status()

            with open(filepath, "wb") as f:

                for chunk in r.iter_content(chunk_size=8192):

                    f.write(chunk)

        print("[DOWNLOAD] Saved OK")

        return filepath


    def do_homework(self, data):

        print("\n======================")
        print("[HW] DO HOMEWORK")
        print("======================")

        print("[HW] Input data:")
        print(data)

        date = data.get("date")

        unit = data.get("unit")

        subunit = data.get("subunit")

        day_of_unit = data.get("day_of_unit")

        homework_info = {

            "level_id": self.level_id,

            "unit": unit,

            "subunit": subunit,

            "day": day_of_unit,

            "date": date,

            "from": None,

            "to": None,

            "book_type": None
        }

        print("[HW] Homework info:")
        print(homework_info)


        results = {}

#        for task in self.auth.available_homework_types:
        for task in ["extra_task"]:
            print("[HW] Task:", task)

            results[task] = {}

            for subtask in self.auth.available_homework_subtypes:

                print("[HW] Subtask:", subtask)

                results[task][subtask] = {}


#        for task in self.auth.available_homework_types:
        for task in ["extra_task"]:

            for subtask in self.auth.available_homework_subtypes:

                print("\n[REQUEST] Getting homework")

                print("[REQUEST] Task:", task)

                print("[REQUEST] Subtask:", subtask)

                h = self.auth.get_homework(task, subtask, homework_info)
                if h is None:
                    print(f"[INFO] {task} - {subtask} doesn't exist")
                    continue

                print("[REQUEST] Response:")
                print(h)


                if h.get("message") == "You have finished this task before!":

                    print("[REQUEST] Already finished")

                    continue


                data = h.get("data")

                print("[REQUEST] Data:")
                print(data)


                if subtask.lower() == "listening":

                    print("[LISTENING] Processing listening")

                    audio_path = self.download_listening_audio_file(data)

                    print("[LISTENING] Audio path:", audio_path)

                    audio_text = self.transcriber.transcribe(audio_path)

                    print("[LISTENING] Audio text:")
                    print(audio_text)

                    data["audio_text"] = audio_text


                print("[REQUEST] Sending to AI")

                result = self.gate.make_request(data)

                print("[REQUEST] AI raw result:")
                print(result)

                text = self.gate.get_text(result)

                print("[RESULT] Final text:")
                print(text)

                results[task][subtask] = text


        print("\n[RESULT] FINAL RESULTS:")
        print(results)


    def check(self):

        print("[CHECK] Running check")

        uncompleted_homeworks = self.get_uncompleted_homeworks()

        print("[CHECK] Found:", uncompleted_homeworks)

        for homework in uncompleted_homeworks:

            print("[CHECK] Starting homework:", homework)

            self.do_homework(homework)

            return


        print("[CHECK] No homework found")


print("\n========== START ==========\n")

app = App()

app.load_homeworks()

app.check()

print("\n========== END ==========\n")
