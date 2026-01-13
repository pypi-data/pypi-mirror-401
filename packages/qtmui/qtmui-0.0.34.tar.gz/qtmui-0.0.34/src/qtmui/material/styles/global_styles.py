from qtmui.material.styles import useTheme

theme = useTheme()

FONT_PRIMARY='Public Sans, sans-serif'
FONT_WEIGHT_REGULAR = 400,

GLOBAL_STYLES = f"""
/* /////////////////////////////////////////////////////////////////////////////////////////////////
QWidget */

QWidget {{
    background-color: transparent;
    border: none;
    font-family: "{FONT_PRIMARY}";
    font-weight: {FONT_WEIGHT_REGULAR};
}}

QDialog {{
    background-color: #ffffff;
    border: 1px solid #DFE3E8;
    font-family: "{FONT_PRIMARY}";
    font-weight: {FONT_WEIGHT_REGULAR};
}}

/* /////////////////////////////////////////////////////////////////////////////////////////////////
ScrollBars */

QScrollBar:horizontal {{
    border: none;
    background: rgb(249, 249, 249);
    height: 4px;
    margin: 0px 21px 0 21px;
    border-radius: 0px;
}}

QScrollBar::handle:horizontal {{
    background: rgb(166, 166, 166);
    min-width: 25px;
    border-radius: 0px
}}

QScrollBar::add-line:horizontal {{
    border: none;
    background: transparent;
    width: 20px;
    border-top-right-radius: 0px;
    border-bottom-right-radius: 0px;
    subcontrol-position: right;
    subcontrol-origin: margin;
}}

QScrollBar::sub-line:horizontal {{
    border: none;
    background: transparent;
    width: 20px;
    border-top-left-radius: 0px;
    border-bottom-left-radius: 0px;
    subcontrol-position: left;
    subcontrol-origin: margin;
}}

QScrollBar::up-arrow:horizontal,
QScrollBar::down-arrow:horizontal {{
    background: none;
}}

QScrollBar::add-page:horizontal,
QScrollBar::sub-page:horizontal {{
    background: none;
}}

QScrollBar:vertical {{
    border: none;
    background: rgb(249, 249, 249);
    width: 4px;
    margin: 21px 0 21px 0;
    border-radius: 0px;
}}

QScrollBar::handle:vertical {{
    background: rgb(166, 166, 166);
    min-height: 25px;
    border-radius: 0px;
}}


QScrollBar::add-line:vertical {{
    border: none;
    background: transparent;
    height: 20px;
    border-bottom-left-radius: 0px; 
    border-bottom-right-radius: 0px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}}

QScrollBar::sub-line:vertical {{
    border: none;
    background: transparent;
    height: 20px;
    border-top-left-radius: 0px;
    border-top-right-radius: 0px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}}

QScrollBar::up-arrow:vertical,
QScrollBar::down-arrow:vertical {{
    background: none;
}}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {{
    background: none;
}}

/* /////////////////////////////////////////////////////////////////////////////////////////////////
QTabWidget

QTabWidget::pane{{
border: 1px solid {theme.palette.background.paper};
top:-1px;
background: {theme.palette.background.paper};
}}

QTabBar::tab{{
background: transparent;
border: 1px solid {theme.palette.background.paper};
padding: 15px;
}}

QTabBar::tab:selected{{
background: {theme.palette.secondary.main};
margin-bottom: -1px;
}}


 */
"""


