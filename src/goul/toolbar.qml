import QtQuick 2.1
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.11

ToolBar {
    id: toolbar

    RowLayout {
        width: parent.width

        ToolButton {
            id: drawBtn
            display: AbstractButton.IconOnly
            icon.name: "insert-image"
            onClicked: {
                // FIXME: change to toolbar.toggle_draw()
                toolbar.update_plot()
            }
        }

        ToolButton {
            id: clearBtn
            display: AbstractButton.IconOnly
            icon.name: "edit-clear"
        }

        ToolButton {
            id: randomBtn
            display: AbstractButton.IconOnly
            icon.name: "view-refresh"
        }

        // FIXME: too small dropdown
        ComboBox {
            id: gameTypeCombo
            model: toolbar ? toolbar.game_type_names : []
            onCurrentTextChanged: {
                toolbar ? toolbar.set_game_type(currentText) : undefined
            }
        }

        Item {
            Layout.fillWidth: true
        }

        ToolButton {
            id: playToggleBtn
            display: AbstractButton.IconOnly
            icon.name: "media-playback-start"
        }

    }

}