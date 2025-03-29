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
                toolbarCtx.update_plot()
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
            model: toolbarCtx ? toolbarCtx.game_type_names : []
            onCurrentTextChanged: {
                toolbarCtx ? toolbarCtx.set_game_type(currentText) : undefined
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