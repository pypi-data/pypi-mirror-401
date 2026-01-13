# coding:utf-8
from __future__ import annotations
from enum import Enum
from typing import Union, Literal
import warnings
from typing import TYPE_CHECKING

from PySide6.QtXml import QDomDocument
from PySide6.QtCore import QRectF, Qt, QFile, QObject, QRect,QSize
from PySide6.QtGui import QIcon, QIconEngine, QColor, QPixmap, QImage, QPainter, QAction
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QApplication

import random, re


try:
    from pyconify import svg_path
except ModuleNotFoundError:  # pragma: no cover
    raise ModuleNotFoundError(
        "pyconify is required to use Iconify. "
        "Please install it with `pip install pyconify` or use the "
        "`pip install superqt[iconify]` extra."
    ) from None

if TYPE_CHECKING:
    Flip = Literal["horizontal", "vertical", "horizontal,vertical"]
    Rotation = Literal["90", "180", "270", 90, 180, 270, "-90", 1, 2, 3]


class Iconify(QIcon):
    """QIcon backed by an iconify icon.

    Iconify includes 150,000+ icons from most major icon sets including Bootstrap,
    FontAwesome, Material Design, and many more.

    Search availble icons at https://icon-sets.iconify.design
    Once you find one you like, use the key in the format `"prefix:name"` to create an
    icon:  `Iconify("bi:bell")`.

    This class is a thin wrapper around the
    [pyconify](https://github.com/pyapp-kit/pyconify) `svg_path` function. It pulls SVGs
    from iconify, creates a temporary SVG file and uses it as the source for a QIcon.
    SVGs are cached to disk, and persist across sessions (until `pyconify.clear_cache()`
    is called).

    Parameters are the same as `Iconify.addKey`, which can be used to add
    additional icons for various modes and states to the same QIcon.

    Parameters
    ----------
    *key: str
        Icon set prefix and name. May be passed as a single string in the format
        `"prefix:name"` or as two separate strings: `'prefix', 'name'`.
    color : str, optional
        Icon color. If not provided, the icon will appear black (the icon fill color
        will be set to the string "currentColor").
    flip : str, optional
        Flip icon.  Must be one of "horizontal", "vertical", "horizontal,vertical"
    rotate : str | int, optional
        Rotate icon. Must be one of 0, 90, 180, 270,
        or 0, 1, 2, 3 (equivalent to 0, 90, 180, 270, respectively)
    dir : str, optional
        If 'dir' is not None, the file will be created in that directory, otherwise a
        default
        [directory](https://docs.python.org/3/library/tempfile.html#tempfile.mkstemp) is
        used.

    Examples
    --------
    >>> from PySide6.QtWidgets import QPushButton
    >>> from superqt import Iconify
    >>> btn = QPushButton()
    >>> icon = Iconify("bi:alarm-fill", color="red", rotate=90)
    >>> btn.setIcon(icon)
    """

    def __init__(
        self,
        *key: str,
        color: str | None = None,
        flip: Flip | None = None,
        rotate: Rotation | None = None,
        dir: str | None = None,
        size = None,
        mode= QIcon.Mode.Normal,
        state = QIcon.State.Off
    ):
        super().__init__()
        if key:
            self.addKey(*key, 
                        color=color, 
                        flip=flip, 
                        rotate=rotate, 
                        dir=dir,
                        size = size,
                        mode= mode,
                        state = state)

    def addKey(
        self,
        *key: str,
        color: str | None = None,
        flip: Flip | None = None,
        rotate: Rotation | None = None,
        dir: str | None = None,
        size: QSize | None = None,
        mode: QIcon.Mode = QIcon.Mode.Normal,
        state: QIcon.State = QIcon.State.Off,
    ) -> Iconify:
        """Add an icon to this QIcon.

        This is a variant of `QIcon.addFile` that uses an iconify icon keys and
        arguments instead of a file path.

        Parameters
        ----------
        *key: str
            Icon set prefix and name. May be passed as a single string in the format
            `"prefix:name"` or as two separate strings: `'prefix', 'name'`.
        color : str, optional
            Icon color. If not provided, the icon will appear black (the icon fill color
            will be set to the string "currentColor").
        flip : str, optional
            Flip icon.  Must be one of "horizontal", "vertical", "horizontal,vertical"
        rotate : str | int, optional
            Rotate icon. Must be one of 0, 90, 180, 270, or 0, 1, 2, 3 (equivalent to 0,
            90, 180, 270, respectively)
        dir : str, optional
            If 'dir' is not None, the file will be created in that directory, otherwise
            a default
            [directory](https://docs.python.org/3/library/tempfile.html#tempfile.mkstemp)
            is used.
        size : QSize, optional
            Size specified for the icon, passed to `QIcon.addFile`.
        mode : QIcon.Mode, optional
            Mode specified for the icon, passed to `QIcon.addFile`.
        state : QIcon.State, optional
            State specified for the icon, passed to `QIcon.addFile`.

        Returns
        -------
        Iconify
            This Iconify instance, for chaining.
        """
        try:
            path = svg_path(*key, color=color, flip=flip, rotate=rotate, dir=dir)
        except OSError as e:
            warnings.warn(
                f"Error fetching icon: {e}.\nIcon {key} not cached. Using fallback.",
                stacklevel=2,
            )
            self._draw_text_fallback(key)
        else:
            self.addFile(str(path), size or QSize(), mode, state)

        return self

    def _draw_text_fallback(self, key: tuple[str, ...]) -> None:
        if style := QApplication.style():
            pixmap = style.standardPixmap(style.StandardPixmap.SP_MessageBoxQuestion)
        else:
            pixmap = QPixmap(18, 18)
            pixmap.fill(Qt.GlobalColor.transparent)
            painter = QPainter(pixmap)
            painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "?")
            painter.end()

        self.addPixmap(pixmap)


def writeSvg(iconPath: str, indexes=None, **attributes):
    """ write svg with specified attributes

    Parameters
    ----------
    iconPath: str
        svg icon path

    indexes: List[int]
        the path to be filled

    **attributes:
        the attributes of path

    Returns
    -------
    svg: str
        svg code
    """
    if not iconPath.lower().endswith('.svg'):
        return ""

    f = QFile(iconPath)
    f.open(QFile.OpenModeFlag.ReadOnly)

    dom = QDomDocument()
    dom.setContent(f.readAll())

    f.close()

    # change the color of each path
    pathNodes = dom.elementsByTagName('path')
    indexes = range(pathNodes.length()) if not indexes else indexes
    for i in indexes:
        element = pathNodes.at(i).toElement()

        for k, v in attributes.items():
            element.setAttribute(k, v)

    return dom.toString()


def changeSvgFill(iconPath: str, indexes=None, **attributes):
    """ write svg with specified attributes
    Parameters
    ----------
    iconPath: str
        svg icon path

    indexes: List[int]
        the path to be filled

    **attributes:
        the attributes of path

    Returns
    -------
    svg: str
        svg code
    """
    if not iconPath.lower().endswith('.svg'):
        return ""
    f = QFile(iconPath)
    f.open(QFile.OpenModeFlag.ReadOnly)
    dom = QDomDocument()
    dom.setContent(f.readAll())
    f.close()
    _attributes = dom.attributes()
    nodeType = dom.nodeType()
    # tagName = dom.tagName()
    # text = dom.text()
    documentElement = dom.documentElement()

    # change the color of each path
    pathNodes = dom.elementsByTagName('path')
    indexes = range(pathNodes.length()) if not indexes else indexes
    for i in indexes:
        element = pathNodes.at(i).toElement()
        for k, v in attributes.items():
            element.setAttribute(k, v)
    return dom.toString()


def drawSvgIcon(icon, painter, rect):
    """ draw svg icon

    Parameters
    ----------
    icon: str | bytes | QByteArray
        the path or code of svg icon

    painter: QPainter
        painter
    rect: QRect | QRectF
        the rect to render icon
    """
    renderer = QSvgRenderer(icon)
    renderer.setAnimationEnabled(True)
    renderer.render(painter, QRectF(rect))


class SvgIconEngine(QIconEngine):
    """ Svg icon engine """

    def __init__(self, svg: str):
        super().__init__()
        self.svg = svg

    def paint(self, painter, rect, mode, state):
        drawSvgIcon(self.svg.encode(), painter, rect)

    def clone(self) -> QIconEngine:
        return SvgIconEngine(self.svg)

    def pixmap(self, size, mode, state):
        image = QImage(size, QImage.Format.Format_ARGB32)
        image.fill(Qt.GlobalColor.transparent)
        pixmap = QPixmap.fromImage(image, Qt.ImageConversionFlag.NoFormatConversion)

        painter = QPainter(pixmap)
        rect = QRect(0, 0, size.width(), size.height())
        self.paint(painter, rect, mode, state)
        return pixmap


class DrawSVG:
    def path(self) -> str:
        raise NotImplementedError
    def icon(self, path, color: QColor|str = None) -> QIcon:
        """ create a fluent icon
        Parameters
        ----------
        path: str
            path to the svg file
        color: QColor | Qt.GlobalColor | str
            icon color, only applicable to svg icon
        """
        try:
            iconify = Iconify("material-symbols:auto-stories-outline", color="red")
            print(iconify)
            return iconify
        except Exception as e:
            print(e)
        if not (path.endswith('.svg') and color):
            return QIcon(path)
        color = QColor(color).name()
        return QIcon(SvgIconEngine(changeSvgFill(path, {"fill":color})))

    def render(self, painter: QPainter, rect:QRectF|QRect, icon:str, indexes=None, **attributes):
        """ draw svg icon

        Parameters
        ----------
        painter: QPainter
            painter

        rect: QRect | QRectF
            the rect to render icon

        theme: Theme
            the theme of icon
            * `Theme.Light`: black icon
            * `Theme.DARK`: white icon
            * `Theme.AUTO`: icon color depends on `config.theme`

        indexes: List[int]
            the svg path to be modified

        **attributes:
            the attributes of modified path
        """
        if icon.endswith('.svg'):
            if attributes:
                _icon = changeSvgFill(icon, indexes, **attributes).encode()
            drawSvgIcon(_icon, painter, rect)
        else:
            _icon = QIcon(icon)
            rect = QRectF(rect).toRect()
            painter.drawPixmap(rect, _icon.pixmap(QRectF(rect).toRect().size()))

class IconPath(DrawSVG, Enum):
    """ Fluent icon """
    UP = "Up"
    ADD = "Add"
    BUS = "Bus"
    CAR = "Car"
    CUT = "Cut"
    IOT = "IOT"
    PIN = "Pin"
    TAG = "Tag"
    VPN = "VPN"
    CAFE = "Cafe"
    CHAT = "Chat"
    COPY = "Copy"
    CODE = "Code"
    DOWN = "Down"
    EDIT = "Edit"
    FLAG = "Flag"
    FONT = "Font"
    GAME = "Game"
    HELP = "Help"
    HIDE = "Hide"
    HOME = "Home"
    INFO = "Info"
    LEAF = "Leaf"
    LINK = "Link"
    MAIL = "Mail"
    MENU = "Menu"
    MUTE = "Mute"
    MORE = "More"
    MOVE = "Move"
    PLAY = "Play"
    SAVE = "Save"
    SEND = "Send"
    SYNC = "Sync"
    UNIT = "Unit"
    VIEW = "View"
    WIFI = "Wifi"
    ZOOM = "Zoom"
    ALBUM = "Album"
    BRUSH = "Brush"
    BROOM = "Broom"
    CLOSE = "Close"
    CLOUD = "Cloud"
    EMBED = "Embed"
    GLOBE = "Globe"
    HEART = "Heart"
    LABEL = "Label"
    MEDIA = "Media"
    MOVIE = "Movie"
    MUSIC = "Music"
    ROBOT = "Robot"
    PAUSE = "Pause"
    PASTE = "Paste"
    PHOTO = "Photo"
    PHONE = "Phone"
    PRINT = "Print"
    SHARE = "Share"
    TILES = "Tiles"
    UNPIN = "Unpin"
    VIDEO = "Video"
    TRAIN = "Train"
    ADD_TO  ="AddTo"
    ACCEPT = "Accept"
    CAMERA = "Camera"
    CANCEL = "Cancel"
    DELETE = "Delete"
    FOLDER = "Folder"
    FILTER = "Filter"
    MARKET = "Market"
    SCROLL = "Scroll"
    LAYOUT = "Layout"
    GITHUB = "GitHub"
    UPDATE = "Update"
    REMOVE = "Remove"
    RETURN = "Return"
    PEOPLE = "People"
    QRCODE = "QRCode"
    RINGER = "Ringer"
    ROTATE = "Rotate"
    SEARCH = "Search"
    VOLUME = "Volume"
    FRIGID  = "Frigid"
    SAVE_AS = "SaveAs"
    ZOOM_IN = "ZoomIn"
    CONNECT  ="Connect"
    HISTORY = "History"
    SETTING = "Setting"
    PALETTE = "Palette"
    MESSAGE = "Message"
    FIT_PAGE = "FitPage"
    ZOOM_OUT = "ZoomOut"
    AIRPLANE = "Airplane"
    ASTERISK = "Asterisk"
    CALORIES = "Calories"
    CALENDAR = "Calendar"
    FEEDBACK = "Feedback"
    LIBRARY = "BookShelf"
    MINIMIZE = "Minimize"
    CHECKBOX = "CheckBox"
    DOCUMENT = "Document"
    LANGUAGE = "Language"
    DOWNLOAD = "Download"
    QUESTION = "Question"
    SPEAKERS = "Speakers"
    DATE_TIME = "DateTime"
    FONT_SIZE = "FontSize"
    HOME_FILL = "HomeFill"
    PAGE_LEFT = "PageLeft"
    SAVE_COPY = "SaveCopy"
    SEND_FILL = "SendFill"
    SKIP_BACK = "SkipBack"
    SPEED_OFF = "SpeedOff"
    ALIGNMENT = "Alignment"
    BLUETOOTH = "Bluetooth"
    COMPLETED = "Completed"
    CONSTRACT = "Constract"
    HEADPHONE = "Headphone"
    MEGAPHONE = "Megaphone"
    PROJECTOR = "Projector"
    EDUCATION = "Education"
    LEFT_ARROW = "LeftArrow"
    ERASE_TOOL = "EraseTool"
    PAGE_RIGHT = "PageRight"
    PLAY_SOLID = "PlaySolid"
    BOOK_SHELF = "BookShelf"
    HIGHTLIGHT = "Highlight"
    FOLDER_ADD = "FolderAdd"
    PAUSE_BOLD = "PauseBold"
    PENCIL_INK = "PencilInk"
    PIE_SINGLE = "PieSingle"
    QUICK_NOTE = "QuickNote"
    SPEED_HIGH = "SpeedHigh"
    STOP_WATCH = "StopWatch"
    ZIP_FOLDER = "ZipFolder"
    BASKETBALL = "Basketball"
    BRIGHTNESS = "Brightness"
    DICTIONARY = "Dictionary"
    MICROPHONE = "Microphone"
    ARROW_DOWN = "ChevronDown"
    FULL_SCREEN = "FullScreen"
    MIX_VOLUMES = "MixVolumes"
    REMOVE_FROM = "RemoveFrom"
    RIGHT_ARROW = "RightArrow"
    QUIET_HOURS  ="QuietHours"
    FINGERPRINT = "Fingerprint"
    APPLICATION = "Application"
    CERTIFICATE = "Certificate"
    TRANSPARENT = "Transparent"
    IMAGE_EXPORT = "ImageExport"
    SPEED_MEDIUM = "SpeedMedium"
    LIBRARY_FILL = "LibraryFill"
    MUSIC_FOLDER = "MusicFolder"
    POWER_BUTTON = "PowerButton"
    SKIP_FORWARD = "SkipForward"
    CARE_UP_SOLID = "CareUpSolid"
    ACCEPT_MEDIUM = "AcceptMedium"
    CANCEL_MEDIUM = "CancelMedium"
    CHEVRON_RIGHT = "ChevronRight"
    CLIPPING_TOOL = "ClippingTool"
    SEARCH_MIRROR = "SearchMirror"
    SHOPPING_CART = "ShoppingCart"
    FONT_INCREASE = "FontIncrease"
    BACK_TO_WINDOW = "BackToWindow"
    COMMAND_PROMPT = "CommandPrompt"
    CLOUD_DOWNLOAD = "CloudDownload"
    DICTIONARY_ADD = "DictionaryAdd"
    CARE_DOWN_SOLID = "CareDownSolid"
    CARE_LEFT_SOLID = "CareLeftSolid"
    CLEAR_SELECTION = "ClearSelection"
    DEVELOPER_TOOLS = "DeveloperTools"
    BACKGROUND_FILL = "BackgroundColor"
    CARE_RIGHT_SOLID = "CareRightSolid"
    CHEVRON_DOWN_MED = "ChevronDownMed"
    CHEVRON_RIGHT_MED = "ChevronRightMed"
    EMOJI_TAB_SYMBOLS = "EmojiTabSymbols"
    EXPRESSIVE_INPUT_ENTRY = "ExpressiveInputEntry"
    def path(self):
        return f':/qfluentwidgets/images/icons/{self.value}.svg'

class Icon(QIcon):
    def __init__(self, icon_path: IconPath):
        super().__init__(icon_path.path())
        self.icon_path = icon_path


def paintIcon(painter: QPainter, rect:QRectF|QRect, opacity:int=1,**attributes):
    svg = QSvgRenderer()
    svgBytes = changeSvgFill("", **attributes)
    svg.load(svgBytes)
    svg.render(painter, rect)
    painter.setOpacity(opacity)
    svg.setAnimationEnabled(True)

def drawIcon(icon, painter, rect, state=QIcon.State.Off, **attributes):
    """ draw icon
    Parameters
    ----------
    icon: str | QIcon | FluentIconBaseBase
        the icon to be drawn
    painter: QPainter
        painter
    rect: QRect | QRectF
        the rect to render icon
    **attribute:
        the attribute of svg icon
    """
    if isinstance(icon, DrawSVG):
        icon.render(painter, rect, **attributes)
    elif isinstance(icon, Icon):
        icon.icon_path.render(painter, rect, **attributes)
    else:
        icon = QIcon(icon)
        icon.paint(painter, QRectF(rect).toRect(), Qt.AlignmentFlag.AlignCenter, state=state)
