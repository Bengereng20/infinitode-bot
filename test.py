import numpy as np
import pyautogui
import time
import os, sys, inspect
import subprocess as sbp
import csv

# Get process info
# pinf = sbp.run('TASKLIST /FI "IMAGENAME eq infinitode-2.exe" /V /fo csv /nh', shell=True, stdout=sbp.PIPE, encoding='866').stdout
# pinf = list(csv.reader(pinf.splitlines(), delimiter=','))
# print(pinf)

# Get window info
# winf = sbp.run('wmic path win32_desktopmonitor get screenheight, screenwidth', shell=True, stdout=sbp.PIPE, encoding='866').stdout
# winf = list(csv.reader(winf.splitlines(), delimiter=' '))
# print(winf)