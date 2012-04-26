import pyosd
import argparse
import subprocess

osd = pyosd.osd()

def displaySublim(string, delay):
    import random
    import time

    global osd

    osd.set_vertical_offset(random.randint(0, screenHeight))
    osd.set_horizontal_offset(random.randint(0, screenWidth))
    osd.show()
    osd.display(string)
    time.sleep(delay)
    osd.hide()

parser = argparse.ArgumentParser(description = "Python script to display subliminal messages")
parser.add_argument("File")
parser.add_argument("-c", "--color", help = "Font color (default: black)", default = "black")
parser.add_argument("-s", "--size", help = "Font size (default: 25)", default = "25")
parser.add_argument("-t", "--time", type = float, help = "Time in seconds the message will be displayed (deafult: .05)", default = .05)
parser.add_argument("-l", "--loop", help = "Use this option if you wish to loop subliminals until killed", action = "store_true")
parser.add_argument("-e", "--execute", help = "Use if you want to execute a command instead of reading from a file", action = "store_true")
parser.add_argument("-ef", "--executefile", help = "Use if you want to execute a list of commands from a file", action = "store_true")

args = parser.parse_args()

osd.set_colour(args.color)
osd.set_font("-*-*-*-*-*-*-" + args.size + "-*-*-*-*-*-*-*")

screenWidth = 1680
screenHeight = 1050

if args.execute and args.executefile:
    print "Conflicting options 'execute' and 'executefile'"
    exit()

if args.executefile:
    file = open(args.File, "r")

while True:
    if args.execute:
        toParse = subprocess.Popen(args.File.split(), stdout=subprocess.PIPE).stdout
    elif args.executefile:
        command = file.readline().rstrip("\n").split()

        if len(command) == 0:
            if not args.loop:
                break
            file.seek(0)
            command = file.readline().rstrip("\n").split()

        toParse = subprocess.Popen(command, stdout=subprocess.PIPE).stdout
    else:
        toParse = open(args.File, "r")

    for line in toParse:
        for word in line.split(" "):
            word = word.rstrip("\n")
            displaySublim(word, args.time)

    
    if not (args.loop or args.executefile):
        break
    
    if not (args.execute or args.executefile):
        toParse.seek(0)
