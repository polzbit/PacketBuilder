from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot, QRunnable
import traceback, sys

class WorkerSignals(QObject):
    ''' Thread Signals '''
    finished = pyqtSignal(object, object)
    error = pyqtSignal(tuple)

class Worker(QRunnable):
    def __init__(self, name, key, action, callback, main_callback, **kwargs):
        super(Worker, self).__init__()
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self._stop_event = False
        self.name = name
        self.key = key
        self.action = action
        self.callback = callback
        self.main_callback = main_callback

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        # print("[ Thread ] starting " + self.name +" thread")
        # Retrieve args/kwargs here; and fire processing using them
        res = {}
        try:
            res = self.action(self.stopped, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            # Return the result of the processing
            # self.signals.result.emit(result)
            pass
        finally:
            self.main_callback(self, res)  # Done
            

    def stop(self):
        self._stop_event = True

    def stopped(self, pkt=None):
        ''' check if stop is set '''
        return self._stop_event
