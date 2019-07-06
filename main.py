import sys
import os
import traceback
import lib.main_rc
import lib.httpimport
from PyQt5.QtCore import QUrl, QSettings, QObject, pyqtSlot, pyqtProperty
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine


class Controller(QObject):
    def __init__(self):
        QObject.__init__(self)

    @pyqtSlot("QString", "QString")
    def save(self, url , mod):
        writeSettings(url, mod)

    @pyqtProperty('QString')
    def ip(self):
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip


def readSettings():
    settings = QSettings(QSettings.IniFormat, QSettings.UserScope, "Artanidos", "DynPy")   
    url = settings.value("url")
    mod = settings.value("mod")
    return url, mod
    
def writeSettings(url, mod):
    settings = QSettings(QSettings.IniFormat, QSettings.UserScope, "Artanidos", "DynPy")
    settings.setValue("url", url)
    settings.setValue("mod", mod)


def showError(message):
    writeSettings("", "")
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("message", message)
    engine.load(QUrl("qrc:/message.qml"))
    sys.exit(app.exec())

def start_server(path, port=8000):
    '''Start a simple webserver serving path on port'''
    os.chdir(path)
    httpd = HTTPServer(('', port), CGIHTTPRequestHandler)
    httpd.serve_forever()


if __name__ == "__main__":
    url, mod = readSettings()
    if url and mod:
        try:
            # use only for localhost
            # in production use ssl via https://...
            #lib.httpimport.INSECURE = True
            #lib.httpimport.load(mod, url)
            from lib.httpimport import github_repo
            with github_repo( 'Artanidos', 'DynPy', ) :
                import server.test_package

        except ValueError:
            #message = "Unable to load package[" + mod + "] from [" + url + "]\n" + traceback.format_exc()
            message = traceback.format_exc()
            showError(message)
        except ImportError:
            #message = "Unable to load package[" + mod + "] from [" + url + "]\n" + traceback.format_exc()
            message = traceback.format_exc()
            showError(message)
    else:
        from http.server import HTTPServer, CGIHTTPRequestHandler
        import threading

        # Start the server in a new thread
        port = 8000
        daemon = threading.Thread(name='daemon_server', target=start_server, args=('.', port))
        daemon.setDaemon(True)
        daemon.start()

        controller = Controller()
        app = QGuiApplication(sys.argv)
        engine = QQmlApplicationEngine()
        engine.rootContext().setContextProperty("controller", controller)
        engine.addImportPath("qrc:/")
        engine.load(QUrl("qrc:/main.qml"))
        sys.exit(app.exec())
