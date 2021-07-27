from threads.qt_thread import Worker
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThreadPool,QRunnable

class QThreadManager:
    def __init__(self, master):
        self.master = master
        self.threadpool = QThreadPool()
        self.threads = []
        self.threadpool.setMaxThreadCount(10)
        # print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

    def _generate_key(self, index=0):
        index += 1
        key = f'thread_{str(index)}'
        for t in self.threads:
            if key == t.key:
                key = self._generate_key(index)
                break
        return key

    def _create(self, name, action, callback=None, **kwargs):
        ''' create and append new thread to list '''
        key = self._generate_key()
        worker = Worker(name, key, action, callback, self._callback, **kwargs) # Any other args, kwargs are passed to the run function
        #worker.signals.finished.connect(self._callback)
        self.threads.append(worker)
        return self.threads[-1]

    def _callback(self, thread, res):
        ''' on thread finish remove form list '''
        if thread.callback != None:
            thread.callback(res)
        self.threads.remove(thread)

    def _get(self, name):
        ''' get list of threads by name '''
        threads = []
        for t in self.threads:
            if t.name == name:
                threads.append(t)
        return threads
    
    def _get_by_key(self, key):
        ''' get thread by key '''
        for t in self.threads:
            if t.key == key:
                return t

    def _start(self, name, action, callback=None, **kwargs):
        ''' create and start new thread '''
        w = self._create(name, action, callback, **kwargs)
        self.threadpool.start(w)
        return w

    def _remove(self, name):
        ''' remove all threads by name '''
        threads = self._get(name)
        for t in threads:
            t.stop()

    def _exist(self, name):
        ''' check if thread already exist in list '''
        threads = self._get(name)
        return len(threads) > 0
                                
    def _clear(self):
        ''' stop and clear all threads '''
        for t in self.threads:
            t.stop()
        self.threadpool.waitForDone()
        
