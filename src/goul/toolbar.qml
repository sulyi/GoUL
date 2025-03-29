import QtQuick 2.1
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.11

ToolBar {
    objectName: "actions_toolBar"

    RowLayout {
        width: parent.width

        ToolButton {
            objectName: "draw_btn"
            display: AbstractButton.IconOnly
            icon.name: "insert-image"
            onClicked: {
                // FIXME: change to toolbar.toggle_draw()
                toolbar.update_plot()
            }
        }

        ToolButton {
            objectName: "clear_btn"
            display: AbstractButton.IconOnly
            icon.name: "edit-clear"
        }

        ToolButton {
            objectName: "random_btn"
            display: AbstractButton.IconOnly
            icon.name: "view-refresh"
        }

        // FIXME: too small dropdown
        ComboBox {
            objectName: "game_type_combo"
            model: toolbar ? toolbar.game_type_names : []
            onCurrentTextChanged: {
                toolbar ? toolbar.set_game_type(currentText) : undefined
            }
        }

        Item {
            Layout.fillWidth: true
        }

        ToolButton {
            objectName: "start_stop_btn"
            display: AbstractButton.IconOnly
            icon.name: "media-playback-start"
        }

    }

}