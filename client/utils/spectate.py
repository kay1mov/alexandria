import ctypes
from ctypes import wintypes
from PIL import Image
from io import BytesIO
import zipfile
import time


class Recorder:

    def __init__(self):
        self.video_filename = "record.stack"

    def screenshot(self):
        user32 = ctypes.windll.user32
        gdi32 = ctypes.windll.gdi32

        user32.SetProcessDPIAware()
        screen_width = user32.GetSystemMetrics(0)
        screen_height = user32.GetSystemMetrics(1)

        hdesktop = user32.GetDC(0)
        hmemdc = gdi32.CreateCompatibleDC(hdesktop)
        hbmp = gdi32.CreateCompatibleBitmap(hdesktop, screen_width, screen_height)
        gdi32.SelectObject(hmemdc, hbmp)

        SRCCOPY = 0x00CC0020
        gdi32.BitBlt(hmemdc, 0, 0, screen_width, screen_height, hdesktop, 0, 0, SRCCOPY)

        class BITMAPINFOHEADER(ctypes.Structure):
            _fields_ = [
                ("biSize", wintypes.DWORD),
                ("biWidth", wintypes.LONG),
                ("biHeight", wintypes.LONG),
                ("biPlanes", wintypes.WORD),
                ("biBitCount", wintypes.WORD),
                ("biCompression", wintypes.DWORD),
                ("biSizeImage", wintypes.DWORD),
                ("biXPelsPerMeter", wintypes.LONG),
                ("biYPelsPerMeter", wintypes.LONG),
                ("biClrUsed", wintypes.DWORD),
                ("biClrImportant", wintypes.DWORD)
            ]

        bmp_info = BITMAPINFOHEADER()
        bmp_info.biSize = ctypes.sizeof(BITMAPINFOHEADER)
        bmp_info.biWidth = screen_width
        bmp_info.biHeight = -screen_height
        bmp_info.biPlanes = 1
        bmp_info.biBitCount = 32
        bmp_info.biCompression = 0

        buffer_len = screen_width * screen_height * 4
        buffer = ctypes.create_string_buffer(buffer_len)

        gdi32.GetDIBits(hmemdc, hbmp, 0, screen_height, buffer, ctypes.byref(bmp_info), 0)

        image = Image.frombuffer("RGBA", (screen_width, screen_height), buffer, "raw", "BGRA", 0, 1)
        gdi32.DeleteObject(hbmp)
        gdi32.DeleteDC(hmemdc)
        user32.ReleaseDC(0, hdesktop)

        with BytesIO() as img_bytes:
            image.save(img_bytes, format="PNG")
            img_bytes.seek(0)
            timestamp_name = f"screenshot_{int(time.time() * 1000)}.png"
            with zipfile.ZipFile(self.video_filename, "a") as z:
                z.writestr(timestamp_name, img_bytes.read())

        print(f"Screenshot saved as {timestamp_name} in {self.video_filename}")


# class Player(tk.Tk):
#     def __init__(self, stack_file="record.stack", frame_delay=1000//30):
#         super().__init__()
#         self.title("Stack Player")
#         self.stack_file = stack_file
#         self.frame_delay = frame_delay  # ms
#         self.frames = []
#         self.current = 0
#
#         self.label = tk.Label(self)
#         self.label.pack()
#
#         self.load_frames()
#         self.after(0, self.play)
#
#     def load_frames(self):
#         with zipfile.ZipFile(self.stack_file, "r") as z:
#             for name in sorted(z.namelist()):
#                 with z.open(name) as f:
#                     img = Image.open(f).convert("RGBA")
#                     self.frames.append(ImageTk.PhotoImage(img))
#         print(f"{len(self.frames)} frames loaded")
#
#     def play(self):
#         if not self.frames:
#             return
#         self.label.config(image=self.frames[self.current - 1])
#         if self.current < len(self.frames):
#             self.label.config(image=self.frames[self.current])
#             self.current += 1
#             self.after(self.frame_delay, self.play)

recorder = Recorder()
while True:
    recorder.screenshot()
    time.sleep(1/60)