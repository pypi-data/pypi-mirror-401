import os
import sys
from typing import Any, Callable, Dict, Optional, Union
import uuid

from PySide6.QtWidgets import QTextEdit, QMainWindow, QVBoxLayout, QFrame, QStatusBar, QToolBar, QFileDialog, QComboBox, QFontComboBox, QMessageBox
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QImage, QTextDocument, QAction, QFont, QKeySequence, QActionGroup
from PySide6.QtPrintSupport import QPrintDialog


from ..system.color_manipulator import alpha

from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style

from qtmui.hooks import useEffect
from qtmui.material.styles import useTheme
from qtmui.i18n.use_translation import translate, i18n

from ..py_iconify import PyIconify
from ...qtmui_assets import QTMUI_ASSETS

FONT_SIZES = [7, 8, 9, 10, 11, 12, 13, 14, 18, 24, 36, 48, 64, 72, 96, 144, 288]
IMAGE_EXTENSIONS = ['.jpg','.png','.bmp']
HTML_EXTENSIONS = ['.htm', '.html']

def hexuuid():
    return uuid.uuid4().hex

def splitext(p):
    return os.path.splitext(p)[1].lower()

class TextEdit(QTextEdit):

    def canInsertFromMimeData(self, source):

        if source.hasImage():
            return True
        else:
            return super(TextEdit, self).canInsertFromMimeData(source)

    def insertFromMimeData(self, source):

        cursor = self.textCursor()
        document = self.document()

        if source.hasUrls():

            for u in source.urls():
                file_ext = splitext(str(u.toLocalFile()))
                if u.isLocalFile() and file_ext in IMAGE_EXTENSIONS:
                    image = QImage(u.toLocalFile())
                    document.addResource(QTextDocument.ImageResource, u, image)
                    cursor.insertImage(u.toLocalFile())

                else:
                    # If we hit a non-image or non-local URL break the loop and fall out
                    # to the super call & let Qt handle it
                    break

            else:
                # If all were valid images, finish here.
                return


        elif source.hasImage():
            image = source.imageData()
            uuid = hexuuid()
            document.addResource(QTextDocument.ImageResource, uuid, image)
            cursor.insertImage(uuid)
            return

        super(TextEdit, self).insertFromMimeData(source)


class Editor(QMainWindow):

    def __init__(
            self, 
            id: Optional[str] = None, 
            placeholder: Optional[str] = None, 
            value: Optional[Any] = None, 
            onChange: Optional[Callable] = None, 
            simple: Optional[bool] = None, 
            sx: Optional[Union[Callable, str, Dict]]= None,
            *args, 
            **kwargs
        ):
        super(Editor, self).__init__(*args, **kwargs)

        self.onChange = onChange
        self.simple = simple

        self.setObjectName(str(uuid.uuid4()))

        layout = QVBoxLayout()
        layout.setContentsMargins(2,2,2,2)
        self.editor = TextEdit()
        self.editor.setPlaceholderText("Write something awesome...")
        self.editor.setObjectName(str(uuid.uuid4()))
        # Setup the QTextEdit editor configuration
        self.editor.setAutoFormatting(QTextEdit.AutoAll)
        self.editor.selectionChanged.connect(self.update_format)
        # Initialize default font size.
        font = QFont('Times', 12)
        self.editor.setFont(font)
        # We need to repeat the size to init the current format.
        self.editor.setFontPointSize(12)

        # self.path holds the path of the currently open file.
        # If none, we haven't got a file open yet (or creating new).
        self.path = None

        layout.addWidget(self.editor)

        self.container = QFrame(self)
        self.container.setObjectName(str(uuid.uuid4()))
        self.container.setLayout(layout)
        self.setCentralWidget(self.container)

        self.status = QStatusBar()
        # self.setStatusBar(self.status)

        # Uncomment to disable native menubar on Mac
        # self.menuBar().setNativeMenuBar(False)

        file_toolbar = QToolBar("Fileee")
        file_toolbar.setIconSize(QSize(14, 14))
        self.addToolBar(file_toolbar)
        # file_menu = self.menuBar().addMenu("&Fileee")

        open_file_action = QAction(PyIconify(key=QTMUI_ASSETS.ICONS.FILE_OPEN), "Open file...", self)

        open_file_action.setStatusTip("Open file")
        open_file_action.triggered.connect(self.file_open)
        # file_menu.addAction(open_file_action)
        file_toolbar.addAction(open_file_action)

        save_file_action = QAction(PyIconify(key=QTMUI_ASSETS.ICONS.FILE_SAVE), "Save", self)

        save_file_action.setStatusTip("Save current page")
        save_file_action.triggered.connect(self.file_save)
        # file_menu.addAction(save_file_action)
        file_toolbar.addAction(save_file_action)

        saveas_file_action = QAction(PyIconify(key=QTMUI_ASSETS.ICONS.FILE_SAVE_AS), "Save As...", self)
        saveas_file_action.setStatusTip("Save current page to specified file")
        saveas_file_action.triggered.connect(self.file_saveas)
        # file_menu.addAction(saveas_file_action)
        file_toolbar.addAction(saveas_file_action)

        print_action = QAction(PyIconify(key=QTMUI_ASSETS.ICONS.PRINT), "Print...", self)
        print_action.setStatusTip("Print current page")
        print_action.triggered.connect(self.file_print)
        # file_menu.addAction(print_action)
        file_toolbar.addAction(print_action)

        edit_toolbar = QToolBar("Edit")
        edit_toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(edit_toolbar)
        # edit_menu = self.menuBar().addMenu("&Edit")

        undo_action = QAction(PyIconify(key=QTMUI_ASSETS.ICONS.UNDO), "Undo", self)
        undo_action.setStatusTip("Undo last change")
        undo_action.triggered.connect(self.editor.undo)
        # edit_menu.addAction(undo_action)

        redo_action = QAction(PyIconify(key=QTMUI_ASSETS.ICONS.REDO), "Redo", self)
        redo_action.setStatusTip("Redo last change")
        redo_action.triggered.connect(self.editor.redo)
        edit_toolbar.addAction(redo_action)
        # edit_menu.addAction(redo_action)

        # edit_menu.addSeparator()

        cut_action = QAction(PyIconify(key=QTMUI_ASSETS.ICONS.CONTENT_CUT), "Cut", self)
        cut_action.setStatusTip("Cut selected text")
        cut_action.setShortcut(QKeySequence.Cut)
        cut_action.triggered.connect(self.editor.cut)
        edit_toolbar.addAction(cut_action)
        # edit_menu.addAction(cut_action)

        copy_action = QAction(PyIconify(key=QTMUI_ASSETS.ICONS.CONTENT_COPY), "Copy", self)
        copy_action.setStatusTip("Copy selected text")
        cut_action.setShortcut(QKeySequence.Copy)
        copy_action.triggered.connect(self.editor.copy)
        edit_toolbar.addAction(copy_action)
        # edit_menu.addAction(copy_action)

        paste_action = QAction(PyIconify(key=QTMUI_ASSETS.ICONS.CONTENT_PASTE), "Paste", self)
        paste_action.setStatusTip("Paste from clipboard")
        cut_action.setShortcut(QKeySequence.Paste)
        paste_action.triggered.connect(self.editor.paste)
        edit_toolbar.addAction(paste_action)
        # edit_menu.addAction(paste_action)

        select_action = QAction(PyIconify(key=QTMUI_ASSETS.ICONS.SELECT_ALL), "Select all", self)
        select_action.setStatusTip("Select all text")
        cut_action.setShortcut(QKeySequence.SelectAll)
        select_action.triggered.connect(self.editor.selectAll)
        # edit_menu.addAction(select_action)

        # edit_menu.addSeparator()

        wrap_action = QAction(PyIconify(key=QTMUI_ASSETS.ICONS.WRAP_TEXT), "Wrap text to window", self)
        wrap_action.setStatusTip("Toggle wrap text to window")
        wrap_action.setCheckable(True)
        wrap_action.setChecked(True)
        wrap_action.triggered.connect(self.edit_toggle_wrap)
        # edit_menu.addAction(wrap_action)

        format_toolbar = QToolBar("Format")
        format_toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(format_toolbar)
        # format_menu = self.menuBar().addMenu("&Format")

        # We need references to these actions/settings to update as selection changes, so attach to self.
        self.fonts = QFontComboBox(self)
        self.fonts.currentFontChanged.connect(self.editor.setCurrentFont)
        format_toolbar.addWidget(self.fonts)

        self.fontsize = QComboBox(self)
        self.fontsize.addItems([str(s) for s in FONT_SIZES])

        # Connect to the signal producing the text of the current selection. Convert the string to float
        # and set as the pointsize. We could also use the index + retrieve from FONT_SIZES.
        # self.fontsize.currentIndexChanged[str].connect(lambda s: self.editor.setFontPointSize(float(s)) )
        self.fontsize.currentIndexChanged.connect(lambda i: self.editor.setFontPointSize(float(self.fontsize.itemText(i))))

        format_toolbar.addWidget(self.fontsize)

        self.bold_action = QAction(PyIconify(key=QTMUI_ASSETS.ICONS.FORMAT_BOLD), "Bold", self)
        self.bold_action.setStatusTip("Bold")
        self.bold_action.setShortcut(QKeySequence.Bold)
        self.bold_action.setCheckable(True)
        self.bold_action.toggled.connect(lambda x: self.editor.setFontWeight(QFont.Bold if x else QFont.Normal))
        format_toolbar.addAction(self.bold_action)
        # format_menu.addAction(self.bold_action)

        self.italic_action = QAction(PyIconify(key=QTMUI_ASSETS.ICONS.FORMAT_ITALIC), "Italic", self)
        self.italic_action.setStatusTip("Italic")
        self.italic_action.setShortcut(QKeySequence.Italic)
        self.italic_action.setCheckable(True)
        self.italic_action.toggled.connect(self.editor.setFontItalic)
        format_toolbar.addAction(self.italic_action)
        # format_menu.addAction(self.italic_action)

        self.underline_action = QAction(PyIconify(key=QTMUI_ASSETS.ICONS.FORMAT_UNDERLINED), "Underline", self)
        self.underline_action.setStatusTip("Underline")
        self.underline_action.setShortcut(QKeySequence.Underline)
        self.underline_action.setCheckable(True)
        self.underline_action.toggled.connect(self.editor.setFontUnderline)
        format_toolbar.addAction(self.underline_action)
        # format_menu.addAction(self.underline_action)

        # format_menu.addSeparator()

        self.alignl_action = QAction(PyIconify(key=QTMUI_ASSETS.ICONS.FORMAT_ALIGN_LEFT), "Align left", self)
        self.alignl_action.setStatusTip("Align text left")
        self.alignl_action.setCheckable(True)
        self.alignl_action.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignLeft))
        format_toolbar.addAction(self.alignl_action)
        # format_menu.addAction(self.alignl_action)

        self.alignc_action = QAction(PyIconify(key=QTMUI_ASSETS.ICONS.FORMAT_ALIGN_CENTER), "Align center", self)
        self.alignc_action.setStatusTip("Align text center")
        self.alignc_action.setCheckable(True)
        self.alignc_action.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignCenter))
        format_toolbar.addAction(self.alignc_action)
        # format_menu.addAction(self.alignc_action)

        self.alignr_action = QAction(PyIconify(key=QTMUI_ASSETS.ICONS.FORMAT_ALIGN_RIGHT), "Align right", self)
        self.alignr_action.setStatusTip("Align text right")
        self.alignr_action.setCheckable(True)
        self.alignr_action.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignRight))
        format_toolbar.addAction(self.alignr_action)
        # format_menu.addAction(self.alignr_action)

        self.alignj_action = QAction(PyIconify(key=QTMUI_ASSETS.ICONS.FORMAT_ALIGN_JUSTIFY), "Justify", self)
        self.alignj_action.setStatusTip("Justify text")
        self.alignj_action.setCheckable(True)
        self.alignj_action.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignJustify))
        format_toolbar.addAction(self.alignj_action)
        # format_menu.addAction(self.alignj_action)

        format_group = QActionGroup(self)
        format_group.setExclusive(True)
        format_group.addAction(self.alignl_action)
        format_group.addAction(self.alignc_action)
        format_group.addAction(self.alignr_action)
        format_group.addAction(self.alignj_action)

        # format_menu.addSeparator()

        # A list of all format-related widgets/actions, so we can disable/enable signals when updating.
        self._format_actions = [
            self.fonts,
            self.fontsize,
            self.bold_action,
            self.italic_action,
            self.underline_action,
            # We don't need to disable signals for alignment, as they are paragraph-wide.
        ]

        # Initialize.
        self.update_format()
        self.update_title()
        # self.show()


        theme = useTheme()
        useEffect(
            self._set_stylesheet,
            [theme.state]
        )
        self._set_stylesheet()

    def _set_stylesheet(self):
        theme = useTheme()
        component_styles = theme.components

        # PyEditor_root = component_styles[f"PyEditor"].get("styles")["root"]
        # PyEditor_root_qss = get_qss_style(PyEditor_root)

        # PyEditor
        # self.setStyleSheet(
        #     f"""
        #         #{self.objectName()} {{
        #             border: 1px solid {theme.palette.grey._500};
        #             border-radius: 8px;
        #         }}
        #     """
        # )

        self.setStyleSheet(
            f"""
                #{self.objectName()} {{
                    border: 1px solid {alpha(theme.palette.grey._500, 0.24)};
                    border-radius: 4px;
                }}

                QToolBar {{
                    border-left: 8px solid transparent;
                }}

                QComboBox {{
                    border: none;
                    background-color: transparent;
                    border-radius: 0px;
                    color: {theme.palette.text.primary};
                }}

                QComboBox:hover {{
                    border: none;
                    background-color: transparent;
                }}

                QComboBox QAbstractItemView {{
                    color: {theme.palette.text.primary};
                    selection-color: {theme.palette.action.selected};
                    background-color:  {theme.palette.background.paper};
                    selection-background-color: {theme.palette.action.selected};
                }}

                QComboBox:item:selected {{
                    background-color: {theme.palette.primary.main};
                    color: {theme.palette.text.primary};
                }}

            """
        )

        self.editor.setStyleSheet(
            f"""
                #{self.editor.objectName()} {{
                    border-top: 1px solid {alpha(theme.palette.grey._500, 0.24)};
                    background-color: {theme.palette.background.paper};
                    color: {theme.palette.text.secondary};
                    font-size: 12px;
                    font-weight: {theme.typography.body2.fontWeight};
                    line-height: {theme.typography.body2.lineHeight};
                }}
            """
        )


    def block_signals(self, objects, b):
        for o in objects:
            o.blockSignals(b)

    def update_format(self):
        """
        Update the font format toolbar/actions when a new text selection is made. This is neccessary to keep
        toolbars/etc. in sync with the current edit state.
        :return:
        """
        # Disable signals for all format widgets, so changing values here does not trigger further formatting.
        self.block_signals(self._format_actions, True)

        self.fonts.setCurrentFont(self.editor.currentFont())
        # Nasty, but we get the font-size as a float but want it was an int
        self.fontsize.setCurrentText(str(int(self.editor.fontPointSize())))

        self.italic_action.setChecked(self.editor.fontItalic())
        self.underline_action.setChecked(self.editor.fontUnderline())
        self.bold_action.setChecked(self.editor.fontWeight() == QFont.Bold)

        self.alignl_action.setChecked(self.editor.alignment() == Qt.AlignLeft)
        self.alignc_action.setChecked(self.editor.alignment() == Qt.AlignCenter)
        self.alignr_action.setChecked(self.editor.alignment() == Qt.AlignRight)
        self.alignj_action.setChecked(self.editor.alignment() == Qt.AlignJustify)

        self.block_signals(self._format_actions, False)

    def dialog_critical(self, s):
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()

    def file_open(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "HTML documents (*.html);Text documents (*.txt);All files (*.*)")

        try:
            with open(path, 'rU') as f:
                text = f.read()

        except Exception as e:
            self.dialog_critical(str(e))

        else:
            self.path = path
            # Qt will automatically try and guess the format as txt/html
            self.editor.setText(text)
            self.update_title()

    def file_save(self):
        if self.path is None:
            # If we do not have a path, we need to use Save As.
            return self.file_saveas()

        text = self.editor.toHtml() if splitext(self.path) in HTML_EXTENSIONS else self.editor.toPlainText()

        try:
            with open(self.path, 'w') as f:
                f.write(text)

        except Exception as e:
            self.dialog_critical(str(e))

    def file_saveas(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "HTML documents (*.html);Text documents (*.txt);All files (*.*)")

        if not path:
            # If dialog is cancelled, will return ''
            return

        text = self.editor.toHtml() if splitext(path) in HTML_EXTENSIONS else self.editor.toPlainText()

        try:
            with open(path, 'w') as f:
                f.write(text)

        except Exception as e:
            self.dialog_critical(str(e))

        else:
            self.path = path
            self.update_title()

    def file_print(self):
        dlg = QPrintDialog()
        if dlg.exec_():
            self.editor.print_(dlg.printer())

    def update_title(self):
        self.setWindowTitle("%s - Megasolid Idiom" % (os.path.basename(self.path) if self.path else "Untitled"))

    def edit_toggle_wrap(self):
        self.editor.setLineWrapMode( 1 if self.editor.lineWrapMode() == 0 else 0 )


