# coding:utf-8
from typing import Callable,Optional,Union
from PySide6.QtWidgets import (QLabel, QGraphicsDropShadowEffect, QApplication, QSizePolicy,QWidget, 
                               QFrame,QHBoxLayout, QAbstractItemView, QStyleOptionViewItem,QTableView)
from PySide6.QtCore import QTimer, Qt,QPoint,QRect, QEvent, QObject, QPropertyAnimation, QModelIndex
from PySide6.QtGui import QColor,QCursor, QHelpEvent

from enum import Enum
from qtmui.hooks import State, useEffect
from qtmui.material.styles.create_theme.theme_reducer import ThemeState
from qtmui.material.styles.create_theme.create_palette import PaletteColor

from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from qtmui.i18n.use_translation import translate, i18n


def getCurrentScreen():
    
    """ get current screen """
    cursorPos = QCursor.pos()

    for s in QApplication.screens():
        if s.geometry().contains(cursorPos):
            return s

    return None

def getCurrentScreenGeometry(avaliable=True):
    """ get current screen geometry """
    screen = getCurrentScreen() or QApplication.primaryScreen()
    # this should not happen
    if not screen:
        return QRect(0, 0, 1920, 1080)
    return screen.availableGeometry() if avaliable else screen.geometry()


class ToolTipLabel(QLabel):
    # TOOLTIP / LABEL StyleSheet
    style_tooltip = """ 
    QLabel {{		
        background-color: {backgroundColor};	
        color: {textColor};
        padding-top: 5px;
        padding-bottom: 5px;
        padding-left: 10px;
        padding-right: 10px;
        border-radius: 17px;
        border: 0px solid transparent;
        font: 800 9pt "Segoe UI";
    }}
    """
    def __init__(
        self,
        parent:Optional[Union[str, object]] = None,
        text:str="",
        maxWidth:float=300,
    ):
        super().__init__(parent=parent)

        self._parent:QWidget = parent
        
        self._text = text
        self._maxWidth = maxWidth

        self._init_ui()

    def _init_ui(self):
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self._textColor = "white"
        self._backgroundColor = "black"
        # LABEL SETUP
        self.setObjectName(u"label_tooltip")
        self.setMinimumHeight(34)
        self.setMaximumWidth(self._maxWidth)
        self.setWordWrap(True)
        style = self.style_tooltip.format(
            backgroundColor = self._backgroundColor,
            textColor = self._textColor
        )
        self.setStyleSheet(style)
        # self.setParent(QApplication.instance().mainWindow)
        self.setText(self._text)
        self.adjustSize()

        # SET DROP SHADOW
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(30)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)

        self.shadow.setColor(QColor(0, 0, 0, 80))
        self.setGraphicsEffect(self.shadow)
        # self.hide()

        self.theme = useTheme()
        useEffect(
            self._set_stylesheet,
            [self.theme.state]
        )
        self._set_stylesheet()

        i18n.langChanged.connect(self.reTranslation)
        self.reTranslation()

        self.destroyed.connect(self._on_destroyed)

    def _on_destroyed(self):
        self.theme.state.valueChanged.disconnect(self._set_stylesheet)
        i18n.langChanged.disconnect(self.reTranslation)


    def reTranslation(self):
        if isinstance(self._text, Callable):
            self.setText(translate(self._text))
        else:
            self.setText(self._text)
        self.adjustSize()
         

    def leaveEvent(self, event):
        self.hide()
        super().leaveEvent(event)

    def _set_stylesheet(self, component_styled=None):
        self.theme = useTheme()

        if not component_styled:
            component_styled = self.theme.components

        PyTooltip_qss = get_qss_style(component_styled["PyTooltip"].get("styles")["tooltip"])

        self.setStyleSheet(
            f"""
                QLabel {{		
                    {PyTooltip_qss}
                }}
            """
        )
    
class ToolTipPosition(Enum):
    """ Info bar position """

    TOP = 0
    BOTTOM = 1
    LEFT = 2
    RIGHT = 3
    TOP_LEFT = 4
    TOP_RIGHT = 5
    BOTTOM_LEFT = 6
    BOTTOM_RIGHT = 7
    LEFT_TOP = 8
    LEFT_BOTTOM = 9
    RIGHT_TOP = 10
    RIGHT_BOTTOM = 11



class ItemViewToolTipType(Enum):
    """ Info bar position """

    LIST = 0
    TABLE = 1


class ToolTip(QFrame):
    """
    A tooltip component, styled like Material-UI Tooltip.

    The `Tooltip` component displays a tooltip with customizable content, position, and behavior,
    aligning with MUI Tooltip props. Inherits from native component props.

    Parameters
    ----------
    title : State, str, QWidget, or None, optional
        Content of the tooltip. Default is ''.
        Can be a `State` object for dynamic updates.
    parent : State, QWidget, or None, optional
        Parent widget. Default is None.
        Can be a `State` object for dynamic updates.
    children : State, QWidget, or None, optional
        Reference element for the tooltip (required in MUI). Default is None.
        Can be a `State` object for dynamic updates.
    arrow : State or bool, optional
        If True, adds an arrow to the tooltip. Default is False.
        Can be a `State` object for dynamic updates.
    classes : State or Dict, optional
        Override or extend styles. Default is None.
        Can be a `State` object for dynamic updates.
    components : State or Dict, optional
        Components for slots (Arrow, Popper, Tooltip, Transition, deprecated). Default is None.
        Can be a `State` object for dynamic updates.
    componentsProps : State or Dict, optional
        Props for slot components (deprecated). Default is None.
        Can be a `State` object for dynamic updates.
    describeChild : State or bool, optional
        If True, title is an accessible description. Default is False.
        Can be a `State` object for dynamic updates.
    disableFocusListener : State or bool, optional
        If True, ignores focus events. Default is False.
        Can be a `State` object for dynamic updates.
    disableHoverListener : State or bool, optional
        If True, ignores hover events. Default is False.
        Can be a `State` object for dynamic updates.
    disableInteractive : State or bool, optional
        If True, tooltip is non-interactive. Default is False.
        Can be a `State` object for dynamic updates.
    disableTouchListener : State or bool, optional
        If True, ignores touch events. Default is False.
        Can be a `State` object for dynamic updates.
    enterDelay : State or int, optional
        Delay before showing tooltip (ms). Default is 100.
        Can be a `State` object for dynamic updates.
    enterNextDelay : State or int, optional
        Delay for next tooltip after one closes (ms). Default is 0.
        Can be a `State` object for dynamic updates.
    enterTouchDelay : State or int, optional
        Delay for touch to show tooltip (ms). Default is 700.
        Can be a `State` object for dynamic updates.
    followCursor : State or bool, optional
        If True, tooltip follows cursor. Default is False.
        Can be a `State` object for dynamic updates.
    id : State, str, or None, optional
        ID for accessibility. Default is None.
        Can be a `State` object for dynamic updates.
    leaveDelay : State or int, optional
        Delay before hiding tooltip (ms). Default is 0.
        Can be a `State` object for dynamic updates.
    leaveTouchDelay : State or int, optional
        Delay after touch ends to hide tooltip (ms). Default is 1500.
        Can be a `State` object for dynamic updates.
    onClose : State, Callable, or None, optional
        Callback when tooltip closes. Default is None.
        Can be a `State` object for dynamic updates.
    onOpen : State, Callable, or None, optional
        Callback when tooltip opens. Default is None.
        Can be a `State` object for dynamic updates.
    open : State or bool, optional
        If True, tooltip is shown. Default is False.
        Can be a `State` object for dynamic updates.
    placement : State, str, or None, optional
        Tooltip placement. Default is 'bottom'.
        Can be a `State` object for dynamic updates.
    PopperComponent : State, str, or None, optional
        Component for popper (deprecated). Default is None.
        Can be a `State` object for dynamic updates.
    PopperProps : State or Dict, optional
        Props for popper (deprecated). Default is None.
        Can be a `State` object for dynamic updates.
    slotProps : State or Dict, optional
        Props for slots (arrow, popper, tooltip, transition). Default is None.
        Can be a `State` object for dynamic updates.
    slots : State or Dict, optional
        Components for slots (arrow, popper, tooltip, transition). Default is None.
        Can be a `State` object for dynamic updates.
    sx : State, List, Dict, Callable, or None, optional
        System prop for CSS overrides. Default is None.
        Can be a `State` object for dynamic updates.
    TransitionComponent : State, str, or None, optional
        Component for transition (deprecated). Default is None.
        Can be a `State` object for dynamic updates.
    TransitionProps : State or Dict, optional
        Props for transition (deprecated). Default is None.
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to QFrame, supporting native props.

    Notes
    -----
    - `components`, `componentsProps`, `PopperComponent`, `PopperProps`, `TransitionComponent`, `TransitionProps` are deprecated; use `slotProps` and `slots`.
    - Supports dynamic updates via State objects.
    - MUI classes applied: `MuiTooltip-root`.

    Demos:
    - Tooltip: https://qtmui.com/material-ui/qtmui-tooltip/

    API Reference:
    - Tooltip API: https://qtmui.com/material-ui/api/tooltip/
    """

    def __init__(self, 
                text: Optional[Union[str, State, Callable]] = None,
                 parent=None
                 ):
        """
        Parameters
        ----------
        text: str
            the text of tool tip

        parent: QWidget
            parent widget
        """
        super().__init__(parent=parent)
        self.__text = text
        self.__duration = 1000

        self.container = self._createContainer()
        self.timer = QTimer(self)

        self.setLayout(QHBoxLayout())
        self.containerLayout = QHBoxLayout(self.container)
        # self.label = QLabel(text, self)
        self.label = ToolTipLabel(self,text)

        # set layout
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self.container)
        self.containerLayout.addWidget(self.label)
        self.containerLayout.setContentsMargins(8, 6, 8, 6)

        # add opacity effect
        self.opacityAni = QPropertyAnimation(self, b'windowOpacity', self)
        self.opacityAni.setDuration(150)

        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.hide)

        # set style
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)
        self.__setQss()

    def text(self):
        return self.__text

    def setText(self, text):
        """ set text on tooltip """
        self.__text = text
        self.label.setText(text)
        self.adjustSize()

    def duration(self):
        return self.__duration

    def setDuration(self, duration: int):
        """ set tooltip duration in milliseconds

        Parameters
        ----------
        duration: int
            display duration in milliseconds, if `duration <= 0`, tooltip won't disappear automatically
        """
        self.__duration = duration

    def __setQss(self):
        """ set style sheet """
        # self.container.setObjectName("container")
        self.label.setObjectName("contentLabel")
        self.label.adjustSize()
        self.adjustSize()

    def _createContainer(self):
        return QFrame(self)

    def showEvent(self, e):
        self.opacityAni.setStartValue(0)
        self.opacityAni.setEndValue(1)
        self.opacityAni.start()

        self.timer.stop()
        if self.duration() > 0:
            self.timer.start(self.__duration + self.opacityAni.duration())

        super().showEvent(e)

    def hideEvent(self, e):
        self.timer.stop()
        super().hideEvent(e)

    def adjustPos(self, widget, position: ToolTipPosition):
        """ adjust the position of tooltip relative to widget """
        manager = ToolTipPositionManager.make(position)
        self.move(manager.position(self, widget))


class ToolTipPositionManager:
    """ Tooltip position manager """

    def position(self, tooltip: ToolTip, parent: QWidget) -> QPoint:
        pos = self._pos(tooltip, parent)
        x, y = pos.x(), pos.y()

        rect = getCurrentScreenGeometry()
        x = max(rect.left(), min(pos.x(), rect.right() - tooltip.width() - 4))
        y = max(rect.top(), min(pos.y(), rect.bottom() - tooltip.height() - 4))

        return QPoint(x, y)

    def _pos(self, tooltip: ToolTip, parent: QWidget) -> QPoint:
        raise NotImplementedError

    @staticmethod
    def make(position: ToolTipPosition):
        """ mask info bar manager according to the display position """
        managers = {
            ToolTipPosition.TOP: TopToolTipManager,
            ToolTipPosition.BOTTOM: BottomToolTipManager,
            ToolTipPosition.LEFT: LeftToolTipManager,
            ToolTipPosition.LEFT_TOP: LeftTopToolTipManager,
            ToolTipPosition.LEFT_BOTTOM: LeftBottomToolTipManager,
            ToolTipPosition.RIGHT: RightToolTipManager,
            ToolTipPosition.RIGHT_TOP: RightTopToolTipManager,
            ToolTipPosition.RIGHT_BOTTOM: RightBottomToolTipManager,
            ToolTipPosition.TOP_RIGHT: TopRightToolTipManager,
            ToolTipPosition.BOTTOM_RIGHT: BottomRightToolTipManager,
            ToolTipPosition.TOP_LEFT: TopLeftToolTipManager,
            ToolTipPosition.BOTTOM_LEFT: BottomLeftToolTipManager,
        }

        if position not in managers:
            raise ValueError(f'`{position}` is an invalid info bar position.')

        return managers[position]()


class TopToolTipManager(ToolTipPositionManager):
    """ Top tooltip position manager """

    def _pos(self, tooltip: ToolTip, parent: QWidget):
        pos = parent.mapToGlobal(QPoint())
        x = pos.x() + parent.width()//2 - tooltip.width()//2
        y = pos.y() - tooltip.height()
        return QPoint(x, y)


class BottomToolTipManager(ToolTipPositionManager):
    """ Bottom tooltip position manager """

    def _pos(self, tooltip: ToolTip, parent: QWidget) -> QPoint:
        pos = parent.mapToGlobal(QPoint())
        x = pos.x() + parent.width()//2 - tooltip.width()//2
        y = pos.y() + parent.height()
        return QPoint(x, y)


class LeftToolTipManager(ToolTipPositionManager):
    """ Left tooltip position manager """

    def _pos(self, tooltip: ToolTip, parent: QWidget) -> QPoint:
        pos = parent.mapToGlobal(QPoint())
        x = pos.x() - tooltip.width()
        y = pos.y() + (parent.height() - tooltip.height()) // 2
        return QPoint(x, y)

class LeftTopToolTipManager(ToolTipPositionManager):
    """ Left tooltip position manager """

    def _pos(self, tooltip: ToolTip, parent: QWidget) -> QPoint:
        pos = parent.mapToGlobal(QPoint())
        x = pos.x() - tooltip.width()
        y = pos.y() + parent.height()
        return QPoint(x, y)

class LeftBottomToolTipManager(ToolTipPositionManager):
    """ Left tooltip position manager """

    def _pos(self, tooltip: ToolTip, parent: QWidget) -> QPoint:
        pos = parent.mapToGlobal(QPoint())
        x = pos.x() - tooltip.width()
        y = pos.y() + (parent.height() - tooltip.height())
        return QPoint(x, y)


class RightToolTipManager(ToolTipPositionManager):
    """ Right tooltip position manager """

    def _pos(self, tooltip: ToolTip, parent: QWidget) -> QPoint:
        pos = parent.mapToGlobal(QPoint())
        x = pos.x() + parent.width()
        y = pos.y() + (parent.height() - tooltip.height()) // 2
        return QPoint(x, y)

class RightTopToolTipManager(ToolTipPositionManager):
    """ Right tooltip position manager """

    def _pos(self, tooltip: ToolTip, parent: QWidget) -> QPoint:
        pos = parent.mapToGlobal(QPoint())
        x = pos.x() + parent.width()
        y = pos.y() + parent.height()
        return QPoint(x, y)

class RightBottomToolTipManager(ToolTipPositionManager):
    """ Right tooltip position manager """

    def _pos(self, tooltip: ToolTip, parent: QWidget) -> QPoint:
        pos = parent.mapToGlobal(QPoint())
        x = pos.x() + parent.width()
        y = pos.y() + (parent.height() - tooltip.height())
        return QPoint(x, y)


class TopRightToolTipManager(ToolTipPositionManager):
    """ Top right tooltip position manager """

    def _pos(self, tooltip: ToolTip, parent: QWidget) -> QPoint:
        pos = parent.mapToGlobal(QPoint())
        x = pos.x() + parent.width() - tooltip.width() + \
            tooltip.layout().contentsMargins().right()
        y = pos.y() - tooltip.height()
        return QPoint(x, y)


class TopLeftToolTipManager(ToolTipPositionManager):
    """ Top left tooltip position manager """

    def _pos(self, tooltip: ToolTip, parent: QWidget) -> QPoint:
        pos = parent.mapToGlobal(QPoint())
        x = pos.x() - tooltip.layout().contentsMargins().left()
        y = pos.y() - tooltip.height()
        return QPoint(x, y)


class BottomRightToolTipManager(ToolTipPositionManager):
    """ Bottom right tooltip position manager """

    def _pos(self, tooltip: ToolTip, parent: QWidget) -> QPoint:
        pos = parent.mapToGlobal(QPoint())
        x = pos.x() + parent.width() - tooltip.width() + \
            tooltip.layout().contentsMargins().right()
        y = pos.y() + parent.height()
        return QPoint(x, y)


class BottomLeftToolTipManager(ToolTipPositionManager):
    """ Bottom left tooltip position manager """

    def _pos(self, tooltip: ToolTip, parent: QWidget) -> QPoint:
        pos = parent.mapToGlobal(QPoint())
        x = pos.x() - tooltip.layout().contentsMargins().left()
        y = pos.y() + parent.height()
        return QPoint(x, y)


class ItemViewToolTipManager(ToolTipPositionManager):
    """ Item view tooltip position manager """

    def __init__(self, itemRect=QRect()):
        super().__init__()
        self.itemRect = itemRect

    def _pos(self, tooltip: ToolTip, view: QAbstractItemView) -> QPoint:
        pos = view.mapToGlobal(self.itemRect.topLeft())
        x = pos.x()
        y = pos.y() - tooltip.height() + 10
        return QPoint(x, y)

    @staticmethod
    def make(tipType: ItemViewToolTipType, itemRect: QRect):
        """ mask info bar manager according to the display tipType """
        managers = {
            ItemViewToolTipType.LIST: ItemViewToolTipManager,
            ItemViewToolTipType.TABLE: TableItemToolTipManager,
        }

        if tipType not in managers:
            raise ValueError(f'`{tipType}` is an invalid info bar tipType.')

        return managers[tipType](itemRect)


class TableItemToolTipManager(ItemViewToolTipManager):
    """ Table item view tooltip position manager """

    def _pos(self, tooltip: ToolTip, view: QTableView) -> QPoint:
        pos = view.mapToGlobal(self.itemRect.topLeft())
        x = pos.x() + view.verticalHeader().isVisible() * view.verticalHeader().width()
        y = pos.y() - tooltip.height() + view.horizontalHeader().isVisible() * view.horizontalHeader().height() + 10
        return QPoint(x, y)

class ToolTipFilter(QObject):
    """ Tool button with a tool tip """

    def __init__(self, parent: QWidget, tooltipDelay=300):
        """
        Parameters
        ----------
        parent: QWidget
            the widget to install tool tip

        tooltipDelay: int
            show tool tip after how long the mouse hovers in milliseconds

        position: TooltipPosition
            where to show the tooltip
        """
        super().__init__(parent=parent)
        self._parent = parent
        self.isEnter = False
        self._tooltip = None
        self._tooltipDelay = tooltipDelay
        self.position = self.get_position()
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.showToolTip)
    
    def get_position(self):
        if self._parent._tooltipPlacement == "top-start":
            return ToolTipPosition.TOP_RIGHT
        elif self._parent._tooltipPlacement == "top":
            return ToolTipPosition.TOP
        elif self._parent._tooltipPlacement == "top-end":
            return ToolTipPosition.TOP_LEFT
        elif self._parent._tooltipPlacement == "bottom-start":
            return ToolTipPosition.BOTTOM_RIGHT
        elif self._parent._tooltipPlacement == "bottom":
            return ToolTipPosition.BOTTOM
        elif self._parent._tooltipPlacement == "bottom-end":
            return ToolTipPosition.BOTTOM_LEFT
        elif self._parent._tooltipPlacement == "left-start":
            return ToolTipPosition.LEFT_TOP
        elif self._parent._tooltipPlacement == "left":
            return ToolTipPosition.LEFT
        elif self._parent._tooltipPlacement == "left-end":
            return ToolTipPosition.LEFT_BOTTOM
        elif self._parent._tooltipPlacement == "right-start":
            return ToolTipPosition.RIGHT_TOP
        elif self._parent._tooltipPlacement == "right":
            return ToolTipPosition.RIGHT
        elif self._parent._tooltipPlacement == "right-end":
            return ToolTipPosition.RIGHT_BOTTOM
        else:
            raise TypeError("Type of tooltipPlacement is invalid")
    
    
    def eventFilter(self, obj: QObject, e: QEvent) -> bool:
        if e.type() == QEvent.ToolTip:
            return True
        elif e.type() in [QEvent.Hide, QEvent.Leave]:
            self.hideToolTip()
        elif e.type() == QEvent.Enter:
            self.isEnter = True
            parent = self.parent()  # type: QWidget
            if self._canShowToolTip():
                if self._tooltip is None:
                    self._tooltip = self._createToolTip()

                t = parent.toolTipDuration() if parent.toolTipDuration() > 0 else -1
                self._tooltip.setDuration(t)

                # show the tool tip after delay
                self.timer.start(self._tooltipDelay)
        elif e.type() == QEvent.MouseButtonPress:
            self.hideToolTip()

        return super().eventFilter(obj, e)

    def _createToolTip(self):
        return ToolTip(self.parent().toolTip(), self.parent().window())

    def hideToolTip(self):
        """ hide tool tip """
        self.isEnter = False
        self.timer.stop()
        if self._tooltip:
            self._tooltip.hide()

    def showToolTip(self):
        """ show tool tip """
        if not self.isEnter:
            return

        parent = self.parent()  # type: QWidget
        self._tooltip.setText(parent.toolTip())
        self._tooltip.adjustPos(parent, self.position)
        self._tooltip.show()

    def setToolTipDelay(self, delay: int):
        """ set the delay of tool tip """
        self._tooltipDelay = delay

    def _canShowToolTip(self) -> bool:
        parent = self.parent()  # type: QWidget
        return parent.isWidgetType() and parent.toolTip() and parent.isEnabled()

class ItemViewToolTip(ToolTip):
    """ Item view tool tip """

    def adjustPos(self, view: QAbstractItemView, itemRect: QRect, tooltipType: ItemViewToolTipType):
        manager = ItemViewToolTipManager.make(tooltipType, itemRect)
        self.move(manager.position(self, view))

class ItemViewToolTipDelegate(ToolTipFilter):
    """ Item view tool tip """

    def __init__(self, parent: QAbstractItemView, tooltipDelay=300, tooltipType=ItemViewToolTipType.TABLE):
        super().__init__(parent, tooltipDelay, ToolTipPosition.TOP)
        self.text = ""
        self.currentIndex = None
        self.tooltipDuration = -1
        self.tooltipType = tooltipType
        self.viewport = parent.viewport()

        parent.installEventFilter(self)
        parent.viewport().installEventFilter(self)
        parent.horizontalScrollBar().valueChanged.connect(self.hideToolTip)
        parent.verticalScrollBar().valueChanged.connect(self.hideToolTip)

    def eventFilter(self, obj: QObject, e: QEvent) -> bool:
        if obj is self.parent():
            if e.type() in [QEvent.Type.Hide, QEvent.Type.Leave]:
                self.hideToolTip()
            elif e.type() == QEvent.Type.Enter:
                self.isEnter = True
        elif obj is self.viewport:
            if e.type() == QEvent.Type.MouseButtonPress:
                self.hideToolTip()

        return QObject.eventFilter(self, obj, e)

    def _createToolTip(self):
        return ItemViewToolTip(self.text, self.parent().window())

    def showToolTip(self):
        """ show tool tip """
        if not self._tooltip:
            self._tooltip = self._createToolTip()

        view = self.parent()  # type: QAbstractItemView
        self._tooltip.setText(self.text)

        if self.currentIndex:
            rect = view.visualRect(self.currentIndex)
        else:
            rect = QRect()

        self._tooltip.adjustPos(view, rect, self.tooltipType)
        self._tooltip.show()

    def _canShowToolTip(self) -> bool:
        return True

    def setText(self, text: str):
        self.text = text
        if self._tooltip:
            self._tooltip.setText(text)

    def setToolTipDuration(self, duration):
        self.tooltipDuration = duration
        if self._tooltip:
            self._tooltip.setDuration(duration)

    def helpEvent(self, event: QHelpEvent, view: QAbstractItemView, option: QStyleOptionViewItem, index: QModelIndex) -> bool:
        if not event or not view:
            return False

        if event.type() == QEvent.Type.ToolTip:
            text = index.data(Qt.ItemDataRole.ToolTipRole)
            if not text:
                self.hideToolTip()
                return False
            self.text = text
            self.currentIndex = index
            if not self._tooltip:
                self._tooltip = self._createToolTip()
                self._tooltip.setDuration(self.tooltipDuration)
            # show the tool tip after delay
            self.timer.start(self._tooltipDelay)

        return True




