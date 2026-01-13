from PySide6.QtCore import QtMsgType # qInstallMessageHandler

def qt_message_handler(mode, context, message):
    if mode == QtMsgType.QtWarningMsg:
        print("⚠️ Qt Warning:", message, context)
    elif mode == QtMsgType.QtCriticalMsg:
        print("❌ Qt Critical:", message)
    elif mode == QtMsgType.QtFatalMsg:
        print("💀 Qt Fatal:", context, message)

# qInstallMessageHandler(qt_message_handler)