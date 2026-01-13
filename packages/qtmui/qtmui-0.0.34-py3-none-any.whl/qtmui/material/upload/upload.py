import uuid
from typing import Callable, Union, Optional


from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy, QVBoxLayout, QLabel, QFileDialog, QFrame
from PySide6.QtCore import Qt, QSize, QFile
from PySide6.QtGui import QIcon, QCursor, QMouseEvent

from qtmui.hooks import useEffect
from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from ..system.color_manipulator import alpha

from ..button.button import Button
from ..typography import Typography
from ..button.icon_button import IconButton
from ..py_iconify import PyIconify, Iconify
from ..py_svg_widget import PySvgWidget
from ...qtmui_assets import QTMUI_ASSETS


class Upload(QFrame):
# class Chip(QWidget):
    """
    Button
    Base Chip

    Args:
        key?: 'filled' | 'outlined' | 'outlined' | 'soft'
        severity?: str = 'info' | 'success' | 'warning' | 'error'
        variant?: 'filled' | 'outlined' | 'outlined' | 'soft'
        size?: str = 'small' | 'medium' | 'large'
        sx: str = QSS string
            {
                color: red;
                backroud: none;
            }
        justifyContent: "space-around" | "space-between" | "space-evenly" | "stretch" | "center" | "end" | "flex-end" | "flex-start" | "start"

    Returns:
        new instance of Button
    """
    def __init__(self,
                accept: Optional[Union[list, str]] = None,
                error: Optional[str] = None,
                multiple: bool = None,
                helperText: Optional[str] = None,
                thumbnail: Union[str, bool] = None,
                files: Optional[Union[list, object]] = None,
                onDrop:Callable = None,
                onRemove:Callable = None,
                onRemoveAll:Callable = None,
                onUpload:Callable = None,
                 *args, 
                 **kwargs
                 ):
        super(Upload, self).__init__( *args, **kwargs)
        self.setObjectName(str(uuid.uuid4()))

        self._multiple = multiple
        self._thumbnail = thumbnail
        self._files = files
        self._onDrop = onDrop
        self._onRemove = onRemove
        self._onRemoveAll = onRemoveAll
        self._onUpload = onUpload

        self.theme = useTheme()
        
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        self.setCursor(QCursor(Qt.PointingHandCursor))

        self.frm_content = QFrame()
        self.vlo_frm_content = QVBoxLayout(self.frm_content)

        self.frm_drop_area = QWidget(self)
        self.frm_drop_area.mousePressEvent = self._frmDropPressEvent
        self.frm_drop_area.setObjectName(str(uuid.uuid4()))
        self.vlo_frm_drop_area = QVBoxLayout(self.frm_drop_area)
        self.frm_drop_area.setLayout(self.vlo_frm_drop_area)

        self.btn_icon_upload = QPushButton()
        # self.btn_icon_upload.setLayout(QVBoxLayout())
        # self.btn_icon_upload.layout().addWidget(PySvgWidget(key=ASSETS.ICONS.CLOUD_UPLOAD_BOLD, color=useTheme().palette.primary.main, size=QSize(200, 200)))
        self.btn_icon_upload.clicked.connect(self.open_file)
        self.btn_icon_upload.setStyleSheet('background: none; border: none;')
        self.btn_icon_upload.setIcon(PyIconify(key=QTMUI_ASSETS.ICONS.CLOUD_UPLOAD_BOLD, color=useTheme().palette.primary.main, size=QSize(200, 200)))
        # self.btn_icon_upload.setFixedSize(QSize(200, 200))
        self.btn_icon_upload.setIconSize(QSize(150, 150))
        self.vlo_frm_drop_area.addWidget(self.btn_icon_upload)

        # title
        self.lbl_title = Typography(text="Drop or Select file", variant="h6")
        self.lbl_title.setAlignment(Qt.AlignCenter)
        self.vlo_frm_drop_area.addWidget(self.lbl_title)

        # description
        self.frm_description = QFrame()
        self.hlo_frm_description = QHBoxLayout(self.frm_description)
        self.btn_browser = QPushButton("browser")
        self.btn_browser.clicked.connect(self.open_file)
        self.hlo_frm_description.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.hlo_frm_description.addWidget(QLabel("Drop files here or click"))
        self.hlo_frm_description.addWidget(self.btn_browser)
        self.hlo_frm_description.addWidget(QLabel("thorough your machine"))
        self.hlo_frm_description.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.vlo_frm_drop_area.addWidget(self.frm_description)

        self.frm_action = QFrame()
        self.frm_action.hide()
        self.hlo_frm_action = QHBoxLayout(self.frm_action)
        self.hlo_frm_action.setContentsMargins(0,9,0,9)

        self.hlo_frm_action.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.hlo_frm_action.addWidget(
            Button(text="Remove All", variant="outlined")
        )
        self.hlo_frm_action.addWidget(
            Button(text="Upload", startIcon=":/baseline/resource_qtmui/baseline/cloud_upload.svg", variant="contained")
        )

        self.vlo_frm_content.addWidget(self.frm_drop_area)
        self.vlo_frm_content.addWidget(self.frm_action)

        self.layout().addWidget(self.frm_content)


        theme = useTheme()
        useEffect(
            self._set_stylesheet,
            [theme.state]
        )
        self._set_stylesheet()

    def _set_stylesheet(self):
        theme = useTheme()
        component_styles = theme.components

        PyUpload_root = component_styles[f"PyUpload"].get("styles")["root"]
        PyUpload_root_qss = get_qss_style(PyUpload_root)
        # print(PyUpload_root_qss)

        # self.btn_browser.setStyleSheet(f"background: none; border: none;color: {self.theme.palette.primary.main};")
        self.btn_browser.setStyleSheet(f"background: none; border: none;color: {theme.palette.primary.main};")

        self.frm_description.setStyleSheet(
            f"""
                QWidget {{
                    color: {theme.palette.text.secondary};
                }}
            """
        )
        self.frm_drop_area.setStyleSheet(
            f"""
                #{self.frm_drop_area.objectName()} {{
                    {PyUpload_root_qss}
                }}
            """
        )
        self.frm_content.setStyleSheet(
            f"""
                #frm_file_info {{
                    border: 1px solid {alpha(theme.palette.grey._500, 0.24)}; 
                    border-radius: 8px;
                }}
                #lbl_file_title_upload {{
                    font-size: 13px; font-weight: bold;color: {useTheme().palette.text.primary};
                }}
                #lbl_file_size_upload {{
                    font-size: 12px; font-weight: bold;color: {useTheme().palette.text.secondary};
                }}
            """
        )
        # self.frm_drop_area.setStyleSheet('#frm_drop_area {border: 1px dashed #ccc; border-radius: 10px; background-color: #f9f9f9;}')


    def _frmDropPressEvent(self, event: QMouseEvent) -> None:
        self.open_file()

    def renderMultiPreview(self, file, file_name, file_size):
        frm_file_info = QWidget()
        frm_file_info.setObjectName('frm_file_info')

        hlo_frm_file_info = QHBoxLayout(frm_file_info)
        hlo_frm_file_info.setContentsMargins(0,0,0,0)

        frm_file_info.data = file

        frm_left_info = QFrame()
        hlo_frm_left_info = QHBoxLayout(frm_left_info)
        btn_icon = QPushButton()
        btn_icon.setStyleSheet('border: none;background: none;')
        btn_icon.setIcon(PyIconify(key=QTMUI_ASSETS.ICONS.UPLOAD_FILE, color=useTheme().palette.primary.main))
        btn_icon.setIconSize(QSize(64, 64))
        hlo_frm_left_info.addWidget(btn_icon)

        frm_info = QFrame()
        vlo_frm_info = QVBoxLayout(frm_info)
        lbl_title = QLabel(file_name)
        lbl_title.setObjectName("lbl_file_title_upload")
        lbl_size = QLabel(str(file_size))
        lbl_size.setObjectName("lbl_file_size_upload")
        vlo_frm_info.addWidget(lbl_title)
        vlo_frm_info.addWidget(lbl_size)
        hlo_frm_left_info.addWidget(frm_info)

        frm_right_info = QFrame()
        vlo_frm_right_info = QHBoxLayout(frm_right_info)
        vlo_frm_right_info.addWidget(IconButton(
                onClick=lambda f=frm_file_info: self.removeSinglePreview(f),
                edge="end",
                size="small",
                icon=Iconify(key=QTMUI_ASSETS.ICONS.CLOSE)
            ))
        

        hlo_frm_file_info.addWidget(frm_left_info)
        hlo_frm_file_info.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        hlo_frm_file_info.addWidget(frm_right_info)

        self.vlo_frm_content.insertWidget(self.vlo_frm_content.count() - 1, frm_file_info)

        if isinstance(self._files, list) and len(self._files):
            self.frm_action.show()
        else:
            self.frm_action.hide()

    def removeSinglePreview(self, frm_file_info):
        print(frm_file_info.data)
        print(self._files)
        if frm_file_info.data in self._files:
            self._files.remove(frm_file_info.data)

        self.vlo_frm_drop_area.removeWidget(frm_file_info)
        frm_file_info.deleteLater()

        if isinstance(self._files, list) and len(self._files):
            self.frm_action.show()
        else:
            self.frm_action.hide()

    def open_file(self):
        # filename = QFileDialog.getOpenFileName(self, 'Open File', '.', "Archive (*.zip)")
        # filename = QFileDialog.getOpenFileName(self, 'Open File', '.', "Image files (*.jpg *.jpeg *.png)")
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)")

        _file_name = file_name.split('/')[-1]

        if file_name:
            file = QFile(_file_name)
            file_size = file.size()
            self._files.append([file_name, file_size])

            file_size_str = self.format_size(file_size)
            self.renderMultiPreview([file_name, file_size], _file_name, file_size_str)
            # if file.open(QIODevice.ReadOnly):
            #     file_size = file.size()
            #     file_size_kb = file_size / 1024
            #     self.renderMultiPreview(file_name, file_size)
            #     file.close()


    def format_size(self, bytes):
        """
        Hàm này nhận đầu vào là số byte và trả về chuỗi định dạng kích thước tương ứng
        dưới dạng byte, KB, MB hoặc GB.
        """
        if bytes < 1024:
            return f"{bytes} B"
        elif bytes < 1024**2:
            kb = bytes / 1024
            return f"{kb:.2f} KB"
        elif bytes < 1024**3:
            mb = bytes / 1024**2
            return f"{mb:.2f} MB"
        else:
            gb = bytes / 1024**3
            return f"{gb:.2f} GB"
