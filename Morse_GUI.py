from tkinter import *
import tkinter.font
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

##We will define morse code using GPIO functions
def dot():

    time.sleep(0.5)
    GPIO.output(17, True)
    time.sleep(0.5)
    GPIO.output(17, False)

def dash():
    time.sleep(0.5)
    GPIO.output(17, True)
    time.sleep(1.5)
    GPIO.output(17, False)

def charbreak():
    time.sleep(1.0)

def wordbreak():
    time.sleep(3.0)

##Morse dictionary
MORSE_CODE_DICT = { 'A':'.-', 'B':'-...',

                    'C':'-.-.', 'D':'-..', 'E':'.',

                    'F':'..-.', 'G':'--.', 'H':'....',

                    'I':'..', 'J':'.---', 'K':'-.-',

                    'L':'.-..', 'M':'--', 'N':'-.',

                    'O':'---', 'P':'.--.', 'Q':'--.-',

                    'R':'.-.', 'S':'...', 'T':'-',

                    'U':'..-', 'V':'...-', 'W':'.--',

                    'X':'-..-', 'Y':'-.--', 'Z':'--..',

                    '1':'.----', '2':'..---', '3':'...--',

                    '4':'....-', '5':'.....', '6':'-....',

                    '7':'--...', '8':'---..', '9':'----.',

                    '0':'-----', ', ':'--..--', '.':'.-.-.-',

                    '?':'..--..', '/':'-..-.', '-':'-....-',

                    '(':'-.--.', ')':'-.--.-'}


MORSE_TO_GPIO_DICT= {'.': 'dot(), ', '-': 'dash(), ', ' ': 'charbreak(), '}

##encrypting user text
def encrypt(message):
    cipher = ''
    for letter in message:
        if letter != ' ':
            # Looks up the dictionary and adds the
            # corresponding morse code
            # along with a space to separate
            # morse codes for different characters
            cipher += MORSE_CODE_DICT[letter] + ' '
        else:
            # 1 space indicates different characters
            # and 2 indicates different words
            cipher += ' '
    return cipher

def morseBlink(cipher):
    morse = ''
    for symbol in cipher:
        ##Here we match the dot or dash to the corresponding function, as a long string.
        morse += MORSE_TO_GPIO_DICT[symbol]
    ## To avoid using heaps of code to read double spaces, we can just replace double charbreaks with a wordbreak
    morse = morse.replace(' charbreak(), charbreak(),', ' wordbreak(),')
    ##We need to evaluate the string as a list of functions
    eval(morse)
    return morse

#GUI DEF
win = Tk()
win.title("Text To Morse")
myFont = tkinter.font.Font(family = 'Helvetica', size = 12, weight = "bold")

##Button Functions
def close(window):
    window.destroy()
    GPIO.cleanup()
    print("closewindow")

def convertAndBlink():
    global textInput
    userText = textInput.get()
    print(userText)

    ## we store our encrypted text in uppercase for the dictionary.
    textAsMorse = encrypt(userText.upper())
    print(textAsMorse)
    morseToBlink = morseBlink(textAsMorse)
    print(morseToBlink)

## WIDGETS ##
    ##Text input
textInput = Entry(win, width=50)
textInput.pack()

    ##This assigns the keyboard to the text box once the program is launched.
textInput.focus_set()
  
sendButton = Button(win, text = 'Send', font = myFont, command = convertAndBlink, bg = 'white', height = 1, width = 24)
sendButton.pack(side= 'top')
closeButton = Button(win, text = 'Close', font = myFont, command = lambda: close(win), bg = 'white', height = 1, width = 24)
closeButton.pack(side = 'bottom')

# All codes thanks to github