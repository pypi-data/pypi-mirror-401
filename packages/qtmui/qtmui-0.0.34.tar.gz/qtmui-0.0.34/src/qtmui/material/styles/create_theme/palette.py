from typing import Dict, Union

# Các màu sắc được định nghĩa trong hệ thống
GREY = {
    0: '#FFFFFF',
    100: '#F9FAFB',
    200: '#F4F6F8',
    300: '#DFE3E8',
    400: '#C4CDD5',
    500: '#919EAB',
    600: '#637381',
    700: '#454F5B',
    800: '#212B36',
    900: '#161C24',
}

PRIMARY = {
    'lighter': '#C8FAD6',
    'light': '#5BE49B',
    'main': '#00A76F',
    'dark': '#007867',
    'darker': '#004B50',
    'contrastText': '#FFFFFF',
}

SECONDARY = {
    'lighter': '#EFD6FF',
    'light': '#C684FF',
    'main': '#8E33FF',
    'dark': '#5119B7',
    'darker': '#27097A',
    'contrastText': '#FFFFFF',
}

INFO = {
    'lighter': '#CAFDF5',
    'light': '#61F3F3',
    'main': '#00B8D9',
    'dark': '#006C9C',
    'darker': '#003768',
    'contrastText': '#FFFFFF',
}

SUCCESS = {
    'lighter': '#D3FCD2',
    'light': '#77ED8B',
    'main': '#22C55E',
    'dark': '#118D57',
    'darker': '#065E49',
    'contrastText': '#ffffff',
}

WARNING = {
    'lighter': '#FFF5CC',
    'light': '#FFD666',
    'main': '#FFAB00',
    'dark': '#B76E00',
    'darker': '#7A4100',
    'contrastText': GREY[800],
}

ERROR = {
    'lighter': '#FFE9D5',
    'light': '#FFAC82',
    'main': '#FF5630',
    'dark': '#B71D18',
    'darker': '#7A0916',
    'contrastText': '#FFFFFF',
}

# Các giá trị phổ biến
COMMON = {
    'common': {'black': '#000000', 'white': '#FFFFFF'},
    'primary': PRIMARY,
    'secondary': SECONDARY,
    'info': INFO,
    'success': SUCCESS,
    'warning': WARNING,
    'error': ERROR,
    'grey': GREY,
    'divider': 'rgba(145, 158, 171, 0.2)',
    'action': {
        'hover': 'rgba(145, 158, 171, 0.08)',
        'selected': 'rgba(145, 158, 171, 0.16)',
        'disabled': 'rgba(145, 158, 171, 0.8)',
        'disabledBackground': 'rgba(145, 158, 171, 0.24)',
        'focus': 'rgba(145, 158, 171, 0.24)',
        'hoverOpacity': 0.08,
        'disabledOpacity': 0.48,
    },
}

# Hàm tạo palette cho hệ thống
def palette(mode: str) -> Dict:
    light = {
        **COMMON,
        'mode': 'light',
        'text': {
            'primary': GREY[800],
            'secondary': GREY[600],
            'disabled': GREY[500],
        },
        'background': {
            'paper': GREY[100],
            'default': '#FFFFFF',
            'neutral': GREY[200],
            'notched': GREY[300],
            'navigation': "#F9F9F9",
            'main': "#F9F9F9", # kieu cua postman
            # 'main': GREY[300], # mini_nav
            'second': GREY[200], # label_nav
            'thirty': GREY[100], # group_nav
            'content': GREY[0], # group_detail
            # 'main': "#ecedee", # mini_nav
            # 'second': "#f4f5f6", # label_nav
            # 'thirty': "#DFE3E8", # group_nav
            # 'content': "#f8f9fa", # group_detail
            'transparent': "transparent"
        },
        'action': {
            **COMMON['action'],
            'active': GREY[600],
        },
    }

    dark = {
        **COMMON,
        'mode': 'dark',
        'text': {
            'primary': '#FFFFFF',
            'secondary': GREY[500],
            'disabled': GREY[600],
        },
        'background': {
            'paper': GREY[800],
            'default': GREY[900],
            'neutral': GREY[700],
            'notched': 'rgba(145, 158, 171, 0.04)',
            # 'navigation': "#161C24",
            'navigation': GREY[800],
            # 'main': GREY[900], # mini_nav
            # 'second': GREY[800], # label_nav
            # 'thirty': GREY[700], # group_nav
            # 'content': GREY[600], # group_detail
            # 'main': "#161C24", # mini_nav
            # 'second': "#19212A", # label_nav
            # 'thirty': "#1D2630", # group_nav
            # 'content': "#212B36", # group_detail
            # 'main': "#161C24", # mini_nav
            # 'second': "#252D36", # label_nav
            # 'thirty': "#353E48", # group_nav
            # 'content': "#454F5B", # group_detail
            # 'main': "#454F5B", # mini_nav
            'main': GREY[800], # mini_nav #262626 postman
            'second': "#353E48", # label_nav
            'thirty': "#252D36", # group_nav
            'content': GREY[900], # group_detail
            'transparent': "transparent"
        },
        'action': {
            **COMMON['action'],
            'active': GREY[500],
        },
    }

    _mode = light if mode == 'light' else dark
    # print('_mode____________________', _mode["mode"])

    return _mode
