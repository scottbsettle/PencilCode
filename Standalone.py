# browser using PySide from https://gist.github.com/mmolero/9d8326367c4657f73a3b6d565206a3e4

import sys
import os
import ctypes

from PySide.QtGui import *
from PySide.QtCore import *
from cefpython3 import cefpython

# open server


os.system("python pythonHTTPServer.py")


class CefWidget(QWidget):
    browser = None

    def __init__(self, parent=None):
        super(CefWidget, self).__init__(parent)
        self.show()

    def embed(self):
        # it needs to be called after setupping the layout,
        windowInfo = cefpython.WindowInfo()
        windowInfo.SetAsChild(int(self.winIdFixed()))
        self.browser = cefpython.CreateBrowserSync(windowInfo,
                                                   browserSettings={},
                                                   navigateUrl="http://127.0.0.1:8000/content/welcome.html")

    def winIdFixed(self):
        # PySide bug: QWidget.winId() returns <PyCObject object at 0x02FD8788>,
        # there is no easy way to convert it to int.
        try:
            return int(self.winId())
        except:
            if sys.version_info[0] == 2:
                ctypes.pythonapi.PyCObject_AsVoidPtr.restype = ctypes.c_void_p
                ctypes.pythonapi.PyCObject_AsVoidPtr.argtypes = [ctypes.py_object]
                return ctypes.pythonapi.PyCObject_AsVoidPtr(self.winId())
            elif sys.version_info[0] == 3:
                ctypes.pythonapi.PyCapsule_GetPointer.restype = ctypes.c_void_p
                ctypes.pythonapi.PyCapsule_GetPointer.argtypes = [ctypes.py_object]
                return ctypes.pythonapi.PyCapsule_GetPointer(self.winId(), None)

    def moveEvent(self, event):
        cefpython.WindowUtils.OnSize(int(self.winIdFixed()), 0, 0, 0)

    def resizeEvent(self, event):
        cefpython.WindowUtils.OnSize(int(self.winIdFixed()), 0, 0, 0)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setGeometry(150, 150, 800, 800)

        self.view = CefWidget(self)

        m_vbox = QVBoxLayout()
        m_label = QLabel("Pencil Code")
        m_label.setMaximumHeight(0)

        m_vbox = QVBoxLayout()
        m_vbox.addWidget(m_label)
        m_vbox.addWidget(self.view)

        # Do not use it
        # m_vbox.insertStretch(-1, 1)

        frame = QFrame()
        frame.setLayout(m_vbox)
        self.setCentralWidget(frame)

        # it needs to be called after setupping the layout
        self.view.embed()


class CefApplication(QApplication):
    timer = None

    def __init__(self, args):
        super(CefApplication, self).__init__(args)
        self.createTimer()

    def createTimer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.onTimer)
        self.timer.start(10)

    def onTimer(self):
        cefpython.MessageLoopWork()

    def stopTimer(self):
        # Stop the timer after Qt message loop ended, calls to MessageLoopWork()
        # should not happen anymore.
        self.timer.stop()


if __name__ == "__main__":

    settings = {}
    settings["browser_subprocess_path"] = "%s/%s" % (
        cefpython.GetModuleDirectory(), "subprocess")
    settings["context_menu"] = {
        "enabled": False,
        "navigation": False,  # Back, Forward, Reload
        "print": False,
        "view_source": False,
        "external_browser": False,  # Open in external browser
        "devtools": False,  # Developer Tools
    }

    cefpython.Initialize(settings)

    app = CefApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec_()
    app.stopTimer()
    del win
    del app
    cefpython.Shutdown()