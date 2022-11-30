hardcoded_connections = [
    ('0', '1'),
    ('1', '3'),
    ('1', '2'),
    ('3', '4'),
    ('2', '4'),
    ('2', '5'),
    ('5', '6'),
    ('5', '7'),
    ('6', '7'),
    ('8', '9')
]


connections = {
    '0': ['1'],
    '1': ['0', '3', '2'],
    '2': ['1', '4', '5'],
    '3': ['1', '4'],
    '5': ['2', '6', '7'],
    '6': ['5', '7'],
    '7': ['5', '6', '8'],
    '8': ['7', '9'],
    '9': ['8']
}


topologia_inicial = {
    {
        'nodo': '0',
        'is_server': True,
        'is_bigNode': False,
    },
    {
        'nodo': '1',
        'is_server': False,
        'is_bigNode': False,
    },
    {
        'nodo': '2',
        'is_server': False,
        'is_bigNode': False,
    },
    {
        'nodo': '3',
        'is_server': False,
        'is_bigNode': False,
    },
    {
        'nodo': '4',
        'is_server': False,
        'is_bigNode': False,
    },
    {
        'nodo': '5',
        'is_server': False,
        'is_bigNode': False,
    },
    {
        'nodo': '6',
        'is_server': False,
        'is_bigNode': False,
    },
    {
        'nodo': '7',
        'is_server': False,
        'is_bigNode': False,
    },
    {
        'nodo': '8',
        'is_server': False,
        'is_bigNode': False,
    },
    {
        'nodo': '9',
        'is_server': False,
        'is_bigNode': False,
    }
}


topologia_ideal = {
    {
        'nodo': '0',
        'is_server': True,
        'is_bigNode': False,
        'fastest_path': []
    },
    {
        'nodo': '1',
        'is_server': False,
        'is_bigNode': False,
        'fastest_path': ['0']
    },
    {
        'nodo': '2',
        'is_server': False,
        'is_bigNode': False,
        'fastest_path': ['1', '0']
    },
    {
        'nodo': '3',
        'is_server': False,
        'is_bigNode': False,
        'fastest_path': ['1', '0']
    },
    {
        'nodo': '4',
        'is_server': False,
        'is_bigNode': False,
        'fastest_path': ['3', '1', '0']
    },
    {
        'nodo': '5',
        'is_server': False,
        'is_bigNode': True,
        'fastest_path': ['2', '1', '0']
    },
    {
        'nodo': '6',
        'is_server': False,
        'is_bigNode': False,
        'fastest_path': ['5', '0']
    },
    {
        'nodo': '7',
        'is_server': False,
        'is_bigNode': False,
        'fastest_path': ['5', '0']
    },
    {
        'nodo': '8',
        'is_server': False,
        'is_bigNode': False,
        'fastest_path': ['7', '5', '0']
    },
    {
        'nodo': '9',
        'is_server': False,
        'is_bigNode': False,
        'fastest_path': ['8', '7', '5', '0']
    }
}


topologia_arvore = {
    '0': ['1'],
    '1': ['0', '3', '2'],
    '2': ['1', '5'],
    '3': ['1', '4'],
    '5': ['2', '6', '7'],
    '6': ['5'],
    '7': ['5', '8'],
    '8': ['7', '9'],
    '9': ['8']
}


# ----------------------- topologia.py -----------------------

