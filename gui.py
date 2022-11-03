from tkinter import *
import datetime as dt
import threading
import time
from gsmmodem.modem import GsmModem
from cryptography.fernet import Fernet
import os, csv
import speech_recognition as sr
import pygame
import requests
import pickle
import random

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

foodQuoteList=["Add 2 bananas today before or after food. \nBananas regulate your blood pressure, they provide you \nwith energy and have a positive influence on your digestion. \nit is very rich in fibres, which makes it ideal when it comes to \nintestinal problems. ",
      "Add an Apple today before or after food. \nApples are an incredibly nutritious fruit that offers \nmultiple health benefits. They’re rich in fiber and antioxidants. \nEating them is linked to a lower risk of many chronic \nconditions, including diabetes, heart disease, and cancer. \nApples may also promote weight loss and \nimprove gut and brain health.",
      "Add an Orange today before or after food. \nThe fiber in oranges can keep blood sugar levels \nin check and reduce high cholesterol to \nprevent cardiovascular disease.",
      "Add some slices of papaya today before or after food. \nA medium-sized papaya contains more than 200% of the vitamin C \nyou need per day, helping to reduce the \nrisk of heart disease and boost the immune system.",
      "Add dry fruits like Dehydrated Grapes/ Almonds/ Walnuts \nto your food today. Dry fruits are rich medium of carbohydrates \nand dietary fibers which help in bowel movements.Decreases cholestrol levels heart diseases, good for a healthy skin",
      "Add Grapes today before or after food. \nThey’re a rich source of beneficial plant compounds \nthat have been linked to numerous health \nbenefits, such as a lowered risk of heart \ndisease and certain types of cancer.",
      "Add few slices of watermelons today before or after food. \nThe nutrient in watermelons may also decrease the risk of heart \ndisease, cancer, and type 2 diabetes, \ndecrease effect of sunburn,hydrates your body"
      ]

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

        self.servDets()
        #self.attributes("-fullscreen", True)
        self.geometry("480x800")
        self.height = 800#self.winfo_screenheight()
        self.width = 480#self.winfo_screenwidth()

        def updateTime():
            while True:
                try:
                    self.timeLabel.configure(text=self.timeGet())
                    time.sleep(30)
                except:
                    pass

        threading.Thread(target=updateTime, daemon=True).start()

        def getServerDetails():
            while True:
                self.servDets()
                time.sleep(3600)

        threading.Thread(target=getServerDetails, daemon=True).start()

        def alarm():
            time.sleep(5)
            while True:
                if dt.datetime.now().strftime("%H:%M") in self.alarmList:
                    sound = pygame.mixer.Sound(
                        "/home/pi/Desktop/Ajjisstant-GUI/alarm.wav")
                    pygame.mixer.Sound.set_volume(sound, 1)
                    sound.play()
        
        threading.Thread(target=alarm, daemon=True).start()
        try:
            self.alarmList = pickle.load(open("alarms.txt", "rb"))
            self.emergencyContacts = pickle.load(open("emergency.txt", "rb"))
        except:
            self.servDets()
        
        threading.Thread(target=self.get_birthdayfromfile, daemon=True).start()
        
        def Food():
            while True:
                try:
                    self.foodLabel.configure(text=random.choice(foodQuoteList))
                    time.sleep(43200)
                except:
                    pass
        
        threading.Thread(target=Food, daemon=True).start()
        threading.Thread(target=self.financeFile, daemon=True).start()

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
        
        self.medicineFrame = Frame(self.mainframe,
                                   height=80,
                                   width=80,
                                   bg=self.back)

        self.callFrame = Frame(self.mainframe,
                                   height=80,
                                   width=80,
                                   bg=self.back)
        
        self.bdayFrame = Frame(self.mainframe,
                                   height=80,
                                   width=80,
                                   bg=self.back)
        
        self.financeFrame = Frame(self.mainframe,
                                   height=80,
                                   width=80,
                                   bg=self.back)

        self.sosButton = Button(
            self.sosFrame,
            image=self.sosImage,
            bg=self.back,
            command=lambda: self.SOS("+918073289563"),
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

        self.foodLabel = Label(
            self.mainframe,
            text=random.choice(foodQuoteList),
            bg=self.back,
            fg=self.front,
            font=("Arial", 12),
            width=450
        )
        
        self.foodLabel.place(relx=0.5, rely=0.7, anchor=CENTER)

        self.medicineButton = Button(
            self.medicineFrame,
            text="MEDICINE",
            bg=self.back,
            fg=self.front,
            command=self.medicine,
            relief=SUNKEN
        )

        self.medicineFrame.place(relx=0.5, rely=0.2, anchor=CENTER)
        self.medicineButton.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.callButton = Button(
            self.callFrame,
            text="CALL",
            bg=self.back,
            fg=self.front,
            command=self.call,
            relief=SUNKEN
        )

        self.callFrame.place(relx=0.45, rely=0.95, anchor=CENTER)
        self.callButton.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.bdayButton = Button(
            self.bdayFrame,
            text="BDAYS",
            bg=self.back,
            fg=self.front,
            command=self.birthdayWINDOW,
            relief=SUNKEN
        )

        self.bdayFrame.place(relx=0.5, rely=0.3, anchor=CENTER)
        self.bdayButton.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.financeButton = Button(
            self.financeFrame,
            text="FINANCE",
            bg=self.back,
            fg=self.front,
            command=self.financeWINDOW,
            relief=SUNKEN
        )

        self.financeFrame.place(relx=0.5, rely=0.1, anchor=CENTER)
        self.financeButton.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.mainloop()

    def call(self):
        self.mainframe.destroy()

        self.callWin = Frame(self,
                                   height=self.height,
                                   width=self.width,
                                   background=self.back)
        self.callWin.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.backFrame = Frame(self.callWin,
                                   height=80,
                                   width=80,
                                   bg=self.back)

        self.backButton = Button(
                    self.backFrame,
                    text="back",
                    bg=self.back,
                    fg=self.front,
                    command=self.exitCall,
                    relief=SUNKEN
                )

        self.emergencyButtonsList = []
        names = list(self.emergencyContacts.keys())

        for i in range(len(self.emergencyContacts)):
            self.emergencyButtonsList.append(Button(self.callWin, text=names[i], bg=self.back, fg=self.front, command=lambda: self.SOS(self.emergencyContacts[names[i]]), relief=SUNKEN))
            self.emergencyButtonsList[i].place(relx=0.5, rely=0.1*i)

        self.backFrame.place(relx=0.5, rely=0.9, anchor=CENTER)
        self.backButton.place(relx=0.5, rely=0.5, anchor=CENTER)

    def exitCall(self):
        self.callWin.destroy()
        self.mainPage()

    def SOS(self, NUMBER):
        PORT = "/dev/serial0"
        BAUDRATE = 115200
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

        self.backFrame = Frame(self.reminderFrame,
                                   height=80,
                                   width=80,
                                   bg=self.back)

        self.backButton = Button(
                    self.backFrame,
                    text="back",
                    bg=self.back,
                    fg=self.front,
                    command=self.exitReminder,
                    relief=SUNKEN
                )

        self.backFrame.place(relx=0.5, rely=0.9, anchor=CENTER)
        self.backButton.place(relx=0.5, rely=0.5, anchor=CENTER)

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

    def exitReminder(self):
        self.reminderFrame.destroy()
        self.mainPage()

    def deleteSound(self):
        os.remove("/home/pi/Desktop/Ajjisstant-GUI/reminder.wav")
        self.reminderFrame.destroy()
        self.mainPage()

    def playback(self):
        sound = pygame.mixer.Sound(
            "/home/pi/Desktop/Ajjisstant-GUI/reminder.wav")
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
        while True:
            todays_date = dt.datetime.now()
            self.namelist = []
            with open("/home/pi/Desktop/Ajjisstant-GUI/bday.csv", newline="") as birthday_file:
                date_sequence = csv.reader(birthday_file)
                for dates in date_sequence:
                    if "/".join((dates[1].split("/")[0], dates[1].split("/")[1])) == (todays_date.strftime("%d/%m")):
                        byear = int(dates[1].split("/")[2])
                        age = int(todays_date.strftime("%Y")) - byear
                        self.namelist.append((dates[0], str(age)))
                if int(str(todays_date.day)) == 1:
                    self.namelist.append(("Electricity Bill", 0))
                    self.namelist.append(("Rent", 0))
                    self.namelist.append(("Pension - VISIT BANK", 0))
            time.sleep(7200)

    def birthdayWINDOW(self):
        self.mainframe.destroy()
        self.birthdayFrame = Frame(self,
                                   height=self.height,
                                   width=self.width,
                                   background=self.back)
        self.birthdayFrame.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.backFrame = Frame(self.birthdayFrame,
                                   height=80,
                                   width=80,
                                   bg=self.back)

        self.backButton = Button(
                    self.backFrame,
                    text="back",
                    bg=self.back,
                    fg=self.front,
                    command=self.exitBirthdays,
                    relief=SUNKEN
                )

        self.backFrame.place(relx=0.5, rely=0.9, anchor=CENTER)
        self.backButton.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.bdayLabelList = []

        for i in range(len(self.namelist)):
            if self.namelist[i][0] in ("Electricity Bill", "Rent", "Pension - VISIT BANK"):
                t = self.namelist[i][0]
            else:
                t = self.namelist[i][0] + " turns " + self.namelist[i][1] + " today."
            self.bdayLabelList.append(Label(self.birthdayFrame, text=t, bg=self.back, fg=self.front, font=("Arial", 12), width=450))
            self.bdayLabelList[i].place(relx=0.5, rely=0.1*(i+1), anchor=CENTER)


    def exitBirthdays(self):
        self.birthdayFrame.destroy()
        self.mainPage()

    def get_details(self):
        self.financefile = open("/home/pi/Desktop/Ajjisstant-GUI/f.file", "rb")
        self.enc_fin = self.financefile.read()
        self.financefile.close()

        self.dec_fin = fernet.decrypt(self.enc_fin).decode()
        self.req_list = self.dec_fin.split("\n")
        self.accounts = []
        for account in self.req_list:
            self.accounts.append(account.split(","))
        self.finance = []
        for i in range(len(self.accounts)):
            self.finance.append({
                "accno": self.accounts[i][0],
                "branch": self.accounts[i][2],
                "loans": self.accounts[i][1],
            })

    def financeWINDOW(self):
        self.mainframe.destroy()
        self.finFrame = Frame(self,
                                   height=self.height,
                                   width=self.width,
                                   background=self.back)
        self.finFrame.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.backFrame = Frame(self.finFrame,
                                   height=80,
                                   width=80,
                                   bg=self.back)

        self.backButton = Button(
                    self.backFrame,
                    text="back",
                    bg=self.back,
                    fg=self.front,
                    command=self.exitFinance,
                    relief=SUNKEN
                )

        self.backFrame.place(relx=0.5, rely=0.9, anchor=CENTER)
        self.backButton.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.financeLabelList = []

        for i in range(len(self.finance)):
            t = "Number: " + self.finance[i]["accno"] + "        Branch: " + self.finance[i]["branch"] + "        Loan: " + self.finance[i]["loans"] + " Rupees"
            self.financeLabelList.append(Label(self.finFrame, text=t, bg=self.back, fg=self.front, font=("Arial", 12), width=450))
            self.financeLabelList[i].place(relx=0.5, rely=0.1*(i+1), anchor=CENTER)


    def exitFinance(self):
        self.finFrame.destroy()
        self.mainPage()

    def financeFile(self):
        while True:
            try:
                x = requests.get('https://old-person.herokuapp.com/finance/select?username=test').json()["data"][1]
                accounts = x["accno"].split("|")
                loans = x["loans"].split("|")
                branch = x["branch"].split("|")
                self.content = ""
                for i in range(len(accounts)):
                    self.content += accounts[i]
                    self.content += ","
                    self.content += loans[i]
                    self.content += ","
                    self.content += branch[i]
                    self.content += "\n"
                
                self.enc_shit = fernet.encrypt(self.content[:-1].encode())
                with open("/home/pi/Desktop/Ajjisstant-GUI/f.file", "wb") as file:
                    file.write(self.enc_shit)
                self.get_details()
                time.sleep(7200)
            except:
                time.sleep(30)

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
        self.mainframe.destroy()

        self.medFrame = Frame(self,
                                   height=self.height,
                                   width=self.width,
                                   background=self.back)
        self.medFrame.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.backFrame = Frame(self.medFrame,
                                   height=80,
                                   width=80,
                                   bg=self.back)

        self.backButton = Button(
                    self.backFrame,
                    text="back",
                    bg=self.back,
                    fg=self.front,
                    command=self.exitMedicine,
                    relief=SUNKEN
                )

        self.backFrame.place(relx=0.5, rely=0.9, anchor=CENTER)
        self.backButton.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.medLabelList = []

        for i in range(len(self.medicineList)):
            t = "Name: " + self.medicineList[i]["name"] + "        " + "Times: " + ", ".join(self.medicineList[i]["time"]) + "\n" + "Per Tablet: " + self.medicineList[i]["dosage"] + "        " + "Left: " + str(self.medicineList[i]["inventory"])
            self.medLabelList.append(Label(self.medFrame, text=t, bg=self.back, fg=self.front, font=("Arial", 12), width=450))
            self.medLabelList[i].place(relx=0.5, rely=0.1*(i+1), anchor=CENTER)

    def exitMedicine(self):
        self.medFrame.destroy()
        self.mainPage()

    def walk(self):
        # TODO - Sanath
        pass

    def servDets(self):
        try:
            self.alarmList = requests.get('https://old-person.herokuapp.com/alarms/select?username=test').json()["data"][1]
            newfile = open("alarms.txt", "wb")
            pickle.dump(self.alarmList, newfile)
            newfile.close()
        except:
            self.alarmList = pickle.load(open("alarms.txt", "rb"))

        try:
            x = requests.get('https://old-person.herokuapp.com/emergency/select?username=test').json()["data"][0][1]
            
            self.emergencyContacts = {}
            for i in x:
                self.emergencyContacts[i.split("|")[0]] = "+91" + i.split("|")[1]

            newfile = open("emergency.txt", "wb")
            pickle.dump(self.emergencyContacts, newfile)
            newfile.close()
        except:
            self.emergencyContacts = {"Arnav" : "+919845045447", "Sham" : "+923473845"}

        try:
            self.birthdays = requests.get('https://old-person.herokuapp.com/birthdays/select?username=test').json()["data"][1]
            newfile = open("/home/pi/Desktop/Ajjisstant-GUI/bday.csv", "w", newline="")
            writ = csv.writer(newfile)
            for i in self.birthdays:
                writ.writerow([i, self.birthdays[i]])
            newfile.close()
        except:
            pass


        try:
            x = requests.get('https://old-person.herokuapp.com/medicines/select?username=test').json()["data"][1]
            self.medicineList = []
            for i in x:
                self.medicineList.append({"name":i, "time":x[i]["time"], "dosage":x[i]["dosage"], "inventory":x[i]["inventory"]})
            newfile = open("/home/pi/Desktop/Ajjisstant-GUI/medicines.txt", "wb")
            pickle.dump(self.medicineList, newfile)
            newfile.close()
        except:
            self.medicineList = pickle.load(open("medicines.txt", "rb"))

x = window(mode="Light")
