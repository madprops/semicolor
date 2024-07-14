# Standard
from pathlib import Path

# Libraries
from PySide6.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout  # type: ignore
from PySide6.QtWidgets import QPushButton, QWidget, QColorDialog
from PySide6.QtGui import QIcon  # type: ignore
from PySide6.QtCore import QTimer  # type: ignore


def main() -> None:
    app = QApplication([])
    picker, picker_row = make_picker(app)
    btn_row = make_buttons(picker)

    main_layout = QVBoxLayout()
    main_layout.addLayout(picker_row)
    main_layout.addLayout(btn_row)

    prepare_window(app, main_layout)


def copy(text: str) -> None:
    clipboard = QApplication.clipboard()
    clipboard.setText(text)


def prepare_window(app: QApplication, main_layout: QVBoxLayout) -> None:
    window = QWidget()
    main_layout.setSizeConstraint(QVBoxLayout.SetFixedSize)
    window.setLayout(main_layout)
    window.show()

    here = Path(__file__).parent
    path = Path(here, "icon.png")
    window.setWindowIcon(QIcon(str(path)))
    window.setWindowTitle("Semicolor")
    app.setStyleSheet("QWidget { background-color: #333; color: #FFF; }")
    app.exec()


def make_picker(app) -> tuple[QColorDialog, QHBoxLayout]:
    picker_row = QHBoxLayout()
    picker = QColorDialog()
    picker.setOption(QColorDialog.DontUseNativeDialog)
    picker.setOption(QColorDialog.NoButtons)

    def close_window() -> None:
        app.quit()

    picker.finished.connect(close_window)
    picker.setMinimumWidth(200)
    picker.setMinimumHeight(100)
    picker.setStyleSheet("background-color: #666;")
    picker_row.addWidget(picker)
    return picker, picker_row


def make_buttons(picker: QColorDialog) -> QHBoxLayout:
    def copied(btn: QPushButton, text: str) -> None:
        btn.setText("Copied!")
        QTimer.singleShot(1000, lambda: btn.setText(text))

    def copy_rgb() -> None:
        color = picker.currentColor()
        rgb = f"rgb({color.red()}, {color.green()}, {color.blue()})"
        copy(rgb)
        copied(btn_rgb, "Copy RGB")

    def copy_hex() -> None:
        color = picker.currentColor()
        hex_color = color.name()
        copy(hex_color)
        copied(btn_hex, "Copy Hex")

    btn_row = QHBoxLayout()
    btn_rgb = QPushButton("Copy RGB")
    btn_hex = QPushButton("Copy Hex")
    btn_rgb.setStyleSheet("font-size: 18px;")
    btn_hex.setStyleSheet("font-size: 18px;")
    btn_row.addWidget(btn_rgb)
    btn_row.addWidget(btn_hex)
    btn_rgb.clicked.connect(copy_rgb)
    btn_hex.clicked.connect(copy_hex)
    return btn_row


if __name__ == "__main__":
    main()
