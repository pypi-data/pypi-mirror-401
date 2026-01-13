from ...system.color_manipulator import alpha
from .palette import palette
from .create_palette import Palette

class Shadows:
    z1 : tuple = None
    z2 : tuple = None
    z3 : tuple = None
    z4 : tuple = None
    z5 : tuple = None
    z6 : tuple = None
    z7 : tuple = None
    z8 : tuple = None
    z9 : tuple = None
    z10 : tuple = None
    z11 : tuple = None
    z12 : tuple = None
    z13 : tuple = None
    z14 : tuple = None
    z15 : tuple = None
    z16 : tuple = None
    z17 : tuple = None
    z18 : tuple = None
    z19 : tuple = None
    z20 : tuple = None
    z21 : tuple = None
    z22 : tuple = None
    z23 : tuple = None
    z24 : tuple = None

    primary : tuple = ""
    info : tuple = ""
    secondary : tuple = ""
    success : tuple = ""
    warning : tuple = ""
    error : tuple = ""
    card : tuple = ""
    dialog : tuple = ""
    dropdown : tuple = ""
    

    def __init__(self,options):
        self.z1 = options['z1']
        self.z2 = options['z2']
        self.z3 = options['z3']
        self.z4 = options['z4']
        self.z5 = options['z5']
        self.z6 = options['z6']
        self.z7 = options['z7']
        self.z8 = options['z8']
        self.z9 = options['z9']
        self.z10 = options['z10']
        self.z11 = options['z11']
        self.z12 = options['z12']
        self.z13 = options['z13']
        self.z14 = options['z14']
        self.z15 = options['z15']
        self.z16 = options['z16']
        self.z17 = options['z17']
        self.z18 = options['z18']
        self.z19 = options['z19']
        self.z20 = options['z20']
        self.z21 = options['z21']
        self.z22 = options['z22']
        self.z23 = options['z23']
        self.z24 = options['z24']
        self.primary = options['primary']
        self.info = options['info']
        self.secondary = options['secondary']
        self.success = options['success']
        self.warning = options['warning']
        self.error = options['error']
        self.card = options['card']
        self.dialog = options['dialog']
        self.dropdown = options['dropdown']




def create_shadows(palette: Palette)->Shadows:
    transparent = alpha(palette.grey._200 if palette.mode == "light" else palette.grey._200, 0.04)
    transparent = palette.grey._300
    card_color = alpha(palette.grey._500 if palette.mode == "light" else palette.common.black, 0.2)
    dialog_dropdown_color = alpha(palette.grey._500 if palette.mode == "light" else palette.common.black, 0.24)

    shadows_1_24 = {}
    for i in range(25):
        if i != 0:
            shadows_1_24.update({f"z{i}": (i, 0, 1, int(f"{i*2 + 25}"))})

    shadows = shadows_1_24 | {
        # "primary" : (10, 8, 16, f"{alpha(palette.primary.main, 0.24)}"),
        # "info" : (10, 8, 16, f"{alpha(palette.info.main, 0.24)}"),
        # "secondary" : (10, 8, 16, f"{alpha(palette.secondary.main, 0.24)}"),
        # "success" : (10, 8, 16, f"{alpha(palette.success.main, 0.24)}"),
        # "warning" : (10, 8, 16, f"{alpha(palette.warning.main, 0.24)}"),
        # "error" : (10, 8, 16, f"{alpha(palette.error.main, 0.24)}"),

        # "primary" : (10, 0, 1, f"{alpha(palette.primary.main, 0.24)}"),
        # "info" : (10, 0, 1, f"{alpha(palette.info.main, 0.24)}"),
        # "secondary" : (10, 0, 1, f"{alpha(palette.secondary.main, 0.24)}"),
        # "success" : (10, 0, 1, f"{alpha(palette.success.main, 0.24)}"),
        # "warning" : (10, 0, 1, f"{alpha(palette.warning.main, 0.24)}"),
        # "error" : (10, 0, 1, f"{alpha(palette.error.main, 0.24)}"),

        "primary" : (10, 0, 1, palette.primary.main),
        "info" : (10, 0, 1, palette.info.main),
        "secondary" : (10, 0, 1, palette.secondary.main),
        "success" : (10, 0, 1, palette.success.main),
        "warning" : (10, 0, 1, palette.warning.main),
        "error" : (10, 0, 1, palette.error.main),

        "card" : (0, 0, 2, 25),
        "dialog" : (10, 40, 80, 25),
        "dropdown" : (0, 0, 1, 25)
    }

    return Shadows(shadows)



