unlocked_towers = ['base', 'sniper', 'cannot', 'freese', 'antiair', 'splesh', 'blast', 'multi', 'minigun', 'venom', 'tesla', 'rocket', 'flamethrower', 'laser']
towers = {
    'base': {
        'hotkey': '3',
        'cost': 39,
        'max_level': 10,
        'num_upgrades': [],
    },
    'sniper': {
        'hotkey': '4',
        'cost': 54,
        'num_upgrades': ['num1', 'num2', 'num5'],
        'max_level': 10,
    },
    'cannot': {
        'hotkey': '5',
        'cost': 46,
        'max_level': 10,
        'num_upgrades': [],
    },
    'freese': {
        'hotkey': '6',
        'cost': 71,
        'num_upgrades': ['num1', 'num2', 'num6'],
        'max_level': 10,
    },
    'anti_air': {
        'hotkey': 'e',
        'cost': 33,
        'num_upgrades': ['num1', 'num2', 'num6'],
        'max_level': 10,
    },
    'splesh': {
        'hotkey': 'r',
        'cost': 66,
        'max_level': 10,
        'num_upgrades': [],
    },
    'blast': {
        'hotkey': 't',
        'cost': 57,
        'max_level': 10,
        'num_upgrades': [],
    },
    'multi': {
        'hotkey': 'y',
        'cost': 74,
        'max_level': 10,
        'num_upgrades': [],
    },
    'minigun': {
        'hotkey': 'd',
        'cost': 93,
        'max_level': 9,
        'num_upgrades': [],
    },
    'venom': {
        'hotkey': 'f',
        'cost': 82,
        'max_level': 10,
        'num_upgrades': [],
    },
    'tesla': {
        'hotkey': 'g',
        'cost': 78,
        'num_upgrades': ['num1', 'num2', 'num6'],
        'max_level': 10,
    },
    'rocket': {
        'hotkey': 'h',
        'cost': 123,
        'max_level': 10,
        'num_upgrades': [],
    },
    'flamethrower': {
        'hotkey': 'c',
        'cost': 71,
        'num_upgrades': ['num3', 'num1', 'num6'],
        'max_level': 10,
    },
    'laser': {
        'hotkey': 'v',
        'cost': 52,
        'max_level': 10,
        'num_upgrades': ['num3', 'num1', 'num6'],
    },
}
mods = {
    'xp': {
        'hotkey': ['ctrl', '3'],
        'costs': [25, 150, 225],
        'max_level': 1,
    },
    'search': {
        'hotkey': ['ctrl', '4'],
        'costs': [50, 150, 225],
        'max_level': 0,
    },
    'power': {
        'hotkey': ['ctrl', '5'],
        'costs': [100, 150, 225],
        'max_level': 0,
    },
    'damage': {
        'hotkey': ['ctrl', '6'],
        'costs': [100, 150, 225, 335, 510, 760, 1140],
        'max_level': 0,
    },
    'attack_speed': {
        'hotkey': ['ctrl', 'e'],
        'costs': [100, 150, 225, 335, 510, 760, 1140],
        'max_level': 0,
    },
    'mining_speed': {
        'hotkey': ['ctrl', 'r'],
        'costs': [120, 150, 225],
        'max_level': 5,
    },
    'reward': {
        'hotkey': ['ctrl', 't'],
        'costs': [720, 1240, 2120, 3640, 6250, 10750, 18450, 31650],
        'percent': 2,
        'max': 88,
        'max_level': 0,
    },
}