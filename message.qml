import QtQuick 2.2
import QtQuick.Dialogs 1.1

MessageDialog {
    id: messageDialog
    title: "DynPy"
    text: message
    onAccepted: {
        Qt.quit()
    }
    Component.onCompleted: visible = true
}