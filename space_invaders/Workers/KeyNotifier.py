import time

from PyQt5.QtCore import QThread, pyqtSignal


class KeyNotifierWorker(QThread):
    key_signal = pyqtSignal(int)
    finished_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.keys = []
        self.is_done = False

    def add_key(self, key):
        self.keys.append(key)

    def rem_key(self, key):
        if key in self.keys:
            self.keys.remove(key)

    def die(self):
        """
        End notifications.
        """
        self.is_done = True
        self.finished_signal.emit()

    def run(self):

        while not self.is_done:
            for k in self.keys:
                self.key_signal.emit(k)
            time.sleep(0.05)