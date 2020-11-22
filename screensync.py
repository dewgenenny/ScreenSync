from PIL import ImageGrab
from PIL import ImageStat
from flux_led import WifiLedBulb, BulbScanner
import argparse
import time

parser = argparse.ArgumentParser()
led_mac = "unset"

parser.add_argument("--led_mac", help="LED strip MAC address formatted without delimiters eg 63039F06BE28 ", required=False)
parser.add_argument("--timing", help="Timing mode: slow, medium, fast, unlimited", required=False)
args = parser.parse_args()

# get timing mode // it's simply how many millis to wait per loop. Has an effect on CPU usage

timings = {"slow": 500,
           "medium": 200,
           "fast": 50,
           "unlimited": 1}

requested_timing = args.timing

if requested_timing is None:
    requested_timing = 'fast'

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
    print("No MAC address provided, attempting to use first one discovered: " + scanner.found_bulbs[0]['id'])
    first_discovered_bulb = scanner.getBulbInfoByID(scanner.found_bulbs[0]['id'])
    bulb = WifiLedBulb(first_discovered_bulb['ipaddr'])

while 1:

    image = ImageGrab.grab(bbox=(960, 490, 1060, 590))
    image_stats = ImageStat.Stat(image)
    try:
        bulb.setRgb(image_stats.median[0], image_stats.median[1], image_stats.median[2], persist=False)
    except:
        print("Oops looks like we couldn't connected to the LED strip")

    # Wait for a few millis determined by --timing setting to save on CPU // network
    time.sleep(timings[requested_timing] / 1000)
