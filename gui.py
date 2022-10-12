from tkinter import *
import datetime as dt
import threading
import time


class window(Tk):

    def __init__(self, mode="Dark"):
        Tk.__init__(self)

        if mode == "Dark":
            self.back = "#000000"
            self.front = "#FFFFFF"
        elif mode == "Light":
            self.back = "#FFFFFF"
            self.front = "#000000"
        else:
            exit()

        # self.attributes("-fullscreen", True)
        self.geometry("480x800")
        self.height = 800  # self.winfo_screenheight()
        self.width = 480  # self.winfo_screenwidth()
        self.c = Canvas(
            self,
            bg=self.back,
            height=self.height,
            width=self.width,
            highlightthickness=0,
        )
        self.c.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.sosImage = PhotoImage(file=f"./sosButton{mode}.png")
        self.reminderImage = PhotoImage(file=f"./reminderButton{mode}.png")

        self.sosFrame = Frame(self, height=80, width=80, bg=self.back)
        self.reminderFrame = Frame(self, height=80, width=80, bg=self.back)

        self.sosButton = Button(
            self.sosFrame,
            image=self.sosImage,
            bg=self.back,
            command=self.SOS,
            relief=SUNKEN,
        )
        self.sosFrame.place(relx=0.085, rely=0.9495, anchor=CENTER)
        self.sosButton.place(relx=0.49, rely=0.49, anchor=CENTER)

        self.remindButton = Button(
            self.reminderFrame,
            image=self.reminderImage,
            bg=self.back,
            command=self.reminder,
            relief=SUNKEN,
        )
        self.reminderFrame.place(relx=0.255, rely=0.9495, anchor=CENTER)
        self.remindButton.place(relx=0.49, rely=0.49, anchor=CENTER)

        self.timeLabel = Label(self,
                               text=self.timeGet(),
                               bg=self.back,
                               fg=self.front,
                               font=("Arial", 12))
        self.timeLabel.place(relx=0.8, rely=0.95, anchor=CENTER)

        def updateTime():
            while True:
                time.sleep(30)
                self.timeLabel.configure(text=self.timeGet())

        threading.Thread(target=updateTime, daemon=True).start()

        self.mainloop()

    def SOS(self):
        # TODO - Me
        pass

    def reminder(self):
        # TODO - Shamantha
        pass

    def birthday(self):
        # TODO - Shamantha
        pass

    def finance(self):
        # TODO - Shamantha
        pass

    def getSettings(self):
        # TODO - Shamantha
        pass

    def timeGet(self):
        t = dt.datetime.now()
        weekday = t.strftime("%A")
        month = t.strftime("%B")
        day = str(int(t.strftime("%d")))
        year = t.strftime("%Y")
        hourMinute = t.strftime("%H:%M")
        return weekday + "\n" + month + " " + day + " " + year + "\n" + hourMinute

    def medicine(self):
        # TODO - Sanath
        pass

    def alarm(self):
        # TODO - Sanath
        pass

    def food(self):
        # TODO - Sanath
        pass

    def walk(self):
        # TODO - Sanath
        pass


x = window(mode="Light")
