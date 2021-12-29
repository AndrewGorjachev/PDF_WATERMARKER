import QtQuick 2.15
import QtQuick.Window 2.2
import QtQuick.Dialogs 1.0
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.15
import QtQuick.Dialogs 1.3

Window
{
    id: main_window
    visible: true
    property alias row_bot: row_bot
    width: main_layout.implicitWidth
    height: main_layout.implicitHeight
    minimumWidth: main_layout.implicitWidth
    minimumHeight: main_layout.implicitHeight
    title: qsTr("PDF WaterMarker " + Qt.application.version)

    property bool thread_is_running: false

    onClosing:
    {
        close.accepted = !thread_is_running

        onTriggered:
        {
            if(thread_is_running)
            {
                exit_message_dialog_id.open()
            }
        }
    }
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
            id: row_top

            ColumnLayout
            {
                id: column_left

                Text
                {
                    id: text_directory
                    width: 150
                    text: qsTr("Directory:")
                    font.pixelSize: 14
                    horizontalAlignment: Text.AlignLeft
                    verticalAlignment: Text.AlignVCenter
                    wrapMode: Text.WordWrap
                    Layout.fillHeight: true
                    Layout.fillWidth: false
                }
                Text
                {
                    id: text_empty_1
                    width: 150
                    visible: true
                    text: qsTr("")
                    font.pixelSize: 20
                    horizontalAlignment: Text.AlignLeft
                    verticalAlignment: Text.AlignVCenter
                    Layout.fillHeight: true
                    Layout.fillWidth: false
                }
                Text
                {
                    id: text_watermark
                    width: 150
                    text: qsTr("Watermark:")
                    font.pixelSize: 14
                    horizontalAlignment: Text.AlignLeft
                    verticalAlignment: Text.AlignVCenter
                    wrapMode: Text.WordWrap
                    Layout.fillHeight: true
                    Layout.fillWidth: false
                }
                Text
                {
                    id: text_empty_2
                    width: 150
                    visible: true
                    text: qsTr("")
                    font.pixelSize: 20
                    horizontalAlignment: Text.AlignLeft
                    verticalAlignment: Text.AlignVCenter
                    Layout.fillHeight: true
                    Layout.fillWidth: false
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
                    placeholderText: qsTr("Watermark line 0")
                    selectByMouse: true
                    onEditingFinished:
                    {
                        save_parameters()
                    }
                }
                TextField
                {
                    id: text_field_watermark_line_1
                    text: "Watermark line 1"
                    horizontalAlignment: Text.AlignHCenter
                    Layout.fillHeight: true
                    Layout.fillWidth: true
                    placeholderText: qsTr("Watermark line 1")
                    font.pointSize: 10
                    selectByMouse: true
                    onEditingFinished:
                    {
                        save_parameters()
                    }
                }
                TextField
                {
                    id: text_field_watermark_line_2
                    text: "Watermark line 2"
                    horizontalAlignment: Text.AlignHCenter
                    Layout.fillHeight: true
                    Layout.fillWidth: true
                    placeholderText: qsTr("Watermark line 2")
                    font.pointSize: 10
                    selectByMouse: true
                    onEditingFinished:
                    {
                        save_parameters()
                    }
                }
            }
        }
        RowLayout
        {
            id: row_mid_0

            Text
            {
                id: opacity_text
                width: 140
                text: qsTr("Opacity:")
                font.pixelSize: 14
                horizontalAlignment: Text.AlignLeft
                verticalAlignment: Text.AlignVCenter
                Layout.fillWidth: true
                Layout.fillHeight: true
            }
            Slider
            {
                id: opacity_slider
                font.weight: Font.Light
                font.pointSize: 6
                Layout.fillWidth: true
                Layout.fillHeight: true
                stepSize : 0.05
                onMoved:
                {
                    if (value == 0)
                    {
                        value = 0.05
                    }
                    opacity_text.opacity = value
                    save_parameters()
                }
            }

            Text {
                id: font_size_text
                text: qsTr("Font size:")
                font.pixelSize: 14
                horizontalAlignment: Text.AlignLeft
                verticalAlignment: Text.AlignVCenter
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
            }

            ComboBox {
                id: font_size_comboBox
                font.pointSize: 10
                Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                Layout.fillWidth: true
                Layout.fillHeight: true
                currentIndex: 3
                model: ["10", "12", "14", "16", "18", "20", "22"]
                onCurrentIndexChanged:
                {
                    save_parameters()
                }
            }
        }
        RowLayout {
            id: row_mid_1
            Button {
                id: process_pdf1
                text: qsTr("Process PDF files")
                font.bold: true
                Layout.fillWidth: true
                Layout.fillHeight: true
                font.pointSize: 12
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                onClicked:
                {
                    save_parameters()

                    controller.process_pdfs(text_field_directory.text)
                }
            }
        }
        RowLayout
        {
            id: row_bot
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
    function save_parameters()
    {
        controller.watermark_slot(text_field_watermark_line_0.text + "\n" +text_field_watermark_line_1.text + "\n" +text_field_watermark_line_2.text)

        controller.opacity_slot(opacity_slider.value*100)

        controller.font_size_slot(font_size_comboBox.textAt(font_size_comboBox.currentIndex))

        controller.write_config_file()
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
            thread_is_running = false
            processing_has_been_completed.open()
        }
        function onError_while_processing_signal(file_path)
        {
            error_while_processing.text = "Error while processing"+file_path
            error_while_processing.open()
        }
        function onProcessing_started_signal()
        {
            thread_is_running = true
        }
        function onFile_corrupted_signal(file_path)
        {
            file_corrupted_window.text = "The file could be corrupted or locked: "+file_path
            file_corrupted_window.open()
        }
        function onSet_watermark_opacity_signal(opacity)
        {
            opacity_slider.value = opacity/100
            opacity_text.opacity = opacity/100
        }
        function onSet_font_size_signal(index)
        {
            console.log(index)
            font_size_comboBox.currentIndex = index
        }
        function onWrong_ini_signal()
        {
            wrong_ini_dialog.open()
        }
        function onPlease_wait_signal()
        {
            process_hasn_t_been_completed_dialog.open()
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
    MessageDialog
    {
        id: file_corrupted_window
        title: "File Open Error"
        icon: StandardIcon.Warning
        standardButtons: StandardButton.Ok
        modality: Qt.WindowModal
    }
    MessageDialog
    {
        id: exit_message_dialog_id
        title: "Exiting"
        icon: StandardIcon.Question
        text: "The files processing isn't completed. Are you sure to exit?"
        standardButtons: StandardButton.Yes | StandardButton.No
        onYes:
        {
            thread_is_running = false
            main_window.close()
        }
    }
    MessageDialog
    {
        id: wrong_ini_dialog
        title: "Open ini file error"
        icon: StandardIcon.Warning
        text: "Error while opening ini file."
        standardButtons: StandardButton.Ok
    }
    MessageDialog
    {
        id:  process_hasn_t_been_completed_dialog
        title: "Please wait"
        icon: StandardIcon.Warning
        text: "The process hasn't been completed."
        standardButtons: StandardButton.Ok
    }
}


