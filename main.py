#create bot for game 'infinitode 2'

import winsound
import numpy as np
import pyautogui
import keyboard
import time
import random
import os, sys, inspect
import cv2, mss
import pytesseract
import info
import maps

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Set up canstants
PATH = 'images/'
IMAGE_SUFFIX = '.png'
DEFAULT_WAIT_TIME = 0.1

def event_listener(timer):
    start = time.monotonic()
    while True:
        if time.monotonic() - start > timer: return
        if keyboard.is_pressed('alt'):
            print('Exit')
            winsound.Beep(1000, 1000)
            exit()
        if keyboard.is_pressed('-'):
            print('Pause')
            winsound.Beep(1000, 250)
            time.sleep(3)
            while True:
                if keyboard.is_pressed('-'):
                    print('Continue')
                    winsound.Beep(1000, 250)
                    time.sleep(0.5)
                    break
        time.sleep(0.01)

def press_key(key, count=1, duration=0, wait_time_after_press=DEFAULT_WAIT_TIME):
    if type(key) == str: key = [key]
    else: key = list(key)
    for i in range(count):
        for k in key: pyautogui.keyDown(k)
        event_listener(duration)
        for k in key: pyautogui.keyUp(k)
    event_listener(wait_time_after_press)

def click(xy, button='left', clicks=1, wait_time_after_click=DEFAULT_WAIT_TIME, click_duration=0.1):
    print(f'Clicking {xy}', time.strftime('%H:%M:%S'))
    pyautogui.moveTo(*xy)
    pyautogui.click(button=button, clicks=clicks, duration=click_duration)
    event_listener(wait_time_after_click)

def find_image(image_name,
               wait_duration=5, find_interval=0.1, grayscale=True, confidence=0.9, click=True, button='left',
               clicks=1, wait_time_after_click=DEFAULT_WAIT_TIME, click_duration=0.1, interval=0,
               if_not_found='exit'): # Or 'exit' or a function
    image = PATH + image_name + IMAGE_SUFFIX
    start_time = time.monotonic()
    while True:
        localtion = pyautogui.locateOnScreen(image, grayscale=grayscale, confidence=confidence)
        if localtion:
            print(f'Found {image_name}', time.monotonic())
            if click:
                pyautogui.moveTo(localtion)
                pyautogui.click(button=button, clicks=clicks, duration=click_duration, interval=interval)
                event_listener(wait_time_after_click)
            return localtion
        if time.monotonic() - start_time > wait_duration:
            if if_not_found == 'nothing':
                return None
            elif if_not_found == 'exit':
                print('Failed to find image: ' + image_name)
                exit()
            else:
                return if_not_found()
        event_listener(find_interval)

def center(location): # Get the center of the image location
    return (location.left+location.width/2, location.top+location.height/2) # (x, y) -> (row, col) (0, 0) is the top left corner

def get_game_map_grid(cell_1, cell_2, map_width, map_height):
    cell_1_location = find_image(cell_1['image'], wait_duration=5, grayscale=False, click=False)
    cell_2_location = find_image(cell_2['image'], wait_duration=5, grayscale=False, click=False)
    cell_1_location = center(cell_1_location)
    cell_2_location = center(cell_2_location)
    cell_width = (cell_2_location[0] - cell_1_location[0]) / (cell_2['position'][0] - cell_1['position'][0])
    cell_height = (cell_2_location[1] - cell_1_location[1]) / (cell_2['position'][1] - cell_1['position'][1])
    cell00_location = (cell_1_location[0] - cell_width * cell_1['position'][0], cell_1_location[1] - cell_height * cell_1['position'][1])
    grid: list[list[list[float]]] = []
    for i in range(map_width):
        grid.append([])
        for j in range(map_height):
            grid[i].append((cell00_location[0] + i * cell_width, cell00_location[1] + j * cell_height))
    return np.array(grid)

def get_coin_value(coin_image_name):
    coin_location = find_image(coin_image_name, grayscale=False, click=False)
    region = {'top': coin_location.top, 'left': coin_location.left+coin_location.width, 'width': 100, 'height': coin_location.height}
    # screen capture
    with mss.mss() as sct:
        img = np.array(sct.grab(region))
    # convert to gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # read the value
    value = pytesseract.image_to_string(gray, config='--psm 6')
    try:
        value = int(value)
    except:
        value = 0
    return value

def farm_1(this_map=maps.farm_1.copy()):
    find_image('level_redactor')
    find_image('play_button', grayscale=False)
    if not find_image('play', wait_duration=3, if_not_found='nothing'):
        find_image('ok')
        find_image('play')
    # Press ] to speed up twice
    press_key(']', 2)
    grid = get_game_map_grid(this_map['cell_1'], this_map['cell_2'], this_map['width'], this_map['height'])
    # Get towers for this map
    towers_to_build = list(this_map['towers'].keys())
    towers_info = {}
    # Get cells to build towers
    for i in range(len(towers_to_build)):
        tower = towers_to_build[i]
        towers_info[tower] = {}
        towers_info[tower]['cels'] = []
        for j in range(len(this_map['towers'][tower]['cels'])):
            x, y = this_map['towers'][tower]['cels'][j]
            towers_info[tower]['cels'].append((x, y))

    # Get the location of the first tower
    tower_location = towers_info[towers_to_build[0]]['cels'][0]
    # Build the first tower
    click(grid[tower_location])
    press_key(info.towers[towers_to_build[0]]['hotkey'])
    # Remember location of the first tower of this type
    towers = {towers_to_build[0]: tower_location}
    # Remove this position from the list
    towers_info[towers_to_build[0]]['cels'].pop(0)

    # Get the location of the second tower
    tower_location = towers_info[towers_to_build[1]]['cels'][0]
    # Build the second tower
    click(grid[tower_location])
    press_key(info.towers[towers_to_build[1]]['hotkey'])
    # Remember the location of the first tower of this type
    towers[towers_to_build[1]] = tower_location
    # Remove this position from the list
    towers_info[towers_to_build[1]]['cels'].pop(0)

    core_upgrades = ['uc1', 'uc2', 'uc3', 'uc4', 'uc5', 'uc6', 'uc7', 'uc8', 'uc9', 'uc10', 'uc11', 'uc12', 'uc13', 'uc14', 'uc15', 'uc16']

    # Press cntrl+space to start the game
    press_key(['ctrl', 'space'])
    # Loop until the game is over
    while True:
        # Are we in the game?
        # if not find_image('game_on_taskbar', wait_duration=3, if_not_found='nothing'): ...
        # If the game is over
        if find_image('menu', wait_duration=0, if_not_found='nothing'):
            print('Game over at', time.strftime('-----------------%X', time.localtime()))
            press_key('esc')
            event_listener(5)
            return farm_1()
        
        # If there are still towers to build
        # And if we have enough coins to build the next tower
        while len(towers_to_build) > 0 and get_coin_value('coin') >= info.towers[towers_to_build[0]]['cost']:
            # Get the location of the next tower
            tower_location = towers_info[towers_to_build[0]]['cels'][0]
            # Build the next tower
            click(grid[tower_location])
            press_key(info.towers[towers_to_build[0]]['hotkey'])
            # Remember the location of the first tower of this type (if there is the first tower of this type)
            if towers_to_build[0] not in towers: towers[towers_to_build[0]] = tower_location
            # Remove this position from the list
            towers_info[towers_to_build[0]]['cels'].pop(0)
            # Remove this tower from the list if there are no more positions
            if len(towers_info[towers_to_build[0]]['cels']) == 0: towers_to_build.pop(0)
        
        # Check if the core(is the cell 1) needs to be upgraded
        click(grid[this_map['cell_1']['position']])
        for upgrade in core_upgrades:
            location = find_image(upgrade, grayscale=False, if_not_found='nothing', wait_duration=0, confidence=0.95)
            if location: click((location.left, location.top))

        # Upgrade all the towers
        for tower in towers:
            click(grid[towers[tower]])
            # Press cntrl+shift to upgrade all the towers of same type by 1 level if there are enough coins
            press_key(['ctrl', 'shift'])
            # Press cntrl+num upgredes to select the upgrade to be applied to all the towers of same type if there are enough xp level of the tower
            for upgrade in info.towers[tower]['num upgrades']:
                press_key(['ctrl', upgrade])
        

        


    # Print coin value

if __name__ == '__main__':
    # test
    find_image('game_on_taskbar')
    farm_1()