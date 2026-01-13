from PySide6.QtCore import QByteArray
from PySide6.QtGui import QPixmap

def icon_base64_to_pixmap(icon_base64):
    data = QByteArray.fromBase64(icon_base64.encode())
    pixmap = QPixmap()
    pixmap.loadFromData(data)
    return pixmap