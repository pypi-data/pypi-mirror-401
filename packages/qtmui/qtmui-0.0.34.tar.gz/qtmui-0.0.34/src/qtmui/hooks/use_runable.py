import traceback, sys
from PySide6.QtCore import Signal, QObject, QRunnable, Slot

class Signals(QObject):
    loading = Signal()
    error = Signal(object)
    result = Signal(object)
    finished = Signal()


class useRunnable(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(useRunnable, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = Signals()

    @Slot()
    def run(self):
        try:
            self.signals.loading.emit()
            result = self.fn(*self.args, **self.kwargs)
        except Exception as e:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit({f"Opp! error at {str(self.fn.__name__)} {str(e)}"})
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()
