import sys
import json
import traceback
from PySide6.QtCore import QObject, QRunnable, Signal, Slot
from PySide6.QtCore import QObject, Signal, Slot

from qtmui.hooks import useState

# Định nghĩa các tín hiệu cho worker
class Signals(QObject):
    loading = Signal(dict)
    error = Signal(dict)
    result = Signal(dict)
    finished = Signal(dict)


# Worker để thực hiện request
class useSWR(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(useSWR, self).__init__()
        # self.setAutoDelete(False)  # giữ sống tới khi cleanup
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = Signals()

        # self.signals.loading.connect(lambda data: print("Loading...", data))
        # self.signals.error.connect(lambda data: print("Error:", data))
        # self.signals.result.connect(lambda data: print("Result:", data))
        # self.signals.finished.connect(lambda data: print("Finished:", data))

    @Slot()
    def run(self):
        try:
            self.signals.loading.emit({'loading': True})
            result = self.fn(*self.args, **self.kwargs)
        except Exception as e:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit({"error": f"Bad request: {str(self.fn)}"})
        else:

            if isinstance(result, str):
                self.signals.error.emit(result)
            elif result.get("status") == "error":
                self.signals.error.emit(result)
            elif result.get("status") == "success":
                self.signals.result.emit(result)
        finally:
            self.signals.finished.emit({'finished': True})

