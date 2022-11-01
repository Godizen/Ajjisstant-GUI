from tkinter import *
import datetime as dt
import threading
import time
from gsmmodem.modem import GsmModem
from cryptography.fernet import Fernet
import os, csv
import speech_recognition as sr
import pygame

if not os.path.exists("/home/pi/Desktop/Ajjisstant-GUI/filekey.lib"):
    key = Fernet.generate_key()
    with open("/home/pi/Desktop/Ajjisstant-GUI/filekey.key", "wb") as filekey:
        filekey.write(key)
    create = open("/home/pi/Desktop/Ajjisstant-GUI/f.file", "wb")
    create.close()

with open("/home/pi/Desktop/Ajjisstant-GUI/filekey.key", "rb") as filekey:
    key = filekey.read()
fernet = Fernet(key)

pygame.mixer.init()

class window(Tk):

    def __init__(self, mode="Dark"):
        Tk.__init__(self)

        if mode == "Dark":
            self.mode = "Dark"
            self.back = "#000000"
            self.front = "#FFFFFF"
        elif mode == "Light":
            self.mode = "Light"
            self.back = "#FFFFFF"
            self.front = "#000000"
        else:
            exit()

        self.attributes("-fullscreen", True)
        self.height = self.winfo_screenheight()
        self.width = self.winfo_screenwidth()

        self.mainPage()

    def mainPage(self):

        self.mainframe = Frame(self,
                               height=self.height,
                               width=self.width,
                               bg=self.back)
        self.mainframe.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.c = Canvas(
            self.mainframe,
            bg=self.back,
            height=self.height,
            width=self.width,
            highlightthickness=0,
        )
        self.c.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.sosImage = PhotoImage(
            file=f"/home/pi/Desktop/Ajjisstant-GUI/sosButton{self.mode}.png")
        self.reminderImage = PhotoImage(
            file=
            f"/home/pi/Desktop/Ajjisstant-GUI/reminderButton{self.mode}.png")

        self.sosFrame = Frame(self.mainframe,
                              height=80,
                              width=80,
                              bg=self.back)
        self.reminderFrame = Frame(self.mainframe,
                                   height=80,
                                   width=80,
                                   bg=self.back)

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

        self.timeLabel = Label(
            self.mainframe,
            text=self.timeGet(),
            bg=self.back,
            fg=self.front,
            font=("Arial", 12),
        )
        self.timeLabel.place(relx=0.8, rely=0.95, anchor=CENTER)

        def updateTime():
            while True:
                time.sleep(30)
                self.timeLabel.configure(text=self.timeGet())

        threading.Thread(target=updateTime, daemon=True).start()

        self.mainloop()

    def SOS(self):
        PORT = "/dev/serial0"
        BAUDRATE = 115200
        NUMBER = "+919449087092"
        PIN = None
        waitingForModemToRespondInSeconds = 10

        modem = GsmModem(PORT, BAUDRATE)
        modem.connect(PIN, waitingForModemToRespondInSeconds)
        modem.waitForNetworkCoverage(30)
        call = modem.dial(NUMBER)
        wasAnswered = False
        while call.active:
            if call.answered:
                wasAnswered = True
                time.sleep(3.0)
                try:
                    if call.active:
                        print("Hanging up call...")
                        call.hangup()
                        print("Call has been ended by remote party")
                except:
                    pass
            else:
                time.sleep(0.5)
        if not wasAnswered:
            print("Call was not answered by remote party")
        print("Done.")
        modem.close()

    def reminder(self):
        self.mainframe.destroy()

        self.reminderFrame = Frame(self,
                                   height=self.height,
                                   width=self.width,
                                   background=self.back)
        self.reminderFrame.place(relx=0.5, rely=0.5, anchor=CENTER)

        if os.path.exists("/home/pi/Desktop/Ajjisstant-GUI/reminder.wav"):
            self.show = Button(self.reminderFrame,
                               text="Play",
                               command=self.playback)
            self.show.place(relx=0.5, rely=0.5, anchor=CENTER)
            self.deleteButton = Button(self.reminderFrame,
                                       text="Delete",
                                       command=self.deleteSound)
            self.deleteButton.place(relx=0.5, rely=0.6, anchor=CENTER)
        else:
            self.recordButton = Button(self.reminderFrame,
                                       text="Record",
                                       command=self.recordReminder)
            self.recordButton.place(relx=0.5, rely=0.5, anchor=CENTER)

    def deleteSound(self):
        os.remove("/home/pi/Desktop/Ajjisstant-GUI/reminder.wav")
        self.reminderFrame.destroy()
        self.mainPage()

    def playback(self):
        sound = pygame.mixer.Sound("/home/pi/Desktop/Ajjisstant-GUI/reminder.wav")
        pygame.mixer.Sound.set_volume(sound, 1)
        sound.play()

    def recordReminder(self):
        rec = sr.Recognizer()
        mic = sr.Microphone()
        with mic as source:
            audio = rec.listen(source)
        open("/home/pi/Desktop/Ajjisstant-GUI/reminder.wav",
             "wb").write(audio.get_wav_data())
        self.reminderFrame.destroy()
        self.mainPage()

    def get_birthdayfromfile(self):
        todays_date = dt.datetime.now()

        self.namelist = []
        with open("/home/pi/Desktop/Ajjisstant-GUI/bday.csv",
                  newline="") as birthday_file:
            date_sequence = csv.reader(birthday_file)
            for dates in date_sequence:
                if dates[1][:5] == (str(todays_date.day) + "/" +
                                    str(todays_date.month)):
                    if int(dates[1][6:]) <= int(str(todays_date.year)[2:]):
                        byear = int("20" + str(dates[1][6:]))
                    else:
                        byear = int("19" + str(dates[1][6:]))
                    age = todays_date.year - byear
                    self.namelist.append((dates[0], age))
            if int(str(todays_date.day)) == int(1):
                self.reminders.append(("Electricity Bill", 0))
                self.reminders.append(("Rent", 0))
                self.reminders.append(("Pension - VISIT BANK", 0))

    def updatebirthdayfile():
        # CONNECT TO SERVER FIRST, THEN GET THE CSV FILE FROM THE SERVER
        newfile = open("/home/pi/Desktop/Ajjisstant-GUI/newfile.bday")
        newfile.close()
        os.delete("/home/pi/Desktop/Ajjisstant-GUI/bday.csv")
        os.rename(
            "/home/pi/Desktop/Ajjisstant-GUI/newfile.bday",
            "/home/pi/Desktop/Ajjisstant-GUI/bday.csv",
        )

    def get_details(self):
        self.financefile = open("/home/pi/Desktop/Ajjisstant-GUI/f.file", "rb")
        self.enc_fin = self.financefile.read()
        self.financefile.close()

        self.dec_fin = fernet.decrypt(self.enc_fin)
        self.req_list = self.dec_fin.split("\n")
        self.accounts = []
        for account in self.req_list:
            self.accounts.append(account.split(","))
        self.finance = {}
        for i in range(len(self.accounts)):
            self.finance[i] = {
                "Account number:": self.accounts[i][0],
                "Name of branch:": self.accounts[i][1],
                "Pending loans": self.accounts[i][2],
            }

    def fetch_server_file(self):
        # GET A NEW F.FILE
        with open("/home/pi/Desktop/Ajjisstant-GUI/newf.file",
                  "rb") as self.file:
            self.content = self.file.read()
        self.enc_shit = fernet.encrypt(self.content)

        os.remove("/home/pi/Desktop/Ajjisstant-GUI/f.file")
        os.remove("/home/pi/Desktop/Ajjisstant-GUI/newf.file")
        with open("/home/pi/Desktop/Ajjisstant-GUI/f.file", "wb") as file:
            file.write(self.enc_shit)

    def timeGet(self):
        t = dt.datetime.now()
        weekday = t.strftime("%A")
        month = t.strftime("%B")
        day = str(int(t.strftime("%d")))
        year = t.strftime("%Y")
        hourMinute = t.strftime("%H:%M")

        if hourMinute == "00:00":
            self.reminders = []
            self.fetch_server_file()
            self.get_details()
            self.updatebirthdayfile()
            self.get_birthdayfromfile()
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


x = window(mode="Dark")
