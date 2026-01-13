from typing import Callable, Dict, Optional, Union
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl, QObject, Slot, QMarginsF, QTimer
from PySide6.QtGui import QAction, QPageLayout, QPageSize
from PySide6.QtWebChannel import QWebChannel
import markdown
import base64, urllib.parse
from PySide6.QtWidgets import QMenu, QApplication, QFileDialog, QMessageBox
import webbrowser, copy
from enum import Enum
from qtmui.hooks import State

# from src.components.site_packages.markdown.extensions.tables


__all__ = ["MarkdownView", "LinkMiddlewarePolicy"]
aboutInformation = """Markdown 0.2
a package based on ..site_packages.qtcompat designed to help you preview Markdown documents.
"""

class LinkMiddlewarePolicy(Enum):
    OpenNewTab = 0
    Open = 1
    OpenNew = 2


class Markdown(QWebEngineView):
    extensions = None
    value = ""

    class LinkMiddleware(QObject):
        policy = None

        @Slot(str)
        def open_external(self, url):
            if url is None:
                return
            if self.policy == LinkMiddlewarePolicy.Open:
                webbrowser.open(url)
            if self.policy == LinkMiddlewarePolicy.OpenNew:
                webbrowser.open_new(url)
            else:
                webbrowser.open_new_tab(url)

    def __init__(
                self, 
                parent=None,
                content: str = None,
                sx: Optional[Union[Callable, str, Dict]]= None,
                ):
        super().__init__(parent=parent)
        self.load(QUrl("qrc:/markdown_view/page.html"))
        self.channel = QWebChannel()
        self.page().setWebChannel(self.channel)
        self.link_middleware = self.LinkMiddleware()
        self.extensions = list()
        self.channel.registerObject("link_middleware", self.link_middleware)
        self.setLinkMiddlewarePolicy(LinkMiddlewarePolicy.OpenNewTab)

        # Sang Pc
        self.setExtensions(["markdown.extensions.tables", "markdown.extensions.extra"])
        self.setLinkMiddlewarePolicy(LinkMiddlewarePolicy.OpenNew)

        if content:
            if isinstance(content, State):
                content.valueChanged.connect(self.setValue)
                self.setValue(content.value)
            elif isinstance(content, str):
                self.setValue(content)


    def setValue(self, value: str):
        self.value = value
        extensions = self.getExtensions()
        body_html = markdown.markdown(value, extensions=extensions)
        bs64 = base64.b64encode(urllib.parse.quote(body_html).encode()).decode()
        self.script = "setValue({});".format(repr(bs64))
        QTimer.singleShot(1000, self._run_script)

    def _run_script(self):
        self.page().runJavaScript(self.script)

    def getValue(self) -> str:
        return self.value

    def contextMenuEvent(self, arg__1) -> None:
        menu = QMenu(self)
        reload_page = QAction("Reload")
        reload_page.triggered.connect(lambda : self.setValue(self.getValue()))
        copy_page = QAction("Copy Source Code")
        def Copy():
            QApplication.clipboard().setText(self.getValue())
            QMessageBox.information(self, "Markdown View", "Source code has been copied to clipboard.")
        copy_page.triggered.connect(Copy)
        pdf_export = QAction("Export to PDF")
        def pdfExport():
            fp = QFileDialog.getSaveFileName(self, "Save PDF...", filter = "PDF(*.pdf)")[0]
            if fp is None or fp == "":
                return
            lay = QPageLayout(QPageSize(QPageSize.PageSizeId.A4), QPageLayout.Orientation.Portrait, QMarginsF())
            self.page().printToPdf(fp, lay)
            QMessageBox.information(self, "Markdown View", "The document has been exported successfully.")
        pdf_export.triggered.connect(pdfExport)
        about = QAction("About")
        about.triggered.connect(lambda : QMessageBox.information(self, "Markdown View", aboutInformation))
        menu.addActions([reload_page, copy_page, pdf_export, about])
        menu.exec(arg__1.globalPos())

    def setLinkMiddlewarePolicy(self, policy) -> None:
        self.link_middleware.policy = policy

    def getLinkMiddlewarePolicy(self):
        return self.link_middleware.policy

    def setExtensions(self, extensions: list[str]) -> None:
        self.extensions = copy.deepcopy(extensions)

    def getExtensions(self) -> list[str]:
        return copy.deepcopy(self.extensions)

    def addExtension(self, extension: str) -> None:
        self.extensions.append(extension)
