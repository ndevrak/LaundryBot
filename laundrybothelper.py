import json
from datetime import datetime as dt
from discord.ext import tasks

wash_time_def = 29
dry_time_def = 45

CHANNEL_ID = 823721207366680657

ADMINS = ['<@297502550037626891>','<@194640488043773952>',
'<@247226621377904641>','<@297509765347541016>']

laundry_json_path = "laundry.json"

TIME_FMT = "%y-%m-%d %H:%M"


class LaundryJsonHandler:
    def __init__(self, path):
        self.path = path
    
    def readJson(self):
        with open(self.path,'r') as file:
            data = json.load(file)
        return data
    
    def updateJson(self, newData):
        data = self.readJson()
        for k in newData.keys():
            data[k] = newData[k]
        with open(self.path, 'w') as file:
            json.dump(data, file)

class LaundryHandler:
    def __init__(self, client):
        global laundry_json_path
        self.messageActions = {
                "washer" : {"messages" : ['.w','.washer', '.d', '.drier'], "method" : self.machineMessageFunct},
                "reset" : {"messages" : ['.laundryreset'], "method" : self.resetMachines}
        }
        self.machines = ["w1","w2", "d1","d2"]
        self.LJH = LaundryJsonHandler(laundry_json_path)
        self.client = client
    
    async def LaundryMessageHandler(self, message):
        for key in self.messageActions:
            for m_start in self.messageActions[key]["messages"]:
                if message.content.startswith(m_start):
                    await self.messageActions[key]["method"](message)
                    break

    def atAuthor(self, message):
        return '<@' + str(message.author.id) + '>'

    async def machineMessageFunct(self, message):
        atAuth = self.atAuthor(message)
        splitMessage = message.content.split()
        try:
            machineNum = splitMessage[1]
        except IndexError:
            await message.channel.send("No machine number given " + atAuth + " have a space and the machine number. i.e. '.w 2'.")
            return
        machine = splitMessage[0][1] + machineNum
        minutes = self.machineStatus(machine)

        if minutes >0:
            await message.channel.send(atAuth + " the machine is in use by " + self.machineLastUser(machine) + " and has " + str(minutes) + " min left.")
            return
        
        try:
            runTime = splitMessage[2]
        except IndexError:
            if machine[0] == 'w':
                runTime = wash_time_def
            else:
                runTime = dry_time_def
        
        self.setMachine(machine, atAuth, runTime)
        await message.channel.send(atAuth + " started " + machine + " for " + str(runTime) + " minute(s).")
        return


    
    def readMachine(self, machine):
        data = self.LJH.readJson()
        return data[machine]

    def machineLastUser(self,machine):
        return self.LJH.readJson()[machine]["whoRan"]

    def machineStatus(self, machine):
        data = self.readMachine(machine)
        now = dt.now()
        machineStart = dt.strptime(data["lastRan"], TIME_FMT)
        minutes = int(data["runTime"] - (now-machineStart).total_seconds()/60)
        return minutes
    
    def setMachine(self, machine, atAuth, runTime):
        newData = {machine : {"lastRan":dt.now().strftime(TIME_FMT),"whoRan" : atAuth, "runTime" : int(runTime)  }}
        self.LJH.updateJson(newData)
    
    async def resetMachines(self, message):
        for machine in self.machines:
            self.setMachine(machine, self.atAuthor(message), 1)




#/
#{
#    "w1" : {"lastRan" : "22-10-25 10:45", "whoRan" : "<@297509765347541016>", "runTime" : 29},
#    "w2" : {"lastRan" : "00 00:00", "whoRan" : "<@297509765347541016>", "runTime" : 29},
#    "d1" : {"lastRan" : "00 00:00", "whoRan" : "<@297509765347541016>", "runTime" : 45},
#    "d2" : {"lastRan" : "00 00:00", "whoRan" : "<@297509765347541016>", "runTime" : 45}
#}
#