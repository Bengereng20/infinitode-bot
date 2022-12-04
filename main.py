import math
import winsound
import numpy as np
import pyautogui
import keyboard
import time
import random
import os
import cv2, mss
import pytesseract
import info
import maps

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
pyautogui.PAUSE = 0.01

# Set up constants
WINF = os.popen('wmic path win32_desktopmonitor get screenheight, screenwidth').read()
PATH_TO_IMAGES = 'images/'
PATH_TO_LOG = 'log/'
IMAGE_SUFFIX = '.png'
DEFAULT_WAIT_TIME = 0.01

def event_listener(timer):
    start = time.monotonic()
    while True:
        if time.monotonic() - start > timer: return
        if find_image('menu', wait_duration=0, if_not_found='nothing'):
            print('Game over at', time.strftime('-----------------%X', time.localtime()))
            event_listener(1)
            find_image('menu', wait_duration=0, if_not_found='nothing')
            press_key('esc')
            event_listener(1)
            farm()
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

def press_key(key, count=1, duration=0.0, wait_time_after_press=DEFAULT_WAIT_TIME):
    if type(key) == str: key = [key]
    else: key = list(key)
    for i in range(count):
        for k in key: pyautogui.keyDown(k)
        time.sleep(duration)
        for k in key: pyautogui.keyUp(k)
    event_listener(wait_time_after_press)

def click(xy, button='left', clicks=1, wait_time_after_click=DEFAULT_WAIT_TIME, click_duration=0.01):
    pyautogui.moveTo(*xy)
    pyautogui.click(button=button, clicks=clicks, duration=click_duration)
    event_listener(wait_time_after_click)

def find_image(image_name,
               wait_duration=5, find_interval=0.1, grayscale=True, confidence=0.9, click=True, button='left',
               clicks=1, wait_time_after_click=DEFAULT_WAIT_TIME, click_duration=0.1, interval=0, region=None,
               if_not_found='exit'): # Or 'exit' or a function
    image = PATH_TO_IMAGES + image_name + IMAGE_SUFFIX
    start_time = time.monotonic()
    while True:
        localtion = pyautogui.locateOnScreen(image, grayscale=grayscale, confidence=confidence, region=region)
        if localtion:
            print(f'Found {image_name}', time.strftime('%X', time.localtime()))
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
    coin_location = find_image(coin_image_name, grayscale=False, wait_time_after_click=0)
    region = {'top': coin_location.top, 'left': coin_location.left+coin_location.width, 'width': 100, 'height': coin_location.height}
    # screen capture
    with mss.mss() as sct:
        img = np.array(sct.grab(region))
    # convert to gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # read the value
    value = pytesseract.image_to_string(gray, config='--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789 ,')
    value = value.replace(',', '')
    value = value.replace(' ', '')
    try:
        value = int(value)
    except:
        value = 0
    return value

def get_upgrade_cost(left=1859, top=908, width=61, height=22):
    region = {'top': top, 'left': left, 'width': width, 'height': height}
    # screen capture
    with mss.mss() as sct:
        img = np.array(sct.grab(region))
    # convert to gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # read the value
    value = pytesseract.image_to_string(gray, config='--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789 ,')
    print('Upgrade cost: ', value)
    value = value.replace(' ', '')
    try:
        value = int(value)
    except:
        # Log image and value to log directory
        _image_name = f'upgrade_cost_{time.strftime("%Y%m%d_%H%M%S", time.localtime())}.png'
        cv2.imwrite(os.path.join(PATH_TO_LOG, _image_name), img)
        with open(os.path.join(PATH_TO_LOG, 'upgrade_cost.txt'), 'r') as f:
            text = f.read()
        with open(os.path.join(PATH_TO_LOG, 'upgrade_cost.txt'), 'w') as f:
            f.write(text + f'Upgrade cost: {value} at {_image_name}/n')
        value = 1000000000
    return value

def update_offset(rtb, _rewards, _offset, value, offset_multiplier):
    if value < 0: value = 0
    if len(rtb) == 0:
        _offset = info.mods['reward']['max'] / (info.mods['reward']['percent'] / 100) if _rewards > 0 else 0
    else:
        _offset = _offset+value*offset_multiplier
    return _offset

def farm(this_map=maps.main):
    find_image('level_redactor')
    _region =  [0, 0, 1920, 1080]
    for _ in range(this_map['ordinal_number'] - 1):
        _location = find_image('play_button', region=_region, grayscale=False, click=False)
        _region[1] = _location.top + _location.height
    find_image('play_button', grayscale=False, region=_region)
    if not find_image('play', wait_duration=3, if_not_found='nothing'):
        find_image('ok')
        find_image('play')
    press_key(']', 2, 0.5)
    pyautogui.moveTo(0, 300)
    pyautogui.dragTo(0, 350, 0.25)
    grid = get_game_map_grid(this_map['cell_1'], this_map['cell_2'], this_map['width'], this_map['height'])
    # Get towers for this map
    towers_info = this_map['towers']

    towers_order = [ round(len(towers_info[tower]['cells'])*towers_info[tower]['priority']) for tower in towers_info ]
    _max = max(towers_order)
    _min = min(towers_order)
    _gcd = math.gcd(*towers_order)
    towers_order = []
    for tower in towers_info:
        towers_order.extend([ tower for _ in range(round( len(towers_info[tower]['cells'])*towers_info[tower]['priority'] / _gcd )) ])
    
    random.shuffle(towers_order)
    for tower in list(towers_info.keys())[::-1]:
        if tower not in towers_order: continue
        towers_order.insert(0, towers_order.pop(towers_order.index(tower)))
    
    towers = {}
    mods = {}

    mods_to_build = []
    rewards_to_build = []
    for mod in list(this_map['mods'].keys()):
        for i, cell in enumerate(this_map['mods'][mod]['cells']):
            if mod != 'reward':
                mods_to_build.append({
                    'mod': mod,
                    'cell': cell,
                    'cost': info.mods[mod]['costs'][i],
                })
            else:
                rewards_to_build.append({
                    'mod': mod,
                    'cell': cell,
                    'cost': info.mods[mod]['costs'][i],
                })
    # Sort mods by cost
    mods_to_build.sort(key=lambda x: x['cost'])
    rewards = 0 # This mod gets info.mods['reward']['percent']% from existing coins as a reward per wave, but no more than info.mods['reward']['max']
    offset = 0
    first_towers = {}
    tasks = {}

    for tower in towers_info:
        for i, cell in enumerate(towers_info[tower]['cells']):
            tasks[cell] = {
                'name': tower,
                'type': 'build',
                'object_type': 'tower',
                'object': tower,
                'cost': info.towers[tower]['cost'],
            }
    for mod in mods_to_build:
        tasks[mod['cell']] = {
            'name': mod['mod'],
            'type': 'build',
            'object_type': 'mod',
            'object': mod['mod'],
            'cost': mod['cost'],
        }


    core_upgrades = this_map['core_upgrades'].copy()

    # Press cntrl+space to start the game
    press_key(['ctrl', 'space'])
    
    while True:
        # Are we in the game?
        # if not find_image('game_on_taskbar', wait_duration=3, if_not_found='nothing'): ... TODO
        
        # Check if the core(is the cell 1) needs to be upgraded
        if len(core_upgrades) > 0:
            click(grid[this_map['cell_1']['position']])
            location = find_image(core_upgrades[0], grayscale=False, if_not_found='nothing', wait_duration=0, confidence=0.95)
            if location:
                click((location.left, location.top))
                core_upgrades.pop(0)
        
        coins = get_coin_value('coin')
        available_coins = coins - offset
            
        # If there are still rewards to build
        if len(rewards_to_build) > 0 and coins > rewards_to_build[0]['cost']:
            # Calculate the current reward
            current_reward = min(offset * info.mods['reward']['percent'] / 100, info.mods['reward']['max']) * rewards
            # Calculate the new reward
            new_reward = min((coins-rewards_to_build[0]['cost']) * info.mods['reward']['percent'] / 100, info.mods['reward']['max']) * (rewards+1)
            if new_reward > current_reward:
                # Build the next reward
                click(grid[rewards_to_build[0]['cell']])
                press_key(info.mods[rewards_to_build[0]['mod']]['hotkey'])
                available_coins -= rewards_to_build[0]['cost']
                # Remove this reward from the list
                rewards_to_build.pop(0)
                # Increase the reward counter
                rewards += 1
                if offset > info.mods['reward']['max'] / (info.mods['reward']['percent'] / 100):
                    offset = info.mods['reward']['max'] / (info.mods['reward']['percent'] / 100)
        
        
        # If any cost == 1000000000, it means that we don't know the cost of this task
        # So we need to find it
        for cell in tasks:
            if tasks[cell]['cost'] == 1000000000:
                click(grid[cell])
                tasks[cell]['cost'] = get_upgrade_cost()

        # Get tasks keys sorted by cost
        tasks_keys = list(tasks.keys())
        tasks_keys.sort(key=lambda x: tasks[x]['cost'])

        task_counter = 0
        last_cell = None
        while len(tasks_keys) > 0 and task_counter < 20:
            # Get the first task
            cell = tasks_keys[0]
            task = tasks[tasks_keys[0]]

            if available_coins <= task['cost']: break # If there are not enough coins to build or upgrade the next object, break the loop
            if towers_order[0] != task['object'] and task['object_type'] == 'tower':
                tasks_keys.pop(0)
                continue   

            available_coins -= task['cost']
            offset = update_offset(rewards_to_build, rewards, offset, task['cost'], this_map['offset_multiplier'])
            if last_cell != cell:
                click(grid[cell])
                last_cell = cell
            
            if task['object_type'] == 'tower':
                _info = info.towers[task['object']]
                this_object = towers
                towers_order.append(towers_order.pop(0))
                
            elif task['object_type'] == 'mod':
                _info = info.mods[task['object']]
                this_object = mods


            if task['type'] == 'build':
                press_key(_info['hotkey'])
                if task['object_type'] == 'tower':
                    towers[cell] = {
                        'position': cell,
                        'type': task['object'],
                        'level': 0,
                    }
                    # If this is the first tower of this type, save it
                    if task['object'] not in first_towers: first_towers[task['object']] = cell

                elif task['object_type'] == 'mod':
                    mods[cell] = {
                        'position': cell,
                        'type': task['object'],
                        'level': 0,
                    }
                task['type'] = 'upgrade'

            elif task['type'] == 'upgrade':
                press_key('shift', wait_time_after_press=0.0001)
                this_object[cell]['level'] += 1

            # If the object is max level, remove it from the tasks list
            if this_object[cell]['level'] == _info['max_level']:
                # If this is the last tower of this type in tasks, remove all this type from towers_order list
                if task['object_type'] == 'tower' and len([ x for x in tasks if tasks[x]['object'] == task['object'] ]) == 1:
                    towers_order = [tower for tower in towers_order if tower != task['object']]
                tasks.pop(cell)
            else:
                task['cost'] = get_upgrade_cost()

            if task['object_type'] == 'tower':
                for key in towers_info[ task['object'] ]['settings'][ this_object[cell]['level'] ]:
                    press_key(key, wait_time_after_press=0)

            tasks_keys = list(tasks.keys())
            tasks_keys.sort(key=lambda x: tasks[x]['cost'])
            task_counter += 1


        print('Coins: '+str(coins))
        print('Offset: '+str(offset))

        
        if task_counter < 20:
            # Let's go on the list of towers and upgrade their num upgrades
            for tower in first_towers:
                click(grid[first_towers[tower]])
                for upgrade in info.towers[tower]['num_upgrades']:
                    press_key(['ctrl', upgrade], 1, 0, 0)

if __name__ == '__main__':
    find_image('game_on_taskbar')
    farm()