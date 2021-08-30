import time
import pyrebase
config = {
    'apiKey': "4IChB1Zhg9FUFAkDLUvioeTgr0Q4A3jqXzdc9GyM",
    'authDomain': "sid-cards.firebaseapp.com",
    'databaseURL': "https://sid-cards-default-rtdb.firebaseio.com",
    'projectId': "sid-cards",
    'storageBucket': "sid-cards.appspot.com",
}
firebase = pyrebase.initialize_app(config)
auth1 = firebase.auth()
database = firebase.database()

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import subprocess

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# 128x32 display with hardware I2C:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font.
font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype('Montserrat-Light.ttf', 13)
font2 = ImageFont.truetype('fontawesome-webfont.ttf', 14)
font_icon_big = ImageFont.truetype('fontawesome-webfont.ttf', 20)
font_text_big = ImageFont.truetype('Montserrat-Medium.ttf', 19)

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

while True:
    id, text = reader.read()
    name = "Blue Heart Lab"
    z = str(id)
    n = int(z[:6])

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    # Icons
    draw.text((x+105, top+15), chr(61528),  font=font_icon_big, fill=255)
    #Text
    draw.text((12, top),    str(name),  font=font, fill=255)
    draw.text((x, top+15),  "ID: "+str(n),  font=font_text_big, fill=255)
    draw.text((x, top+40),  str(text), font=font_text_big, fill=255)
    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(1)
    disp.clear()
    #Database
    data = {"name":text}
    database.child("users").child(name).child(id).update(data)
