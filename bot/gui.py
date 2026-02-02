import customtkinter as ctk
from homework import homeworks



class App(ctk.CTk):

    def __init__(self):
        super(App, self).__init__()

        self.geometry("800x800")
        self.title("Editor")

        self.configure(background="gray")

    def confirm(self):

        date = self.choose_date_button.get()
        task_type = self.choose_task_type.get()
        subtask_type = self.choose_subtask_type.get()
        inner = self.homework_inner.get(0)
        result = self.result_input.get()





    def setup(self):

        self.choose_date_button = ctk.CTkEntry(self, placeholder_text="Date", width=200)
        self.choose_date_button.place(x=10, y=0)

        self.choose_task_type = ctk.CTkEntry(self, placeholder_text="Task Type", width=200)
        self.choose_task_type.place(x=220, y=0)

        self.choose_subtask_type = ctk.CTkEntry(self, placeholder_text="Subtask", width=200)
        self.choose_subtask_type.place(x=430, y=0)

        self.homework_inner = ctk.CTkTextbox(self, font=("Impact", 20), width=800, height=700)
        self.homework_inner.place(x=0, y=100)

        self.result_input = ctk.CTkEntry(self, placeholder_text="Result (%)")
        self.result_input.place(x=20, y=650)

        self.confirm_button = ctk.CTkButton(self, text="Confirm", command=self.confirm)
        self.confirm_button.place(x=500, y=650)

app = App()
app.setup()
app.mainloop()