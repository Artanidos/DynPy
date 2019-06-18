import sys
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QUrl


def loaded(object, url):
    if not object:
        print("Error loading:", url)
        sys.exit(-1)

app = QGuiApplication(sys.argv)
engine = QQmlApplicationEngine()
engine.load(QUrl("https://github.com/Artanidos/DynPy/raw/master/server/view.qml"))
engine.objectCreated.connect(loaded)
sys.exit(app.exec_())
    
