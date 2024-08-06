from rpi_ws281x import *
import time
from datetime import datetime
import board
import adafruit_dht

sensor = adafruit_dht.DHT11(board.D4)

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

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)

strip.begin()



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

degree = [A,B,G,F]
C_Letter = [A,D,E,F]

def displayCurrentTime(strip):
	now = datetime.now()
	hours = now.hour
	minutes = now.minute
	total_seconds = hours * 3600 + minutes * 60
	displayTimeRemaining(strip, int(total_seconds))


def displayDigit(strip, digit, color):
    for i in range(len(array[digit])):
        temp = array[digit][i]
        for x in range(temp[0], temp[1]):
            strip.setPixelColor(x, color)


def displaySecondDigit(strip, digit, color):
    for i in range (len(array[digit])):
        temp = array[digit][i]
        for x in range(int(temp[0]),int(temp[1])):
            strip.setPixelColor(x + (SEG_LEN*SEG_COUNT), color)


def displayThirdDigit(strip, digit, color):
    for i in range (len(array[digit])):
        temp = array[digit][i]
        for x in range(int(temp[0]),int(temp[1])):
            strip.setPixelColor(x + ((SEG_LEN*SEG_COUNT)*2), color)

    
def displayFourthDigit(strip, digit, color):
    for i in range (len(array[digit])):
        temp = array[digit][i]
        for x in range(int(temp[0]),int(temp[1])):
            strip.setPixelColor(x + ((SEG_LEN*SEG_COUNT)*3), color)
			
def displaySegment(strip, segment, display, color):
	for i in range(len(display)):
		temp = display[i]
		for x in range(temp[0],temp[1]):
			strip.setPixelColor(x + ((SEG_LEN*SEG_COUNT)*(segment-1)), color)
		
def clearStrip(strip):
    strip.begin()
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, 0)
    strip.show()
             

def displayTimeRemaining(strip, timeRemaining):
    mins, secs = divmod(timeRemaining, 60)
    hours, mins = divmod(mins, 60)
    toDisplay = '{:02d}{:02d}'.format(mins, secs)
    clearStrip(strip)
    displayDigit(strip, int(str(toDisplay)[0:1]), Color(0,0,125))
    displaySecondDigit(strip, int(str(toDisplay)[1:2]), Color(0,0,125))
    displayThirdDigit(strip, int(str(toDisplay)[2:3]), Color(0,0,125))
    displayFourthDigit(strip, int(str(toDisplay)[3:4]), Color(0,0,125))
    strip.show()

def displayTemperature():
	strip.begin()
	temp = '{:02d}'.format(sensor.temperature)
	humidity = sensor.humidity
	clearStrip(strip)
	displayDigit(strip, int(str(temp)[0:1]), Color(125,0,0))
	displaySecondDigit(strip, int(str(temp)[1:2]), Color(125,0,0))
	displaySegment(strip, 3, degree, Color(125,0,0))
	displaySegment(strip, 4, C_Letter, Color(125,0,0))
	strip.show()