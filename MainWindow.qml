import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Dialogs 1.0
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.15
import QtQuick.Dialogs 1.3

Window
{
    id: main_window
    visible: true
    property alias text_field_watermark_line_0: text_field_watermark_line_0
    width: main_layout.implicitWidth+300
    height: main_layout.implicitHeight
    minimumWidth: main_layout.implicitWidth+300
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
                    text: qsTr("Directory:")
                    height: text_field_directory.implicitHeight
                    font.pixelSize: 20
                    horizontalAlignment: Text.AlignLeft
                    verticalAlignment: Text.AlignVCenter
                    Layout.fillHeight: true
                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                }

                Item
                {
                    clip: false
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    Rectangle
                    {
                        anchors.fill: parent
                        height: text_directory.height
                    }
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

                Item
                {
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    Rectangle
                    {
                        anchors.fill: parent
                        height: text_watermark.height
                    }
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
                    id: text_field_watermark_line_0
                    text: "Watermark line 0"
                    horizontalAlignment: Text.AlignHCenter
                    font.pointSize: 10
                    Layout.fillHeight: true
                    Layout.fillWidth: true
                    placeholderText: qsTr("Text Field")
                    selectByMouse: true
                    onEditingFinished:
                    {
                        controller.write_config_file(text_field_watermark_line_0.text + "\n" +text_field_watermark_line_1.text + "\n" +text_field_watermark_line_2.text)
                    }
                }

                TextField {
                    id: text_field_watermark_line_1
                    text: "Watermark line 1"
                    horizontalAlignment: Text.AlignHCenter
                    Layout.fillHeight: true
                    Layout.fillWidth: true
                    placeholderText: qsTr("Text Field")
                    font.pointSize: 10
                    selectByMouse: true
                }

                TextField {
                    id: text_field_watermark_line_2
                    text: "Watermark line 2"
                    horizontalAlignment: Text.AlignHCenter
                    Layout.fillHeight: true
                    Layout.fillWidth: true
                    placeholderText: qsTr("Text Field")
                    font.pointSize: 10
                    selectByMouse: true
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
                    controller.process_pdfs(text_field_directory.text, text_field_watermark_line_0.text)
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
    Connections
    {
        target: controller

        function onDirectory_not_exist_signal()
        {
            directory_didnt_exist.open()
        }

        function onFiles_not_found_signal()
        {
            files_didnt_found.open()
        }

        function onSet_watermark_text_to_view_signal(line_number, watrmark_text)
        {
            switch (line_number)
            {
            case 0: text_field_watermark_line_0.text = watrmark_text; break
            case 1: text_field_watermark_line_1.text = watrmark_text; break
            case 2: text_field_watermark_line_2.text = watrmark_text; break
            }
        }

        function onProcessing_progress_signal(count)
        {
            progress_bar.value = count/100
        }

        function onProcessing_completed_signal()
        {
            processing_has_been_completed.open()
        }

        function onError_while_processing_signal(file_path)
        {
            error_while_processing.text = "Error while "+file_path+" processing"
            error_while_processing.open()
        }
    }

    FileDialog
    {
        id: openFileDialog
        selectFolder: true
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
