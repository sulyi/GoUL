import QtQuick 2.1
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.11

ToolBar {
    id: toolbar

    RowLayout {
        width: parent.width

        ToolButton {
            id: loadBtn
            display: AbstractButton.IconOnly
            icon.name: "insert-image"
            // TODO: add eventhandler
            //  onClicked: toolbarCtx.load_state()
        }

        ToolButton {
            id: stepBtn
            display: AbstractButton.IconOnly
            icon.name: "edit-redo"
            onClicked: toolbarCtx.step_game()
        }

        ToolButton {
            id: randomBtn
            display: AbstractButton.IconOnly
            icon.name: "view-refresh"
            onClicked: toolbarCtx.generate_state()
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
            // TODO: change icon as toggled
            icon.name: "media-playback-start"
            onClicked: toolbarCtx.toggle_run()
        }

    }

}