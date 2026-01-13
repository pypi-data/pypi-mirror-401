# coding:utf-8
from __future__ import annotations
from typing import Any, Optional, Dict, Callable, Union, Literal
from enum import Enum
import uuid
import warnings
import os
from typing import TYPE_CHECKING

import asyncio

from qtmui.hooks.use_runable import useRunnable
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from ..widget_base.widget_base import PyWidgetBase

# from assets import ASSETS

from PySide6.QtXml import QDomDocument
from PySide6.QtCore import QRectF, Qt, QFile, QSize, QByteArray, QThreadPool, QTimer, QPoint, QEvent
from PySide6.QtGui import QIcon, QColor, QPixmap, QImage, QPainter, QPalette
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QApplication, QSizePolicy, QFrame, QHBoxLayout
from PySide6.QtSvgWidgets import QSvgWidget

from qtmui.material.styles import useTheme
from qtmui.hooks import useEffect

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


class PySvgWidget(QSvgWidget, PyWidgetBase):
    """QIcon backed by an iconify icon.

    Iconify includes 150,000+ icons from most major icon sets including Bootstrap,
    FontAwesome, Material Design, and many more.

    Search availble icons at https://icon-sets.iconify.design
    Once you find one you like, use the key in the format `"prefix:name"` to create an
    icon:  `PySvgWidget("bi:bell")`.

    Parameters
    ----------
    key : str
        Icon set prefix and name. May be passed as a single string in the format
        `"prefix:name"` or as two separate strings: `'prefix', 'name'`.
    color : str, optional
        Icon color. If not provided, the icon will appear black (or theme-based).
    flip : Flip, optional
        Flip icon.  Must be one of "horizontal", "vertical", "horizontal,vertical".
    rotate : Rotation, optional
        Rotate icon. Must be one of 0, 90, 180, 270, or 0, 1, 2, 3 (equivalent to 0, 90, 180, 270).
    dir : str, optional
        Nếu không None, tệp SVG sẽ được tạo trong thư mục này, ngược lại dùng thư mục tạm mặc định.
    size : QSize, optional
        Kích thước của icon, mặc định là QSize(16,16).
    width : Optional[Union[str,int]], optional
        Chiều rộng của widget. Nếu là int sẽ gọi setFixedWidth; nếu là str (ví dụ "100%") thì không áp dụng.
    height : Optional[Union[str,int]], optional
        Chiều cao của widget. Tương tự như width.
    viewBox : Optional[str], optional
        Giá trị viewBox sẽ được gán cho phần tử SVG nếu được cung cấp.
    svgContent : Optional[str], optional
        Nếu truyền vào, đây là nội dung SVG (chuỗi) để hiển thị. Nếu có, bỏ qua việc tải từ iconify.
    mode : QIcon.Mode, optional
        Chế độ của icon, mặc định là QIcon.Mode.Normal.
    state : QIcon.State, optional
        Trạng thái của icon, mặc định là QIcon.State.Off.
    sx : Optional[Union[Callable, str, Dict]], optional
        Tham số tùy chọn khác.

    Examples
    --------
    from qtmui.material.py_svg_widget import PySvgWidget
    from qtmui.material.styles import useTheme

    def BookingIllustration():
        theme = useTheme()
        PRIMARY_MAIN = theme.palette.primary.main
        return PySvgWidget(
            key="custom:booking",
            width="100%",
            height="100%",
            viewBox="0 0 200 200",
            svgContent=f\"\"\"
              <path fill="#FFFFFF" d="M141.968 167.139H48.764a11.932 ... z" />
              <path fill={PRIMARY_MAIN} d="M122.521 99.123h-62.5a1.986 ... z" />
              ... (các path khác) ...
            \"\"\"
        )
    """

    def __init__(
        self,
        key: str = None,
        color: Optional[str] = None,
        flip: Optional[Flip] = None,
        rotate: Optional[Rotation] = None,
        dir: Optional[str] = None,
        fill: Optional[str] = None,
        active: Optional[bool] = None,
        size: QSize = QSize(16, 16),
        width: Optional[Union[str, int]] = None,
        height: Optional[Union[str, int]] = None,
        viewBox: Optional[str] = None,
        svgContent: Optional[str] = None,
        xmlns: Optional[str] = None,
        mode= QIcon.Mode.Normal,
        state= QIcon.State.Off,
        sx: Optional[Union[Callable, str, Dict]] = None,
        **kwargs
    ):
        super().__init__()
        self.setObjectName(str(uuid.uuid4()))

        self.kwargs = kwargs

        self._key = key
        self._color = color
        self._flip = flip
        self._rotate = rotate
        self._dir = dir
        self._size = size
        self._mode = mode
        self._state = state
        self._xmlns = xmlns
        self._sx = sx

        # Lưu thêm các tham số mới
        self._width = width
        self._height = height
        self._viewBox = viewBox
        self._svgContent = svgContent
        
        self._use_runable = True

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        
        self._thread_pool = QThreadPool.globalInstance()  # Sử dụng thread pool toàn cục
        
        self.theme = useTheme()
        
        useEffect(
            self._setup_ui,
            [self.theme.state]
        )
        

        
        self._setup_ui()
        

    def _setup_ui(self):
        
        # Lấy màu từ theme nếu cần
        if self._color and '.' in self._color:
            self._color = self._get_theme_color(self._color)
        
        self.theme = useTheme()

        if self._size:
            if isinstance(self._size, QSize):
                self.setFixedSize(self._size)
            elif isinstance(self._size, int):
                self.setFixedSize(QSize(self._size, self._size))

        # Nếu width/height là số, đặt kích thước cố định
        if isinstance(self._width, int):
            if isinstance(self._height, int):
                self.setFixedHeight(self._height)
            else:
                self.setFixedSize(self._width, self._width)
                
        # Nếu _width hoặc _height là chuỗi (ví dụ "100%"), bạn có thể xử lý theo CSS hoặc layout riêng.

        if self._width == "100%" and self._height == "100%":
            self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            QTimer.singleShot(100, lambda: asyncio.ensure_future(self._set_size_from_parent()))

        if self._key:
            self.addKey()

        elif self._svgContent:
            if self._svgContent.find("</svg>") == -1:
                self._svgContent = f"""
                <svg width="{self._width or 24}" height="{self._height or 24}" viewBox="{self._viewBox or "0 0 24 24"}" fill="none" xmlns="{self._xmlns or "http://www.w3.org/2000/svg"}">
                    {self._svgContent}
                </svg>
                """
            self.addKey()
            
        # if self._svgContent:
        #     if self._svgContent.find("</svg>") == -1:
        #         self._svgContent = f"""
        #         <svg width="{self._width or 24}" height="{self._height or 24}" viewBox="{self._viewBox or "0 0 24 24"}" fill="none" xmlns="{self._xmlns or "http://www.w3.org/2000/svg"}">
        #             {self._svgContent}
        #         </svg>
        #         """
        #     self.addKey()
        
        self._set_stylesheet()
        

    def addKey(self) -> PySvgWidget:
        """Add an icon to this widget.
        Nếu có svgContent được truyền vào, sử dụng nội dung đó để hiển thị,
        ngược lại nếu key là resource key thì xử lý tương ứng, nếu không thì tải qua svg_path.
        """
        
        if self._svgContent:
            self._svg_content_to_byte_array(self._svgContent)
        elif self._key is not None and self._is_resource_key(self._key):
            self._path_to_svg_content(self._key)
        else:
            if self._use_runable:
                worker = useRunnable(lambda: svg_path(self._key, color=self._color, dir=self._dir, rotate=self._rotate))
                worker.signals.result.connect(self._path_to_svg_content)
                worker.signals.error.connect(self._draw_text_fallback)
                self._thread_pool.start(worker)
            else:
                try:
                    self._path = svg_path(self._key, color=self._color, dir=self._dir)
                except OSError as e:
                    warnings.warn(
                        f"Error fetching icon: {e}.\nIcon {self._key} not cached. Using fallback.",
                        stacklevel=2,
                    )
                    self._draw_text_fallback(self._key)
                else:
                    self._path_to_svg_content(path=self._path)

    def _is_resource_key(self, key: str) -> bool:
        pattern = r"^:/[a-zA-Z0-9_-]+(/[a-zA-Z0-9_-]+)*\.[a-zA-Z]+$"
        return bool(re.match(pattern, key))

    def _path_to_svg_content(self, path: Union[str, os.PathLike]):
        """
        Cập nhật tệp SVG từ đường dẫn (path) để thiết lập màu sắc, xoay, lật...
        """
        path = str(path)

        # Nếu path là resource key của Qt
        if path.startswith(":/"):
            svg_file = QFile(path)
            if not svg_file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
                warnings.warn(f"Không thể mở tệp SVG tài nguyên: {path}")
                return ""
            svg_content = svg_file.readAll().data().decode('utf-8')
            svg_file.close()
        else:
            if not os.path.exists(path) or not path.endswith(".svg"):
                warnings.warn(f"Đường dẫn tệp SVG không hợp lệ: {path}")
                return ""
            with open(path, "r", encoding="utf-8") as file:
                svg_content = file.read()

        self._svg_content_to_byte_array(svg_content)


    def _svg_content_to_byte_array(self, svg_content: str):
        # Phân tích nội dung SVG
        dom = QDomDocument()
        if not dom.setContent(svg_content):
            warnings.warn("Không thể phân tích nội dung SVG.")
            return ""

        # Lấy màu từ theme nếu cần
        if self._color:
            if '.' in self._color:
                color = QColor(self._get_theme_color(self._color))
            else:
                color = QColor(self._color)

            # Thay đổi thuộc tính fill cho các thẻ path
            path_elements = dom.elementsByTagName("path")
            for i in range(path_elements.length()):
                element = path_elements.item(i).toElement()
                element.setAttribute("fill", color.name())

        data = QByteArray(dom.toString().encode('utf-8'))

        # Nếu SVG có animation, sử dụng renderer với FPS cao
        if "<animate" in svg_content or "<animateTransform" in svg_content:
            self._renderer = self.renderer()
            self._renderer.setFramesPerSecond(60)
            self._renderer.load(data)
        else:
            # Với SVG tĩnh, tải dữ liệu vào widget qua load()
            self.load(data)


    def _get_theme_color(self, value):
        if isinstance(value, str) and (
            value.startswith("text.") 
            or value.startswith("background.")
            or value.startswith("primary.")
            or value.startswith("secondary.")
            or value.startswith("info.")
            or value.startswith("warning.")
            or value.startswith("error.")
            ):
            value = f"palette.{value}"
        try:
            props = value.split('.')
            theme_value = self.theme
            for prop in props:
                theme_value = getattr(theme_value, prop)
            value = theme_value
        except AttributeError:
            raise ValueError(f"Invalid theme property: {value}")
        return value

    def _draw_text_fallback(self, key: tuple[str, ...]=None) -> None:
        svg_content = f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="{useTheme().palette.info.main}" d="M15.312 7.96q0-1.402-.944-2.254t-2.483-.852q-.994 0-1.736.39q-.741.389-1.282 1.2q-.169.229-.433.288q-.265.058-.476-.103q-.177-.133-.215-.348q-.037-.215.084-.41q.723-1.104 1.73-1.641t2.328-.538q2.04 0 3.331 1.183q1.292 1.183 1.292 3.062q0 1.048-.456 1.957q-.456.91-1.423 1.77q-1.175 1.028-1.615 1.727q-.441.7-.464 1.555q-.023.254-.195.423q-.172.17-.42.17t-.42-.176t-.173-.424q0-1.033.493-1.884q.492-.851 1.646-1.866q1.025-.895 1.428-1.632q.403-.738.403-1.597M11.885 21q-.402 0-.701-.299q-.3-.299-.3-.701t.3-.701t.7-.299t.702.299t.299.701t-.3.701t-.7.299"/></svg>
        """
        self.load(QByteArray(svg_content))
        
        # if style := QApplication.style():
        #     pixmap = style.standardPixmap(style.StandardPixmap.SP_MessageBoxQuestion)
        # else:
        #     pixmap = QPixmap(18, 18)
        #     pixmap.fill(Qt.GlobalColor.transparent)
        #     painter = QPainter(pixmap)
        #     painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "?")
        #     painter.end()
        

    def changeEvent(self, event: QEvent):
        if event.type() == event.Type.StyleChange:
            color = self.palette().color(QPalette.ColorRole.ButtonText)
            if hasattr(self, "_key") and self._key:
                if hasattr(self, "_colorChanged") and self._colorChanged:
                    self._color = color.name()
                    self._colorChanged = False
                self.addKey()
        super().changeEvent(event)
        

    def _set_text_color(self, color):
        self._colorChanged = True
        new_stylesheet = f"""
            #{self.objectName()} {{
                color: {color};
            }}
        """
        self.setStyleSheet(self.styleSheet() + new_stylesheet)

    async def _set_size_from_parent(self):
        self._width = self.parent().width()
        self._height = self.parent().height()
        self._setup_ui()
        self.move(QPoint(0,0))

    def _set_stylesheet(self, component_styled=None):
        self.theme = useTheme()

        ownerState = {}

        if not component_styled:
            component_styled = self.theme.components

        ownerState = {
            **self.kwargs
        }

        PySvgWidget_root = component_styled[f"PySvgWidget"].get("styles")["root"](ownerState)
        PySvgWidget_root_qss = get_qss_style(PySvgWidget_root)
        
        sx_qss = ""
        if self._sx:
            if isinstance(self._sx, dict):
                sx_qss = get_qss_style(self._sx, class_name=f"#{self.objectName()}")
            elif isinstance(self._sx, Callable):
                sx = self._sx()
                if isinstance(sx, dict):
                    sx_qss = get_qss_style(sx, class_name=f"#{self.objectName()}")
                elif isinstance(sx, str):
                    sx_qss = sx
            elif isinstance(self._sx, str) and self._sx != "":
                sx_qss = self._sx


        stylesheet = f"""
                #{self.objectName()} {{
                    {PySvgWidget_root_qss}
                }}

                {sx_qss}

            """
        self.setStyleSheet(stylesheet) 
