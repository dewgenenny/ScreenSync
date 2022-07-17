from PIL import ImageGrab
from PIL import ImageStat
from PIL import ImageEnhance
from tkinter import *
from flux_led import WifiLedBulb, BulbScanner
import time
import tkinter as tk
import configparser
import sys, os
from colorthief import ColorThief

if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app
    # path into variable _MEIPASS'.
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

config = configparser.ConfigParser()
config.read('config.ini')

if not config.has_section('settings'):
    config['settings'] = {'timing': 'fast',
                          'colormode': 'rgb',
                          'sleeptimeout': '600',
                          'sensorsize': 'small'}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

window = tk.Tk(className='ScreenSync v0.3')
window.title("ScreenSync v0.3")
window.geometry("300x290")
window.iconbitmap(bitmap= str(application_path)+ '\icons\screensync.ico')
#print(str(application_path)+ '\icons\screensync.ico')
window.configure(bg='black', padx=20)

fpsText = StringVar()
ipAddress = StringVar()
selectedIP = StringVar()
selectedColor = StringVar()
selectedTiming = StringVar()
selectedSleep = StringVar()
selectedSensorSize = StringVar()
choices = []

screensize= ImageGrab.grab().size
screenX = screensize[0]
screenY = screensize[1]
screenCenter = [int(screenX/2),int(screenY/2)]

print (screenCenter)



def scan():
    global choices
    scanner = BulbScanner()
    scanner.scan(timeout=4)
    scanner_results = []

    for found_bulb in scanner.found_bulbs:
        print("Found a bulb: " + found_bulb['ipaddr'] + " with MAC: " + found_bulb['id'])
        scanner_results.append(found_bulb['ipaddr'])
    # Connect to the LED controller
    if len(scanner.found_bulbs) == 0:
        scanner_results.append("No controllers found :(")

    choices = scanner_results
    print(choices)

def scanbutton():
    global popupMenu
    global choices
    global selectedIP
    scan()
    menu = popupMenu["menu"]
    menu.delete(0, "end")
    for string in choices:
        menu.add_command(label=string,
                         command=lambda value=string: selectedIP.set(value))


timingChoices = ['slow', 'medium', 'fast', 'unlimited']



if config.has_section('settings') and config.has_option('settings','ip'):
    choices.append(config['settings']['ip'])
else:
    scan()


colorChoices = ['RGB', 'RBG', 'GRB', 'GBR', 'BRG', 'BGR']
sleepChoices = [60,300,600,1200,3600,99999]
sensorSizeChoices = ['tiny','small','medium', 'large', 'xlarge']
boundingbox = [ 910, 490, 1010, 590]



def calculateBoundingBox(sensorsize):
    if sensorsize == 'tiny':
        return [ screenCenter[0] - screenX*0.05, screenCenter[1] - screenY*0.05, screenCenter[0] + screenX*0.05, screenCenter[1] + screenY*0.05]
    if sensorsize == 'small':
        return [ screenCenter[0] - screenX*0.075, screenCenter[1] - screenY*0.075, screenCenter[0] + screenX*0.075, screenCenter[1] + screenY*0.075]
    if sensorsize == 'medium':
        return [ screenCenter[0] - screenX*0.15, screenCenter[1] - screenY*0.15, screenCenter[0] + screenX*0.15, screenCenter[1] + screenY*0.15]
    if sensorsize == 'large':
        return [ screenCenter[0] - screenX*0.33, screenCenter[1] - screenY*0.33, screenCenter[0] + screenX*0.33, screenCenter[1] + screenY*0.33]
    if sensorsize == 'xlarge':
        return [ screenCenter[0] - screenX*0.5, screenCenter[1] - screenY*0.5, screenCenter[0] + screenX*0.5, screenCenter[1] + screenY*0.5]

def startstop():
    myUpdateLED.shouldUpdate = not myUpdateLED.shouldUpdate
    fpsText.set("🙈")




def saveConfig(ip, timing, colormode, sleeptimeout, sensorsize):

    config['settings']['ip']= ip
    config['settings']['timing']= timing
    config['settings']['colormode']= colormode
    config['settings']['sleeptimeout']= sleeptimeout
    config['settings']['sensorsize'] = sensorsize

    with open('config.ini', 'w') as configfile:
        config.write(configfile)


window.rowconfigure(3, minsize=30)
window.columnconfigure(2, minsize=30)

fpslabel = tk.Label(text="FPS", fg='white', bg='black',font = "Helvetica 32 bold italic")
fpslabel.grid(column=0, row=1)
fps = tk.Label(text="Starting", textvariable=fpsText, fg='white', bg='black', font ="Helvetica 64 bold")
fps.grid(column=1, row=1)

startstopbutton = tk.Button(window, text ="Start / Stop", command = startstop)
startstopbutton.config(fg='white', bg='black')
startstopbutton.grid( column=1, row=7, pady=10)

scanbutton = tk.Button(window, text ="Scan", command = scanbutton)
scanbutton.config(fg='white', bg='black')
scanbutton.grid( column=0, row=7, pady=10)

timings = {"slow": 500,
           "medium": 200,
           "fast": 10,
           "unlimited": 1}





chooseip = tk.Label(text='Select IP: ', fg='white', bg='black',font = "Helvetica 12 bold italic")
chooseip.grid(column=0, row=2, sticky= 'E')
popupMenu = tk.OptionMenu(window, selectedIP, *choices)
selectedIP.set(choices[0])
popupMenu.config( fg='white', bg='black', highlightbackground='black', highlightcolor='black',highlightthickness=0, bd=0)
popupMenu.grid(column=1, row=2)

choose_color = tk.Label(text='Select Mode: ', fg='white', bg='black',font = "Helvetica 12 bold italic")
choose_color.grid(column=0, row=3, sticky= 'E')
colorMenu = tk.OptionMenu(window, selectedColor, *colorChoices)

selectedColor.set(config['settings']['colormode'])
colorMenu.config( fg='white', bg='black', highlightbackground='black', highlightcolor='black',highlightthickness=0, bd=0)
colorMenu.grid(column=1, row=3)

choose_timing = tk.Label(text='Select Timing: ', fg='white', bg='black',font = "Helvetica 12 bold italic")
choose_timing.grid(column=0, row=4, sticky= 'E')
timingMenu = tk.OptionMenu(window, selectedTiming, *timingChoices)

selectedTiming.set(config['settings']['timing'])
timingMenu.config( fg='white', bg='black', highlightbackground='black', highlightcolor='black',highlightthickness=0, bd=0)
timingMenu.grid(column=1, row=4)

choose_sleep = tk.Label(text='Choose Timeout: ', fg='white', bg='black',font = "Helvetica 12 bold italic")
choose_sleep.grid(column=0, row=5, sticky= 'E')
sleepMenu = tk.OptionMenu(window, selectedSleep, *sleepChoices)

selectedSleep.set(config['settings']['sleeptimeout'])
sleepMenu.config( fg='white', bg='black', highlightbackground='black', highlightcolor='black',highlightthickness=0, bd=0)
sleepMenu.grid(column=1, row=5)

choose_sensorsize = tk.Label(text='Sensor size: ', fg='white', bg='black',font = "Helvetica 12 bold italic")
choose_sensorsize.grid(column=0, row=6, sticky= 'E')
sensorsizeMenu = tk.OptionMenu(window, selectedSensorSize, *sensorSizeChoices)

selectedSensorSize.set(config['settings']['sensorsize'])
sensorsizeMenu.config( fg='white', bg='black', highlightbackground='black', highlightcolor='black',highlightthickness=0, bd=0)
sensorsizeMenu.grid(column=1, row=6)


def connectLED(ip):
    try:
        #led_to_connect = scanner.getBulbInfoByID(args.led_mac)
        #bulb = WifiLedBulb(led_to_connect['ipaddr'])
        bulb = WifiLedBulb(ip)
        print("Connected to LED strip with IP: " + ip)
        ipAddress.set("IP: "+ ip)
    except:
        print("No valid MAC address provided, attempting to use first one discovered: " + scanner.found_bulbs[0]['id'])
        print("Unable to connect to " + ip)
        #first_discovered_bulb = scanner.getBulbInfoByID(scanner.found_bulbs[0]['id'])
        #bulb = WifiLedBulb(first_discovered_bulb['ipaddr'])
    return bulb


#def saveConfig(ip, timing, color, sleep):

def change_selected_ip(*args):
    # print( selectedIP.get() )
    global bulb
    bulb = connectLED(selectedIP.get())
    ipAddress.set(selectedIP.get())
    saveConfig(selectedIP.get(),selectedTiming.get().lower(), selectedColor.get().lower(), str(mySleepTimer.seconds_to_wait ), selectedSensorSize.get())

def change_selected_color(*args):
    global selectedColor
    global myUpdateLED
    # print (myUpdateLED.colorMode)
    myUpdateLED.colorMode = selectedColor.get().lower()
    # print (myUpdateLED.colorMode)
    saveConfig(selectedIP.get(),selectedTiming.get().lower(), selectedColor.get().lower(), str(mySleepTimer.seconds_to_wait ), selectedSensorSize.get())


def change_selected_timing(*args):
    global selectedTiming
    global myUpdateLED
    # print (myUpdateLED.updateFrequency)
    myUpdateLED.updateFrequency = selectedTiming.get().lower()
    # print (myUpdateLED.updateFrequency)
    saveConfig(selectedIP.get(),selectedTiming.get().lower(), selectedColor.get().lower(), str(mySleepTimer.seconds_to_wait ), selectedSensorSize.get())


def change_selected_sleep(*args):
    global selectedSleep
    global mySleepTimer
    #print (mySleepTimer.seconds_to_wait)
    mySleepTimer.seconds_to_wait = int(selectedSleep.get())
    #print (mySleepTimer.seconds_to_wait)
    saveConfig(selectedIP.get(),selectedTiming.get().lower(), selectedColor.get().lower(), str(mySleepTimer.seconds_to_wait ), selectedSensorSize.get())

def change_selected_sensorsize(*args):
    global selectedSensorSize
    global mySensorSize
    global boundingbox
    boundingbox = calculateBoundingBox(selectedSensorSize.get())
    saveConfig(selectedIP.get(),selectedTiming.get().lower(), selectedColor.get().lower(), str(mySleepTimer.seconds_to_wait ), selectedSensorSize.get())




# link function to change dropdown
selectedIP.trace('w', change_selected_ip)
selectedColor.trace('w', change_selected_color)
selectedTiming.trace('w', change_selected_timing)
selectedSleep.trace('w', change_selected_sleep)
selectedSensorSize.trace('w', change_selected_sensorsize)
# print(str(selectedIP.get()))
bulb = connectLED(str(selectedIP.get()))




class FPS:
    ticks = 0
    last_run = 0

    def calc_fps(self):
        millis = int(round(time.time() * 1000))
        if millis - self.last_run > 1000:
            #print("FPS: " + str(self.ticks))
            fpsText.set( str(self.ticks))
            self.last_run = millis
            self.ticks = 0




class SleepTimer:
    same_color = 0
    last_r = 0
    last_b = 0
    last_g = 0
    seconds_to_wait = 300
    millis_to_wait = seconds_to_wait * 1000


    def __init__(self, data):
        self.seconds_to_wait = data

    def check_if_sleeping(self, r, g, b):
        if self.last_r == r and self.last_g == g and self.last_b == b:
            if int(round(time.time() * 1000)) - self.same_color > int(self.seconds_to_wait*1000):
                return True
            return False
        else:
            self.same_color = int(round(time.time() * 1000))
            self.last_r = r
            self.last_b = b
            self.last_g = g
            return False



myFPS = FPS()


class UpdateLED:

    shouldUpdate = True
    colorMode = "rgb"
    updateFrequency = 2
    sleepTimer = 600

    def update(self, tkinterObj):

        if self.shouldUpdate:

            image = ImageGrab.grab(calculateBoundingBox(selectedSensorSize.get()))
            #dominant_color = get_dominant_color(image)
            converter = ImageEnhance.Color(image)
            image2 = converter.enhance(3)

            image_stats = ImageStat.Stat(image2)
            myFPS.ticks = myFPS.ticks + 1
            myFPS.calc_fps()

            if mySleepTimer.check_if_sleeping(image_stats.median[0], image_stats.median[2], image_stats.median[1]):
            #if mySleepTimer.check_if_sleeping(dominant_color[0], dominant_color[2], dominant_color[1]):
                try:
                    bulb.setRgb(0, 0, 0, persist=False)
                except:
                    print("Oops looks like we couldn't connected to the LED strip")
            else:
                if self.colorMode == "rgb":
                    try:
                        bulb.setRgb(image_stats.median[0], image_stats.median[1], image_stats.median[2], persist=False)
                        #bulb.setRgb(dominant_color[0], dominant_color[1], dominant_color[2], persist=False)
                    except:
                        print("Oops looks like we couldn't connected to the LED strip")
                elif self.colorMode == "rbg":
                    try:
                        bulb.setRgb(image_stats.median[0], image_stats.median[2], image_stats.median[1], persist=False)
                       #bulb.setRgb(dominant_color[0], dominant_color[2], dominant_color[1], persist=False)
                    except:
                        print("Oops looks like we couldn't connected to the LED strip")
                elif self.colorMode == "grb":
                    try:
                        bulb.setRgb(image_stats.median[1], image_stats.median[0], image_stats.median[2], persist=False)
                        #bulb.setRgb(dominant_color[1], dominant_color[0], dominant_color[2], persist=False)
                    except:
                        print("Oops looks like we couldn't connected to the LED strip")
                elif self.colorMode == "gbr":
                    try:
                        bulb.setRgb(image_stats.median[1], image_stats.median[2], image_stats.median[0], persist=False)
                        #bulb.setRgb(dominant_color[1], dominant_color[2], dominant_color[0], persist=False)
                    except:
                        print("Oops looks like we couldn't connected to the LED strip")
                elif self.colorMode == "brg":
                    try:
                        bulb.setRgb(image_stats.median[2], image_stats.median[0], image_stats.median[1], persist=False)
                        #bulb.setRgb(dominant_color[2], dominant_color[0], dominant_color[1], persist=False)
                    except:
                        print("Oops looks like we couldn't connected to the LED strip")
                elif self.colorMode == "bgr":
                    try:
                        bulb.setRgb(image_stats.median[2], image_stats.median[1], image_stats.median[0], persist=False)
                        #bulb.setRgb(dominant_color[2], dominant_color[1], dominant_color[0], persist=False)
                    except:
                        print("Oops looks like we couldn't connected to the LED strip")
                else:
                    print("uh oh")
        tkinterObj.after(timings[self.updateFrequency], lambda: myUpdateLED.update(tkinterObj))


myUpdateLED = UpdateLED()
myUpdateLED.colorMode = selectedColor.get().lower()
myUpdateLED.updateFrequency = selectedTiming.get().lower()
myUpdateLED.sleepTimer = selectedSleep.get()


mySleepTimer = SleepTimer(int(selectedSleep.get()))

# Need to kick off the LED update once so it can run and request an 'after' from tkinter

myUpdateLED.update(window)

# Enter into tkinter main loop

saveConfig(selectedIP.get(),selectedTiming.get().lower(), selectedColor.get().lower(), str(mySleepTimer.seconds_to_wait ), selectedSensorSize.get())


window.mainloop()

#RGB, RBG, GRB, GBR, BRG, BGR
