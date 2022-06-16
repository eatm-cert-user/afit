from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import QModelIndex, Qt
from PySide6.QtWidgets import QAbstractItemView

from sources.back.neo.requests_groups import get_groups
from sources.back.neo.neoobj import NeoObj
from sources.back.tools import Tools
from sources.ui.display_options.display_options import DisplayedType
from sources.ui.display_options.display_button_box import DisplayButtonBox, default_display
from sources.ui.window.save_window import SaveWindow


##
# @ingroup section
#

##
# Result.
# Result section (QWidget). Display the result table and save section.
#
class Result(QtWidgets.QWidget):
    ##
    # @var resultList
    # Result Data (list)
    #
    # @var displayed_type
    # Enum DisplayedType representing the current display mode.
    #
    # @var tableView
    # Table View used to display data from self.resultList
    #

    ##
    # Result Constructor.
    # 
    # @param self The object pointer
    # @param parent Parent (QWidget)
    def __init__(self, parent=None):
        super(Result, self).__init__(parent)
        self.setLayout(QtWidgets.QVBoxLayout(self))
        self.layout().addWidget(QtWidgets.QLabel("Results"))

        # Result data.
        self.resultList = [[]]
        # Display option
        self.displayed_type = DisplayedType.IdName
        display_box = DisplayButtonBox(self)
        self.layout().addWidget(display_box)

        # Table View to display Result Data
        self.tableView = QtWidgets.QTableView(self)
        self.tableView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableView.setSelectionMode(QAbstractItemView.SingleSelection)

        self.tableView.setModel(TableModel(self.resultList, self.tableView))
        # I kept the button box in case there is more option to add
        button_box = QtWidgets.QDialogButtonBox(Qt.Horizontal, self)
        save_button = QtWidgets.QPushButton("Save", self)

        button_box.addButton(save_button, QtWidgets.QDialogButtonBox.ActionRole)
        # button_box.addButton(self.detailsButton, QtWidgets.QDialogButtonBox.ActionRole)
        self.layout().addWidget(self.tableView)
        self.layout().addWidget(button_box, alignment=QtCore.Qt.AlignCenter | QtCore.Qt.AlignRight)

        save_button.clicked.connect(self.save)
        # self.detailsButton.clicked.connect(self.details)

    ##
    # Result save method.
    # Create a new SaveWindow exec to save the results and exec the ExitStatus message.
    # @param self The object pointer
    @QtCore.Slot()
    def save(self):
        SaveWindow(self.resultList, self).exec().exec()

    ##
    # Result display_names method.
    # Displays the techniques by names.
    # @param self The object pointer
    @QtCore.Slot()
    def display_names(self):
        default_display(self, DisplayedType.Name)

    ##
    # Result display_ids method.
    # Displays the techniques by ids.
    # @param self The object pointer
    @QtCore.Slot()
    def display_ids(self):
        default_display(self, DisplayedType.Id)

    ##
    # Result display_id_name method.
    # Displays the techniques by ids and names.
    # @param self The object pointer
    @QtCore.Slot()
    def display_id_name(self):
        default_display(self, DisplayedType.IdName)

    ##
    # Result refresh_res method.
    # get data (query) and set self.resultList
    # @param self The object pointer
    def refresh_res(self):
        techniques = self.parent().techniques_list.get_ids()
        if len(techniques) == 0:
            self.resultList = [[]]
        else:
            res = get_groups(techniques)
            if not res:
                self.resultList = [[]]
            else:
                self.resultList = []
                for elem in res:
                    list_neo = []
                    for d in elem[1]:
                        # Removing Aliases
                        if d.get('external_id'):
                            list_neo.append(NeoObj(d))
                    n_used = str(elem[0])
                    n_total = str(len(techniques))
                    percentage = str(int(float(elem[0]) * 100.0 / len(techniques))) + "%"
                    content = n_used + " out of " + n_total + "\n" + percentage
                    tooltip = "These groups used " + n_used
                    tooltip += " techniques contained in the initial list of " + n_total
                    tooltip += " techniques.\nThis amount represent " + percentage + " of the original list."
                    w = QtWidgets.QLabel(content)
                    w.setAutoFillBackground(True)
                    w.setToolTip(tooltip)
                    self.resultList.append([w, list_neo])

    ##
    # Result refresh method.
    # Refresh the display of the table view.
    # @param self The object pointer
    def refresh(self):
        for elem in self.tableView.model().get_data():
            elem[1].set_view(self.displayed_type.value)

    ##
    # Result refresh_data method.
    # set table from self.resultList.
    # @param self The object pointer
    # @param att view type. ex: "name", "id", "id_name" (str)
    def refresh_data(self, att="name"):
        res = Tools.get_display_list(self.resultList, att, self.tableView)
        if not res:
            res = [[]]
        self.tableView.setModel(TableModel(res, self.tableView))
        self.tableView.resizeRowsToContents()
        self.tableView.resizeColumnsToContents()
        old_w = self.tableView.columnWidth(1)
        self.tableView.setColumnWidth(1, old_w + 20)

    ##
    # Result refresh_table method.
    # refresh data and set table view.
    # @param self The object pointer
    def refresh_table(self):
        self.refresh_res()
        self.refresh_data(self.displayed_type.value)


##
# TableModel
# Custom TableModel for the result table view.
#
class TableModel(QtCore.QAbstractTableModel):
    ##
    # @var _data
    # Data contained in the table.
    #

    ##
    # TableModel Constructor.
    # 
    # @param self The object pointer
    # @param data Result in list form
    # @param parent Parent (QWidget)
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self._data = data

    ##
    # TableModel rowCount method.
    # Return number of rows in the table model.
    # @param self The object pointer
    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    ##
    # TableModel columnCount method.
    # Return number of columns in the table model.
    # @param self The object pointer
    def columnCount(self, parent=QModelIndex()):
        return len(self._data[0])

    ##
    # TableModel data method.
    # Set widget in the table view and return str value of the data for a specific index.
    # @param self The object pointer
    # @param index Index of the item
    # @param role Enum Role
    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole or role == Qt.EditRole:
                value = self._data[index.row()][index.column()]
                # insert widget in tableview
                self.parent().setIndexWidget(index, value)
                return value.text()

    ##
    # TableModel get_data method.
    # return data of the table.
    # @param self The object pointer
    def get_data(self):
        return self._data

    ##
    # TableModel get_data_from_index method.
    # return the data contained in the table for a specific index.
    # @param self The object pointer
    def get_data_from_index(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole or role == Qt.EditRole:
                value = self._data[index.row()][index.column()]
                # insert widget in tableview
                self.parent().setIndexWidget(index, value)
                return value

    ##
    # TableModel setData method.
    # set the value of a specific cell of the table
    # @param self The object pointer
    # @param index Index of the cell
    # @param value New value of the cell
    # @param role Role
    def setData(self, index, value, role=Qt.DisplayRole):
        if role == Qt.EditRole:
            self._data[index.row()][index.column()] = value
            return True
        return False

    ##
    # TableModel flags method.
    # Return the flags for the cells
    # @param self The object pointer
    # @param index Index
    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled  # | Qt.ItemIsEditable

    ##
    # TableModel headerData method.
    # Set the headers to be displayed.
    # @param self The object pointer
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            if section == 0:
                return "Count"
            elif section == 1:
                return "Group"
            elif section == 2:
                return "Mitigations"
        return None
