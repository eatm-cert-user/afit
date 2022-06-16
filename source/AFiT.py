import sys

from PySide6 import QtWidgets

from sources.ui.window.main_window import MainWindow


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.resize(800, 600)
    window.show()

    # check version mitre Att&ck
    window.check_graph_version()

    sys.exit(app.exec())
