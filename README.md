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

__Update July 2022__ - now added the option to choose the 'sensor size' in the GUI. This allows you to select the size of the bounding box where the image of the screen is sampled. Tiny and small are good for using with FPS games (this is my use case), large and xlarge probably better for watching videos or similar...

Here's a video of it in action - https://youtu.be/izCWz9-xkw4

