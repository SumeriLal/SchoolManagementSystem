import serial     #import serial moduleimport serial
import time
import json
import pyrebase
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

#Firebase connection
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

# Opening JSON file 
with open('/home/pi/sample.json', 'r') as openfile:
    # Reading from json file 
    json_object = json.load(openfile)
#print(json_object)

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0
# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
# Initialize library.
disp.begin()
# Clear display.
#disp.clear()
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

#Serial port configuration
ser = serial.Serial ("/dev/ttyS0", baudrate=9600, timeout=0.01)      #Open named port

#Buzzer and LED pin configuration
buzzer = 23
ledR = 17
ledG = 27
ledB = 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer,GPIO.OUT)
GPIO.setup(ledR,GPIO.OUT)
GPIO.setup(ledG,GPIO.OUT)
GPIO.setup(ledB,GPIO.OUT)
#Default led
GPIO.output(ledB,1)


while True:
   data = ser.readline()                     #Read ten characters from serial port to dat
   cardID = data
   if len(cardID) > 10:
      #print("Card Detected:", (cardID))
      name = "Blue Heart Lab"
      try:
         z = str(cardID)
         y = json_object[z]
         n = y['rollno']
         text = y['name']
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
         time.sleep(0.2)
         disp.clear()
         
         #Beep Indication
         GPIO.output(buzzer,1)
         GPIO.output(ledG,1)
         time.sleep(0.1)
         GPIO.output(buzzer,0)
         GPIO.output(ledG,0)
         time.sleep(0.05)
         GPIO.output(buzzer,1)
         GPIO.output(ledG,1)
         time.sleep(0.1)
         GPIO.output(buzzer,0)
         GPIO.output(ledG,0)
         time.sleep(0.05)
         #Database
         data = y
         database.child("users").child(name).child(z).update(data)
      except KeyError:
         n = 'Error !'
         text = 'Invalid Card'
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
         time.sleep(0.5)
         disp.clear()
         #Beep Indication
         for i in range(4):
            GPIO.output(buzzer,1)
            GPIO.output(ledR,1)
            time.sleep(0.4)
            GPIO.output(buzzer,0)
            GPIO.output(ledR,0)
            time.sleep(0.02)
      

