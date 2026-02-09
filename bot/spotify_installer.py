import os

import requests
import time
import traceback


class SpotifyInstaller:

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0",
            "Origin": "https://spotdown.org",
            "Referer": "https://spotdown.org/track",
            "Accept": "*/*",
        }

        self.check_url = "https://spotdown.org/api/check-direct-download"
        self.download_url = "https://spotdown.org/api/download"

        self.session = requests.Session()
        self.session.headers.update(self.headers)

        self.progress_bar_callback = None

    def download_track(
        self,
        track_link: str,
        save_path: str | None = None
    ):
        if save_path is None:
            save_path = f"spotify_downloads/song_{int(time.time())}.mp3"

        try:
            # 1️⃣ check
            self.session.get(
                self.check_url,
                params={"url": track_link},
                timeout=15
            )

            # 2️⃣ download
            payload = {"url": track_link}

            with self.session.post(
                self.download_url,
                json=payload,
                stream=True,
                timeout=60
            ) as r:

                r.raise_for_status()

                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                with open(save_path, "wb") as f:
                    for chunk in r.iter_content(8192):
                        if chunk:
                            f.write(chunk)


        except Exception:
            print(traceback.format_exc())
            return None

        return save_path
