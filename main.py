import sys
import httpimport
from PyQt5.QtWidgets import QDialog, QLineEdit, QLabel, QApplication, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class SetupDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.url = ""
        self.mod = ""

        self.setWindowTitle("DynPy Setup")
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()

        layout = QGridLayout()
        icon = QLabel()
        icon.setPixmap(QPixmap("./icon_128.png"))
        self.path = QLineEdit()
        self.server_url = "http://0.0.0.0:8000"
        self.path.setText(self.server_url)

        self.module = QLineEdit()
        self.module.setText("test_package")

        use = QPushButton("Use")
        use.setDefault(True)
        cancel = QPushButton("Cancel")
        hbox.addStretch()
        hbox.addWidget(cancel)
        hbox.addWidget(use)
        layout.addWidget(icon, 0, 0, 4, 1)
        layout.addWidget(QLabel("DynPy is about to setup your application."), 0, 1, 1, 2, Qt.AlignTop)
        layout.addWidget(QLabel("Please enter the url of your http server and"),1, 1, 1, 2, Qt.AlignTop)
        layout.addWidget(QLabel("a modulename for yor python file to be loaded."), 2, 1, 1, 2, Qt.AlignTop)
        layout.setRowStretch(3, 1)
        layout.addWidget(QLabel("Http Server Url"), 4, 0)
        layout.addWidget(self.path, 4, 1)
        layout.addWidget(QLabel("Module Name"), 5, 0)
        layout.addWidget(self.module, 5, 1)
        layout.addLayout(hbox, 6, 0, 1, 2)
        self.setLayout(layout)

        use.clicked.connect(self.useClicked)
        cancel.clicked.connect(self.cancelClicked)


    def useClicked(self):
        self.url = self.path.text()
        self.mod = self.module.text()
        self.close()

    def cancelClicked(self):
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlg = SetupDialog()
    dlg.exec()

    if dlg.url:
        url = dlg.url
        mod = dlg.mod
        if mod.endswith(".py"):
            mod = mod[0:-3]
        app.exit()

        # use only for localhost
        httpimport.INSECURE = True

        with httpimport.remote_repo([mod], url):
            import test_package