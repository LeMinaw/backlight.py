#!/usr/bin/python

# - SCRIPT CONFIGURATION -

blName = "intel_backlight"
blTargets = [1, 10, 20, 50, 75, 100] # In %

# - END SCRIPT CONFIGURATION -

import subprocess
import sys

def scale(x, in_min, in_max, out_min=0, out_max=1):
    '''A fuction that applies linear scaling from one range of values to another.
    Synopsis : scale(number, number, number, number, number)
    Returns : number
    Exemple : y = map(x, 0, 255, 0, 100)'''
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;

def shellcmd(command):
    '''A fuction that executes the shell command it takes in argument, then returns its output.
    Synopsis : shellcmd(string)
    Returns : string
    Exemple : calendar = shellcmd("cal")'''
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (cmdResult, err) = proc.communicate()
    return cmdResult

def incbl():
    blIndex = 0
    while scale(blTargets[blIndex], 0, 100, 0, maxBl) <= oldBl: # Searching for the strictly superior brightness level
        blIndex += 1
        if blIndex > len(blTargets) - 1: # Preventing from overflow
            blIndex = len(blTargets) - 1
            break
    newBl = int(scale(blTargets[blIndex], 0, 100, 0, maxBl))
    shellcmd("echo -n " + str(newBl) + " > " + blPath + "brightness")

def decbl():
    blIndex = len(blTargets) - 1
    while scale(blTargets[blIndex], 0, 100, 0, maxBl) >= oldBl: # Searching for the strictly superior brightness level
        blIndex -= 1
        if blIndex < 0: # Preventing from overflow
            blIndex = 0
            break
    newBl = int(scale(blTargets[blIndex], 0, 100, 0, maxBl))
    shellcmd("echo -n " + str(newBl) + " > " + blPath + "brightness")

blPath = "/sys/class/backlight/"+blName+"/"
maxBl = int(shellcmd("cat " + blPath + "max_brightness")) # The max brightness
oldBl = int(shellcmd("cat " + blPath + "brightness"))

if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == "inc":
            incbl()
        elif sys.argv[1] == "dec":
            decbl()
        else:
            print "[ERROR] Incorrect argument " + str(sys.argv[1]) + " ! Try with a 'inc' or 'dec' argument."
    else:
        print "[ERROR] This script takes exactly one argument ! Given : " + str(len(sys.argv) - 1) + "."
