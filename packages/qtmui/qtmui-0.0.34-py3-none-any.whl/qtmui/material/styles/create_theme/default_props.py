from typing import TYPE_CHECKING
from ...system.color_manipulator import alpha
# from PySide6.QtSvgWidgets import QSvgWidget

if TYPE_CHECKING:
    from qtmui.material.styles.create_theme.theme_reducer import ThemeState
    

# class ArrowDownIcon(QSvgWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         svg_data = b"""
#             <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24">
#                 <path d="M12,16 C11.7663478,16.0004565 11.5399121,15.9190812 11.36,15.77 L5.36,10.77 
#                 C4.93474074,10.4165378 4.87653776,9.78525926 5.23,9.36 C5.58346224,8.93474074 
#                 6.21474074,8.87653776 6.64,9.23 L12,13.71 L17.36,9.39 C17.5665934,9.2222295 
#                 17.8315409,9.14373108 18.0961825,9.17188444 C18.3608241,9.2000378 18.6033268,9.33252029 
#                 18.77,9.54 C18.9551341,9.74785947 19.0452548,10.0234772 19.0186853,10.3005589 
#                 C18.9921158,10.5776405 18.8512608,10.8311099 18.63,11 L12.63,15.83 
#                 C12.444916,15.955516 12.2231011,16.0153708 12,16 Z" />
#             </svg>
#         """
#         self.load(svg_data)
#         self.setFixedSize(24, 24)


# class CheckboxIcon(QSvgWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         svg_data = b"""
#             <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24">
#                 <path d="M17.9 2.318A5 5 0 0 1 22.895 7.1l.005.217v10a5 5 0 0 1-4.783 4.995l-.217.005h-10a5 5 0 0 1-4.995-4.783l-.005-.217v-10a5 5 0 0 1 4.783-4.996l.217-.004h10Zm-.5 1.5h-9a4 4 0 0 0-4 4v9a4 4 0 0 0 4 4h9a4 4 0 0 0 4-4v-9a4 4 0 0 0-4-4Z" />
#             </svg>
#         """
#         self.load(svg_data)
#         self.setFixedSize(24, 24)


# class CheckboxCheckedIcon(QSvgWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         svg_data = b"""
#             <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24">
#                 <path d="M17 2a5 5 0 0 1 5 5v10a5 5 0 0 1-5 5H7a5 5 0 0 1-5-5V7a5 5 0 0 1 5-5Zm-1.625 7.255-4.13 4.13-1.75-1.75a.881.881 0 0 0-1.24 0c-.34.34-.34.89 0 1.24l2.38 2.37c.17.17.39.25.61.25.23 0 .45-.08.62-.25l4.75-4.75c.34-.34.34-.89 0-1.24a.881.881 0 0 0-1.24 0Z" />
#             </svg>
#         """
#         self.load(svg_data)
#         self.setFixedSize(24, 24)

# Các biểu tượng khác tương tự như vậy...

class Iconify:
    icon: str
    width: int
    def __init__(self, icon=None, width=None):
        pass


def default_props(_theme):
    theme: ThemeState = _theme
    return {
        "PyAlert": {
            "defaultProps": {
                "iconMapping": {
                    "error": 'Iconify(icon="solar:danger-bold", width=24)',
                    "info": 'Iconify(icon="eva:info-fill", width=24)',
                    "success": 'Iconify(icon="eva:checkmark-circle-2-fill", width=24)',
                    "warning": 'Iconify(icon="eva:alert-triangle-fill", width=24)',
                },
            },
        },
        "PyStack": {
            "defaultProps": {
                "useFlexGap": True,
            },
        },
        "PyAppBar": {
            "defaultProps": {
                "color": "transparent",
            },
        },
        "PyAvatarGroup": {
            "defaultProps": {
                "max": 4,
            },
        },
        "MuiButtonGroup": {
            "defaultProps": {
                "disableElevation": True,
            },
        },
        "MuiButton": {
            "defaultProps": {
                "color": "inherit",
                "disableElevation": True,
            },
        },
        "PyCardHeader": {
            "defaultProps": {
                "titleTypographyProps": {"variant": "h6"},
                "subheaderTypographyProps": {
                    "variant": "body2",
                    "marginTop": theme.spacing(0.5),
                },
            },
        },
        "PyChip": {
            "defaultProps": {
                "deleteIcon": 'Iconify(icon="solar:close-circle-bold")',
            },
        },
        "PyDialogActions": {
            "defaultProps": {
                "disableSpacing": True,
            },
        },
        "PyFab": {
            "defaultProps": {
                "color": "primary",
            },
        },
        "PyLink": {
            "defaultProps": {
                "underline": "hover",
            },
        },
        "PyListItemText": {
            "defaultProps": {
                "primaryTypographyProps": {
                    "typography": "subtitle2",
                },
                "secondaryTypographyProps": {
                    "component": "span",
                },
            },
        },
        "PyPaper": {
            "defaultProps": {
                "elevation": 0,
                "background-color": theme.palette.background.neutral
            },
        },
        "PySkeleton": {
            "defaultProps": {
                "animation": "wave",
                "variant": "rounded",
            },
        },
        "MuiFilledInput": {
            "defaultProps": {
                "disableUnderline": True,
            },
        },
        "MuiFormHelperText": {
            "defaultProps": {
                "component": "div",
            },
        },
        "PyTab": {
            "defaultProps": {
                "disableRipple": True,
                "iconPosition": "start",
            },
        },
        "PyTabs": {
            "defaultProps": {
                "textColor": "inherit",
                "variant": "scrollable",
                "allowScrollButtonsMobile": True,
            },
        },
        "PyTablePagination": {
            "defaultProps": {
                "backIconButtonProps": {
                    "size": "small",
                },
                "nextIconButtonProps": {
                    "size": "small",
                },
            },
        },
        "PySlider": {
            "defaultProps": {
                "size": "small",
            },
        },
        "MuiAutocomplete": {
            "defaultProps": {
                "popupIcon": 'ArrowDownIcon()',
            },
        },
        "PySelect": {
            "defaultProps": {
                "IconComponent": 'ArrowDownIcon()',
            },
        },
        "PyNativeSelect": {
            "defaultProps": {
                "IconComponent": 'ArrowDownIcon()',
            },
        },
        "MuiCheckbox": {
            "defaultProps": {
                "size": "small",
                "icon": 'CheckboxIcon()',
                "checkedIcon": 'CheckboxCheckedIcon()',
                "indeterminateIcon": 'CheckboxCheckedIcon()',  # Icon tương tự như checked trong trường hợp này
            },
        },
        "PyRadio": {
            "defaultProps": {
                "size": "small",
                "icon": 'CheckboxIcon()',
                "checkedIcon": 'CheckboxCheckedIcon()',
            },
        },
        "PyRating": {
            "defaultProps": {
                "emptyIcon": 'CheckboxIcon()',
                "icon": 'CheckboxCheckedIcon()',
            },
        },
        "PyTreeView": {
            "defaultProps": {
                "defaultCollapseIcon": 'CheckboxIcon()',
                "defaultExpandIcon": 'CheckboxCheckedIcon()',
                "defaultEndIcon": 'CheckboxCheckedIcon()',
            },
        },
    }
