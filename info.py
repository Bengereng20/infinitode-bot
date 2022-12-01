unlocked_towers = ['base', 'sniper', 'cannot', 'freese', 'antiair', 'splesh', 'blast', 'multi', 'minigun', 'venom', 'tesla', 'rocket', 'flamethrower']
towers = {
    'base': {
        'hotkey': '3',
        'cost': 39,
        'upgrade_costs': [1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000],
        'max_level': 10,
    },
    'sniper': {
        'hotkey': '4',
        'cost': 54,
        'num_upgrades': ['num1', 'num2', 'num5'],
        'upgrade_costs': [1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000],
        'max_level': 10,
    },
    'cannot': {
        'hotkey': '5',
        'cost': 46,
        'upgrade_costs': [1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000],
        'max_level': 10,
    },
    'freese': {
        'hotkey': '6',
        'cost': 71,
        'num_upgrades': ['num1', 'num2', 'num6'],
        'upgrade_costs': [19, 32, 51, 79, 126, 197, 305, 493, 799, 1269],
        'max_level': 10,
    },
    'anti_air': {
        'hotkey': 'e',
        'cost': 33,
        'num_upgrades': ['num1', 'num3', 'num6'],
        'upgrade_costs': [1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000],
        'max_level': 10,
    },
    'splesh': {
        'hotkey': 'r',
        'cost': 66,
        'upgrade_costs': [1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000],
        'max_level': 10,
    },
    'blast': {
        'hotkey': 't',
        'cost': 57,
        'upgrade_costs': [1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000],
        'max_level': 10,
    },
    'multi': {
        'hotkey': 'y',
        'cost': 74,
        'upgrade_costs': [1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000],
        'max_level': 10,
    },
    'minigun': {
        'hotkey': 'd',
        'cost': 93,
        'upgrade_costs': [1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000],
        'max_level': 10,
    },
    'venom': {
        'hotkey': 'f',
        'cost': 82,
        'upgrade_costs': [1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000],
        'max_level': 10,
    },
    'tesla': {
        'hotkey': 'g',
        'cost': 78,
        'num_upgrades': ['num1', 'num2', 'num6'],
        'upgrade_costs': [25, 37, 65, 103, 141, 232, 352, 512, 846, 1175],
        'max_level': 10,
    },
    'rocket': {
        'hotkey': 'h',
        'cost': 123,
        'upgrade_costs': [1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000],
        'max_level': 10,
    },
    'flamethrower': {
        'hotkey': 'c',
        'cost': 71,
        'num_upgrades': ['num3', 'num1', 'num6'],
        'upgrade_costs': [19, 27, 54, 77, 115, 202, 272, 413, 775, 1222],
        'max_level': 10,
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
        'max_level': 1,
    },
    'power': {
        'hotkey': ['ctrl', '5'],
        'costs': [100, 150, 225],
        'max_level': 0,
    },
    'damage': {
        'hotkey': ['ctrl', '6'],
        'costs': [100, 150, 225, 335, 510],
        'max_level': 0,
    },
    'attack_speed': {
        'hotkey': ['ctrl', 'e'],
        'costs': [100, 150, 225, 335, 510],
        'max_level': 0,
    },
    'mining_speed': {
        'hotkey': ['ctrl', 'r'],
        'costs': [120, 150, 225],
        'max_level': 5,
    },
    'reward': {
        'hotkey': ['ctrl', 't'],
        'costs': [720, 1240, 2120, 3640, 6250, 10750],
        'percent': 2,
        'max': 70,
        'max_level': 0,
    },
}