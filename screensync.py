from PIL import ImageGrab
from PIL import ImageStat
from PIL import ImageEnhance
from flux_led import WifiLedBulb, BulbScanner
import argparse
import time

parser = argparse.ArgumentParser()
led_mac = "unset"

# set some defaults in case they're not set on command line
default_seconds_before_sleep = 300
default_timing = 'fast'

# parse command line arguments

parser.add_argument("--led_mac", help="LED strip MAC address formatted without delimiters eg 63039F06BE28 ",
                    required=False)
parser.add_argument("--timing", help="Timing mode", choices=['slow', 'medium', 'fast', 'unlimited'], required=False)
parser.add_argument("--sleep", help="Amount of seconds to wait before considered 'asleep'", required=False)
parser.add_argument("--colors", help="Order of LEDs", choices=['RGB', 'RBG', 'GRB', 'GBR', 'BRG', 'BGR'], required=False, default="RGB")
parser.add_argument("--debug", help="true or false", choices=['true', 'false'], required=False)

args = parser.parse_args()

# get timing mode // it's simply how many millis to wait per loop. Has an effect on CPU usage

timings = {"slow": 500,
           "medium": 200,
           "fast": 50,
           "unlimited": 1}

seconds_to_wait_before_sleep = args.sleep

if args.colors is not None:
    requested_colors = args.colors.lower()

if args.timing is not None:
    requested_timing = args.timing.lower()
else:
    requested_timing = None

if args.debug is not None:
    debug_requested = args.debug.lower()
else:
    debug_requested = None

if requested_timing is None:
    requested_timing = default_timing

elif not requested_timing in timings.keys():
    requested_timing = default_timing
    print("Requested timing mode not found, defaulting to: " + requested_timing)

if seconds_to_wait_before_sleep is None:
    seconds_to_wait_before_sleep = default_seconds_before_sleep
    print("Sleep timer not defined, defaulting to " + str(seconds_to_wait_before_sleep))

elif not seconds_to_wait_before_sleep.isnumeric:
    seconds_to_wait_before_sleep = default_seconds_before_sleep
    print("Sleep timer not defined properly, defaulting to " + str(seconds_to_wait_before_sleep))

if debug_requested is None:
    DEBUG = False
elif debug_requested == 'false':
    DEBUG = False
elif debug_requested == 'true':
    DEBUG = True
    print("Turning debug on....")
else:
    DEBUG = False

print("Sleep timeout set to " + str(seconds_to_wait_before_sleep) + " seconds")
print("Starting with timing mode: " + requested_timing)

# scan for the LED controllers

scanner = BulbScanner()
scanner.scan(timeout=4)

for found_bulb in scanner.found_bulbs:
    print("Found a bulb: " + found_bulb['ipaddr'] + " with MAC: " + found_bulb['id'])

# Connect to the LED controller

try:
    led_to_connect = scanner.getBulbInfoByID(args.led_mac)
    bulb = WifiLedBulb(led_to_connect['ipaddr'])
    print("Connected to LED strip MAC: " + args.led_mac + " with IP: " + led_to_connect['ipaddr'])
except:
    print("No valid MAC address provided, attempting to use first one discovered: " + scanner.found_bulbs[0]['id'])
    first_discovered_bulb = scanner.getBulbInfoByID(scanner.found_bulbs[0]['id'])
    bulb = WifiLedBulb(first_discovered_bulb['ipaddr'])


class FPS:
    ticks = 0
    last_run = 0

    def print_fps(self):
        millis = int(round(time.time() * 1000))
        if millis - self.last_run > 1000:
            print("FPS: " + str(self.ticks))
            self.last_run = millis
            self.ticks = 0


class SleepTimer:
    same_color = 0
    last_r = 0
    last_b = 0
    last_g = 0
    millis_to_wait = 1000

    def __init__(self, data):
        self.millis_to_wait = data

    def check_if_sleeping(self, r, g, b):

        if self.last_r == r and self.last_g == g and self.last_b == b:
            if int(round(time.time() * 1000)) - self.same_color > int(self.millis_to_wait):
                return True
            return False
        else:
            self.same_color = int(round(time.time() * 1000))
            self.last_r = r
            self.last_b = b
            self.last_g = g
            return False


myFPS = FPS()
mySleepTimer = SleepTimer(int(seconds_to_wait_before_sleep) * int(1000))

while 1:

    image = ImageGrab.grab(bbox=(910, 490, 1010, 590))
    converter = ImageEnhance.Color(image)
    image2 = converter.enhance(3)

    image_stats = ImageStat.Stat(image2)

    if DEBUG:
        myFPS.ticks = myFPS.ticks + 1
        myFPS.print_fps()

    if mySleepTimer.check_if_sleeping(image_stats.median[0], image_stats.median[2], image_stats.median[1]):
        try:
            bulb.setRgb(0, 0, 0, persist=False)
        except:
            print("Oops looks like we couldn't connected to the LED strip")
    else:
        if requested_colors == "rgb":
            try:
                bulb.setRgb(image_stats.median[0], image_stats.median[1], image_stats.median[2], persist=False)
            except:
                print("Oops looks like we couldn't connected to the LED strip")
        elif requested_colors == "rbg":
            try:
                bulb.setRgb(image_stats.median[0], image_stats.median[2], image_stats.median[1], persist=False)
            except:
                print("Oops looks like we couldn't connected to the LED strip")
        elif requested_colors == "grb":
            try:
                bulb.setRgb(image_stats.median[1], image_stats.median[0], image_stats.median[2], persist=False)
            except:
                print("Oops looks like we couldn't connected to the LED strip")
        elif requested_colors == "gbr":
            try:
                bulb.setRgb(image_stats.median[1], image_stats.median[2], image_stats.median[0], persist=False)
            except:
                print("Oops looks like we couldn't connected to the LED strip")
        elif requested_colors == "brg":
            try:
                bulb.setRgb(image_stats.median[2], image_stats.median[0], image_stats.median[1], persist=False)
            except:
                print("Oops looks like we couldn't connected to the LED strip")
        elif requested_colors == "bgr":
            try:
                bulb.setRgb(image_stats.median[2], image_stats.median[1], image_stats.median[0], persist=False)
            except:
                print("Oops looks like we couldn't connected to the LED strip")

    time.sleep(timings[requested_timing] / 1000)

#RGB, RBG, GRB, GBR, BRG, BGR
