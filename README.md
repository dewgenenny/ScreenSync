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

`usage: screensync.py`   

All options can now be chosen in the GUI :)

Here's a video of it in action - https://youtu.be/izCWz9-xkw4

