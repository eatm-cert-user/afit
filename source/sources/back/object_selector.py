from PySide6 import QtWidgets, QtCore
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QComboBox


class ObjectSelector(QtWidgets.QWidget):
    def __init__(self, result_list, r_type, parent=None):
        super(ObjectSelector, self).__init__(parent)

        self.setLayout(QtWidgets.QGridLayout(self))
        self.elems = {}

        self.combo_box = QComboBox(self)
        for e in result_list:
            self.combo_box.addItem(e.get(r_type))
            self.elems[e.get(r_type)] = e
        self.layout().addWidget(QtWidgets.QLabel("Select " + r_type, self), 0, 0)
        self.layout().addWidget(self.combo_box, 0, 1)
        self.layout().addWidget(button := QtWidgets.QPushButton("More Details...", self), 1, 0)
        button.clicked.connect(self.link)

    def get_elem(self):
        return self.elems[self.combo_box.currentText()]

    @QtCore.Slot()
    def link(self):
        if (obj := self.elems.get(self.combo_box.currentText())) is not None:
            QDesktopServices.openUrl(obj.get_link())
