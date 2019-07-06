import QtQuick 2.12
import QtQuick.Controls 2.5
import QtQuick.Dialogs 1.1


ApplicationWindow {
    id: root
    visible: true
    title: "DynPy"

    Column {
        padding: 15
        spacing: 15

        Text {
            font.family: "Helvetica"
            font.pointSize: 24
            text: "IP: " + controller.ip
        }

        Text {
            font.family: "Helvetica"
            font.pointSize: 24
            wrapMode: Text.WordWrap
            width: root.width - 30
            text: "DynPy is about to setup your application."
        }

        Text {
            font.family: "Helvetica"
            font.pointSize: 24
            wrapMode: Text.WordWrap
            width: root.width - 30
            text: "Please enter the url of your http server and a modulename for yor python file to be loaded."
        }

        Text {
            font.family: "Helvetica"
            font.pointSize: 20
            font.weight: Font.Bold
            text: "Url:"
        }
        TextField {
            id: url
            font.family: "Helvetica"
            font.pointSize: 20
            clip: true
            width: root.width - 30 
            placeholderText: "https://raw.githubusercontent.com/Artanidos/DynPy/master/server"
            text: "https://raw.githubusercontent.com/Artanidos/DynPy/master/server"
        }
        Text {
            font.family: "Helvetica"
            font.pointSize: 20
            font.weight: Font.Bold
            text: "Module:"
        }
        TextField {
            id: mod
            font.family: "Helvetica"
            font.pointSize: 20
            clip: true
            width: root.width - 30
            placeholderText: "demo.py"
            text: "test_package"
        }
        Row {
            spacing: 20
            Button {
                font.family: "Helvetica"
                font.pointSize: 20
                font.weight: Font.Bold
                text: "Load"
                enabled: url.text.length > 0  &&  mod.text.length > 0
                onClicked: {
                    controller.save(url.text, mod.text)
                    close()
                }
            }

            Button {
                font.family: "Helvetica"
                font.pointSize: 20
                font.weight: Font.Bold
                text: "Cancel"
                onClicked: {
                    close()
                }
            }
        }

        Text {
            font.family: "Helvetica"
            font.pointSize: 20
            text: "Please reload the application to load the desired url."
        }
    }
}