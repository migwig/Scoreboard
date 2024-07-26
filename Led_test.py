import time
from rpi_ws281x import *
import argparse
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World"




app.run(host="0.0.0.0")



# LED strip configuration:
LED_COUNT      = 168   # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating a signal (try 10)
LED_BRIGHTNESS = 65      # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
SEG_LEN        = 6
SEG_COUNT      = 7
DIG_QUAN       = 4

seconds = 120

#define segments
A = (SEG_LEN*2) , (SEG_LEN*3)
B = SEG_LEN , (SEG_LEN*2)
C = (SEG_LEN*6) , (SEG_LEN*7)
D = (SEG_LEN*5) , (SEG_LEN*6)
E = (SEG_LEN*4) , (SEG_LEN*5)
F = (SEG_LEN*3) , (SEG_LEN*4)
G = 0, SEG_LEN

#define digits
array = [
        [A,B,C,D,E,F],
        [B,C],
        [A,B,D,E,G],
        [A,B,C,D,G],
        [B,C,F,G],
        [A,C,D,F,G],
        [A,C,D,E,F,G],
        [A,B,C],
        [A,B,C,D,E,F,G],
        [A,B,C,F,G]
        ]


def displayDigit(strip, digit, color):
    for i in range(len(array[digit])):
        temp = array[digit][i]
        for x in range(temp[0], temp[1]):
            strip.setPixelColor(x, color)
    strip.show()

def displaySecondDigit(strip, digit, color):
    for i in range (len(array[digit])):
        temp = array[digit][i]
        for x in range(int(temp[0]),int(temp[1])):
            strip.setPixelColor(x + (SEG_LEN*SEG_COUNT), color)
    strip.show()

def displayThirdDigit(strip, digit, color):
    for i in range (len(array[digit])):
        temp = array[digit][i]
        for x in range(int(temp[0]),int(temp[1])):
            strip.setPixelColor(x + ((SEG_LEN*SEG_COUNT)*2), color)
    strip.show()
    
def displayFourthDigit(strip, digit, color):
    for i in range (len(array[digit])):
        temp = array[digit][i]
        for x in range(int(temp[0]),int(temp[1])):
            strip.setPixelColor(x + ((SEG_LEN*SEG_COUNT)*3), color)
    strip.show()

def displaySegment(strip, segrange, color, wait_ms=50):
    for i in range(int(segrange[0]), int(segrange[1])):
        strip.setPixelColor(i, color)
    strip.show()


# Define functions which animate LEDs in various ways.
def displayRange(strip, segstart, color, wait_ms=50):
    for i in range(SEG_LEN):
        strip.setPixelColor(segstart + i, color)
    strip.show()
    
def clearStrip(strip):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, 0)
    strip.show()
    
def countTest(strip):
    for i in range(10):
        clearStrip(strip, 0)
        displayDigit(strip, i, Color(0,0,255))
        displaySecondDigit(strip, i, Color(255,0,0))
        time.sleep(1)
        
def countdown(strip, seconds):
    while seconds > 0:
        mins, secs = divmod(seconds, 60)  # Convert seconds to minutes and seconds
        hours, mins = divmod(mins, 60)  # Convert minutes to hours and minutes
        toDisplay = '{:02d}{:02d}'.format(mins, secs)
        print(toDisplay)
        clearStrip(strip)
        displayDigit(strip, int(str(toDisplay)[0:1]), Color(0,0,125))
        displaySecondDigit(strip, int(str(toDisplay)[1:2]), Color(0,0,125))
        displayThirdDigit(strip, int(str(toDisplay)[2:3]), Color(0,0,125))
        displayFourthDigit(strip, int(str(toDisplay)[3:4]), Color(0,0,125))
        time.sleep(1)  # Wait for 1 second
        seconds -= 1  # Decrease seconds by 1
    print("The timeout has elapsed!")  # Countdown finished message

    
# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:

        while True:
            clearStrip(strip)
            time.sleep(5)
            countdown(strip, seconds)
            
            
            #countTest(strip)
           # mins = 15
          #  while(seconds > 0):         
           ##     clearStrip(strip,0)
             #   if seconds >= 10:
              #      displayDigit(strip, int(str(seconds)[:1]), Color(0,0,125))
              #      displaySecondDigit(strip, int(str(seconds)[1:]), Color(0,0,125))
              #  else:
              #      displaySecondDigit(strip, seconds, Color(0,0,125))
              #  time.sleep(1)
               # seconds -= 1           
                    
            
        

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0,0,0), 10)

