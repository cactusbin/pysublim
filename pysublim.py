import pyosd
import argparse
import ConfigParser
import subprocess
import os
import random

def displaySublim(string, delay):
    import random
    import time

    global osd

    osd.set_vertical_offset(random.randint(0, (screenHeight - 50)))
    osd.set_horizontal_offset(random.randint(0, (screenWidth - 50)))
    osd.show()
    osd.display(string)
    time.sleep(delay)
    osd.hide()

def isLink(string):
    import re

    #Check if its a URL
    if re.compile('((?:http|https)(?::\\/{2}[\\w]+)(?:[\\/|\\.]?)(?:[^\\s"]*))', re.IGNORECASE | re.DOTALL).search(string):
        return 1

    #Check for numbers brackets (lynx)
    if re.compile('(\\[)(\\d+)(\\])',re.IGNORECASE|re.DOTALL).search(string):
        return 1

    return 0

def getWord(string):
    for line in string:
        for word in line.split(" "):
            if not word == "" and (not args.striplinks or not isLink(word)):
                yield word

def getToParse():
    if args.execute:
        toParse = subprocess.Popen(args.File.split(), stdout=subprocess.PIPE).stdout
    elif args.directory or args.directoryrandom:
        if not files:
            if not args.loop:
                exit
            files = os.listdir(args.File)

        if args.directoryrandom:
            file = open(args.File + "/" + files.pop(random.randrange(0, len(files))), "r")
        else:
            file = open(args.File + "/" + files.pop(), "r")
        toParse = file
    else:
        toParse = open(args.File, "r")

    if args.executefile:
        command = file.readline().rstrip("\n").split()

        if len(command) == 0:
            if not args.loop:
                exit
            file.seek(0)
            command = file.readline().rstrip("\n").split()

        toParse = subprocess.Popen(command, stdout=subprocess.PIPE).stdout

    return toParse

osd = pyosd.osd()

configparser = ConfigParser.ConfigParser()
configparser.readfp(open("pysublim.cfg"))

argparser = argparse.ArgumentParser(description = "Python script to display subliminal messages")
argparser.add_argument("File")
argparser.add_argument("-c", "--color", help = "Font color (default: black)", default = "black")
argparser.add_argument("-s", "--size", help = "Font size (default: 25)", default = "25")
argparser.add_argument("-t", "--time", type = float, help = "Time in seconds the message will be displayed (deafult: .05)", default = .05)
argparser.add_argument("-l", "--loop", help = "Use this option if you wish to loop subliminals until killed", action = "store_true")
argparser.add_argument("-e", "--execute", help = "Use if you want to execute a command instead of reading from a file", action = "store_true")
argparser.add_argument("-ef", "--executefile", help = "Use if you want to execute a list of commands from a file. Can be used with --directory and --directoryrandom.", action = "store_true")
argparser.add_argument("-d", "--directory", help = "Use to display all files in a directory", action = "store_true")
argparser.add_argument("-dr", "--directoryrandom", help = "Use to display all files in a directory in random order", action = "store_true")
argparser.add_argument("-sl", "--striplinks", help = "Use to strip links and urls from input when using 'lynx -dump'", action = "store_true")

args = argparser.parse_args()

osd.set_colour(args.color)
osd.set_font("-*-*-*-*-*-*-" + args.size + "-*-*-*-*-*-*-*")

screenWidth = configparser.getint("screen", "width")
screenHeight = configparser.getint("screen", "height")

if args.execute and args.executefile:
    print "Conflicting options 'execute' and 'executefile'"
    exit()

if args.executefile and not (args.directory or args.directoryrandom):
    file = open(args.File, "r")

if args.directory or args.directoryrandom:
    files = os.listdir(args.File)

while True:
    toParse = getToParse()

    for word in getWord(toParse):
        word = word.rstrip("\n")
        displaySublim(word, args.time)
    
    if not (args.loop or args.executefile or args.directory or args.directoryrandom):
        break
