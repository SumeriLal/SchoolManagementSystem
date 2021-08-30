import serial                          #import serial module

ser = serial.Serial ("/dev/ttyS0", baudrate=9600, timeout=0.01)

while True:
   #Open named port 
   data = ser.readline()         #Close port
   
   data = slice(2, -1)
   cardID = data
   if len(cardID) > 10:
      print("Card Detected:", cardID)
