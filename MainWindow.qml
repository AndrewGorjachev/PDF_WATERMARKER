import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Dialogs 1.2
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.15

Window
{
    id: main_window
    visible: true
    width: main_layout.implicitWidth+60
    height: main_layout.implicitHeight
    minimumWidth: main_layout.implicitWidth+60
    minimumHeight: main_layout.implicitHeight
    title: qsTr("PDF WaterMarker")

    ColumnLayout
    {
        id: main_layout
        visible: true
        anchors.fill: parent
        anchors.rightMargin: 5
        anchors.leftMargin: 5
        anchors.bottomMargin: 5
        anchors.topMargin: 5

        RowLayout
        {
            id: column_top

            Text
            {
                id: text_directory
                text: qsTr("Directory:")
                font.pixelSize: 25
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                Layout.fillHeight: true
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            }

            TextField
            {
                id: text_field_directory
                text: "Choose directory to process"
                horizontalAlignment: Text.AlignHCenter
                font.pointSize: 10
                Layout.fillHeight: true
                Layout.fillWidth: true
                placeholderText: qsTr("Text Field")
                selectByMouse: true
                onEditingFinished:
                {
                    controller.ip_has_changed(text_field_ip.text)
                }
            }
        }
        RowLayout
        {
            id: column_sub_top

            Text
            {
                id: text_ip
                text: qsTr("IP:")
                font.pixelSize: 25
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                Layout.fillHeight: true
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            }

            TextField
            {
                id: text_field_ip
                text: "192.168.0.10"
                horizontalAlignment: Text.AlignHCenter
                font.pointSize: 10
                Layout.fillHeight: true
                Layout.fillWidth: true
                placeholderText: qsTr("Text Field")
                selectByMouse: true
                onEditingFinished:
                {
                    controller.ip_has_changed(text_field_ip.text)
                }
            }
        }


        RowLayout
        {
            id: column_mid

            Button
            {
                id: enable_rtl
                text: qsTr("Enable RTL")
                font.pointSize: 12
                Layout.fillHeight: true
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                onClicked:
                {
                    controller.ip_has_changed(text_field_ip.text)

                    controller.enable_rtl()
                }
            }
        }

        RowLayout
        {
            id: column_bot
            visible: true
            Layout.fillHeight: true
            Layout.fillWidth: true

            ProgressBar
            {
                id: progress_bar
                Layout.fillHeight: true
                Layout.fillWidth: true
                value: 1
            }

            Text
            {
                id: text_time
                text: qsTr("12:00")
                font.pixelSize: 12
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                Layout.fillHeight: true
                Layout.fillWidth: true
            }
        }    
    }
    Component.onCompleted:
    {
        controller.ip_has_changed(text_field_ip.text)
    }

    Connections
    {
        target: controller

        function onUnitConnectionError()
        {
            unit_connection_error.open()
        }

        function onUnitConnectionSuccess()
        {
            unit_connection_success.open()
        }

        function onTimerChanged(count)
        {
            text_time.text = new Date(count*1000).toLocaleTimeString(Qt.locale(), "mm:" + "ss" )
            progress_bar.value = count/(60*12)
        }

        function onSetIP(ip)
        {
            text_field_ip.text = ip
        }

        function onPleaseWait()
        {
            please_wait.open()
        }
    }

    MessageDialog
    {
        id: unit_connection_error
        title: "Unit connection error"
        text: "Error while unit connection"
        icon: StandardIcon.Critical
        standardButtons: StandardButton.Ok
        modality: Qt.WindowModal
    }

    MessageDialog
    {
        id: unit_connection_success
        title: "RTL has enabled"
        text: "RTL has enabled"
        icon: StandardIcon.Information
        standardButtons: StandardButton.Ok
        modality: Qt.WindowModal
    }

    MessageDialog
    {
        id: please_wait
        title: "Please wait"
        text: "Previous try hasn't completed"
        icon: StandardIcon.Warning
        standardButtons: StandardButton.Ok
        modality: Qt.WindowModal
    }
}
