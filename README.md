### Screen Sync is a python based utility to synchronise screen color with 'Magic Home' LED controllers.

It's a very early go at using the awesome flux_led library (https://github.com/beville/flux_led) to create a kind of cheap and cheerful 'philips hue light sync' experience.

So far I'm just using the "ImageGrab" and "ImageStat" modules from Pillow to generate a median color from the screen. It is working quite well, but no doubt it could be more performant with additional work. 

You can find an automated standalone build for windows that was generated using pyinstaller under the 'dist' folder. Otherwise, you'll need to install the necessary dependencies - flux_led and Pillow 

##### Installation

flux_led installation:

`python3 -m pip install --upgrade Pillow`

Pillow installation:

`python3 -m pip install --upgrade flux_led` 

##### Running

`usage: screensync.py [-h] [--led_mac LED_MAC] [--timing TIMING]
                      [--sleep SLEEP] [--debug DEBUG]`
 
 optional arguments:
 
   -h, --help         (show the help message and exit)
   
   --led_mac LED_MAC  (LED strip MAC address formatted without delimiters eg 63039F06BE28)
                      
   --timing TIMING    (Timing mode: slow, medium, fast, unlimited)
   
   --sleep SLEEP      (Amount of seconds to wait before considered 'asleep')
   
   --debug DEBUG      (true or false - will print FPS to CLI each second)
   

You can run the utility without needing to provide any arguments. It will then go out and scan for 'magic home' / flux_led compatible controllers and connect to the first one it finds.

Full example running with all options:

`python3 screensync.py --led_mac 60049F06BA48 --timing unlimited --sleep 300 --debug true`

Here's a video of it in action - https://youtu.be/izCWz9-xkw4

