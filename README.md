### Screen Sync is a python based utility to synchronise screen color with 'Magic Home' LED controllers.

It's a very, very early go at using the awesome flux_led library (https://github.com/beville/flux_led) to create a kind of cheap and cheerful 'philips hue light sync' experience.

So far I'm just using the "ImageGrab" and "ImageStat" modules from Pillow to generate a median color from the screen. It is working quite well, but no doubt it could be more performant with additional work. 

You can find an automated standalone build for windows that was generated using pyinstaller under the 'dist' folder. Otherwise, you'll need to install the necessary dependencies - flux_led and Pillow 

##### Installation

flux_led installation:

`python3 -m pip install --upgrade Pillow`

Pillow installation:

`python3 -m pip install --upgrade flux_led` 

##### Running

You can run the utility without needing to provide any arguments. It will then go out and scan for 'magic home' / flux_led compatible controllers and connect to the first one it finds.

If you'd like, you can provide a specific MAC address to connect to:

`python3 screensync.py --led_mac 63039F06BE28`

Additionally, you can provide a timing setting - this impacts how often the screen is polled / LED strip updated. You can choose from 'slow', 'medium', 'fast' and 'unlimited'. For the unlimited setting, there is no delay within the polling loop. Be careful as this can increase CPU usage quite a bit.

`python3 screensync.py --led_mac 63039F06BE28 --timing fast`

Here's a video of it in action - https://youtu.be/0lskW9P4WpQ

