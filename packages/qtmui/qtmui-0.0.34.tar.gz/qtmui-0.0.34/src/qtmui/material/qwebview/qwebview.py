from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings, QWebEnginePage
from PySide6.QtCore import QUrl, Slot, Qt

class SmoothYouTubeWidget(QWidget):
    def __init__(self, video_id: str, theme_bg: str = "red"):
        super().__init__()
        self.video_id = video_id
        self.theme_bg = theme_bg

        self.webview = QWebEngineView(self)
        self.webview.setVisible(False)  # ẩn ban đầu

        # set styleSheet cho widget webview để background trước khi load
        self.webview.setStyleSheet(f"background-color: {self.theme_bg};")

        # Pre-load dummy để “khởi động” engine
        dummy = QWebEngineView(self)
        dummy.setAttribute(Qt.WidgetAttribute.WA_DontShowOnScreen, True)
        dummy.settings().setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, True)
        dummy.settings().setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        dummy.settings().setAttribute(QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, True)
        # dummy.setStyleSheet(f"background-color: red;")
        dummy.load(QUrl("about:blank"))
        # dummy.deleteLater()  # sau vài giây, có thể xoá

        # thiết lập background color của page nếu có hỗ trợ
        page = self.webview.page()
        try:
            page.setBackgroundColor(self.theme_bg)  # nếu Qt hỗ trợ
        except Exception:
            pass

        s = self.webview.settings()
        s.setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, True)
        s.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        s.setAttribute(QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, True)

        self.webview.loadStarted.connect(self._on_load_started)
        self.webview.loadProgress.connect(self._on_load_progress)
        self.webview.loadFinished.connect(self._on_load_finished)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.webview)
        self.setLayout(layout)

        embed_html = f"""
<html>
  <head>
    <style>body{{ margin:0; background-color:{self.theme_bg}; overflow:hidden; }}</style>
  </head>
  <body>
    <iframe src="https://www.youtube.com/embed/{video_id}?autoplay=1" 
      frameborder="0" allow="autoplay; fullscreen" 
      style="position:absolute; top:0; left:0; width:100%; height:100%;"></iframe>
  </body>
</html>
"""
        # load HTML embed ngay từ đầu
        self.webview.setHtml(embed_html, QUrl("https://www.youtube.com/"))

    @Slot()
    def _on_load_started(self):
        # có thể show khi bắt đầu load
        self.webview.setVisible(True)

    @Slot(int)
    def _on_load_progress(self, progress):
        # chờ tới khi render thực tế một phần nào đó
        if progress > 5 and not self.webview.isVisible():
            self.webview.setVisible(True)

    @Slot(bool)
    def _on_load_finished(self, ok):
        if not ok:
            # nếu load thất bại
            pass
        # khi load xong thì chắc chắn visible rồi

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    w = SmoothYouTubeWidget("UUDPegNLWSM", theme_bg="#1a1a1a")
    w.resize(800,600)
    w.show()
    sys.exit(app.exec())
