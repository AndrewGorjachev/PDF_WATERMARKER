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

            ColumnLayout {
                id: column_left

                Text
                {
                    id: text_directory
                    width: 0
                    text: qsTr("Directory:")
                    font.pixelSize: 20
                    horizontalAlignment: Text.AlignLeft
                    verticalAlignment: Text.AlignVCenter
                    Layout.fillHeight: true
                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                }

                Text
                {
                    id: text_watermark
                    text: qsTr("Watermark:")
                    font.pixelSize: 20
                    horizontalAlignment: Text.AlignLeft
                    verticalAlignment: Text.AlignVCenter
                    Layout.fillHeight: true
                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                }
            }

            ColumnLayout
            {
                id: column_right

                TextField
                {
                    id: text_field_directory
                    text: "Choose your directory to process"
                    horizontalAlignment: Text.AlignHCenter
                    font.pointSize: 10
                    Layout.fillHeight: true
                    Layout.fillWidth: true
                    placeholderText: qsTr("Text Field")
                    selectByMouse: true
                    MouseArea
                    {
                        anchors.fill: parent
                        onClicked:
                        {
                            openFileDialog.open()
                        }
                    }
                }

                TextField
                {
                    id: text_field_watermark
                    text: "Choose your watermark"
                    horizontalAlignment: Text.AlignHCenter
                    font.pointSize: 10
                    Layout.fillHeight: true
                    Layout.fillWidth: true
                    placeholderText: qsTr("Text Field")
                    selectByMouse: true
                    onEditingFinished:
                    {
//                        controller.ip_has_changed(text_field_watermark.text)
                    }
                }
            }

        }

        RowLayout
        {
            id: column_mid

            Button
            {
                id: process_pdf
                text: qsTr("Process PDF files")
                font.pointSize: 12
                Layout.fillHeight: true
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                onClicked:
                {
                    controller.process_pdfs(text_field_directory.text, text_field_watermark.text)
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
                value: 0
            }
        }
    }

    Component.onCompleted:
    {
//        controller.ip_has_changed(text_field_watermark.text)
    }

    Connections
    {
        target: controller

        function onDirectory_didnt_exist()
        {
            directory_didnt_exist.open()
        }

        function onFiles_didnt_found()
        {
            files_didnt_found.open()
        }

        function onProcessing_has_been_completed(count)
        {
            processing_has_been_completed.open()
//            text_time.text = new Date(count*1000).toLocaleTimeString(Qt.locale(), "mm:" + "ss" )
//            progress_bar.value = count/(60*12)
        }

        function onError_while_processing(file_path)
        {
            error_while_processing.text = "Error while "+file_path+" processing"
            error_while_processing.open()
        }
    }

    FileDialog {
        id: openFileDialog
        title: "Please choose a folder"
        folder: shortcuts.home
        onAccepted:
        {
            text_field_directory.text = openFileDialog.fileUrl
        }
        onRejected:
        {
            console.log("Choosing PDF's files source has been canceled!")
        }
    }

    MessageDialog
    {
        id: directory_didnt_exist
        title: "Directory didn't exist"
        text: "Directory didn't exist. Choose another directory."
        icon: StandardIcon.Critical
        standardButtons: StandardButton.Ok
        modality: Qt.WindowModal
    }

    MessageDialog
    {
        id: files_didnt_found
        title: "Files didn't found"
        text: "Appropriate for processing files haven't been found."
        icon: StandardIcon.Information
        standardButtons: StandardButton.Ok
        modality: Qt.WindowModal
    }

    MessageDialog
    {
        id: processing_has_been_completed
        title: "Processing has been completed"
        text: "All files have been watermarked."
        icon: StandardIcon.Information
        standardButtons: StandardButton.Ok
        modality: Qt.WindowModal
    }

    MessageDialog
    {
        id: error_while_processing
        title: "Error while file processing"
        icon: StandardIcon.Warning
        standardButtons: StandardButton.Ok
        modality: Qt.WindowModal
    }
}
