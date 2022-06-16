from PySide6 import QtWidgets, QtGui
from PySide6.QtGui import QStandardItem
from PySide6.QtWidgets import QAbstractItemView

from sources.ui.listview.list_item import ListItem


##
# @ingroup listview
#

##
# ListView.
# Custom QListView used to display list of NeoObj.
#
class ListView(QtWidgets.QListView):
    ##
    # @var msgBox
    # MessageBox in case of error
    #
    # @var current_view
    # View mode of the items of the list
    #
    # @var option
    # option menu of the list
    #

    ##
    # ListView Constructor.
    # 
    # @param self The object pointer
    # @param options Options class to add to listview (class Options)
    # @param content content of the list (list of NeoObj)
    # @param bold content to be displayed in bold (if items are not in content they will be ignored) (list of NeoObj)
    # @param view display mode (id name ...) (str)
    # @param selection_mode selection mode (multiple, one selection, no selection...) (QAbstractItemView.SelectionMode)
    # @param remove if remove option is enable (bool)
    # @param query_type list of query action to add (query generate for each item in content to find relations with
    # specific type in query_type) (list of NeoType)
    # @param parent parent (QWidget)
    # @param sort True if the list must be sorted
    #
    def __init__(self, options=None, content=[], bold=[], view="id_name",
                 selection_mode=QAbstractItemView.MultiSelection, remove=False, query_type=[], parent=None, sort=True):
        super(ListView, self).__init__(parent)

        if sort:
            # bold.sort(key=lambda x: x.get_id(), reverse=True)
            content.sort(key=lambda x: x.get_id())

        # MessageBox in case of error
        self.msgBox = QtWidgets.QMessageBox(parent)
        self.msgBox.setWindowTitle("Error")

        # set items in the list view
        self.current_view = view
        model = QtGui.QStandardItemModel()
        self.setModel(model)
        # index of first item not bold
        self.bold_index = 0
        for e in content:
            self.add_item(ListItem(e, self.current_view), e in bold)
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)

        if options is not None:
            self.option = options(self, remove, query_type)
        self.setSelectionMode(selection_mode)

    ##
    # ListView Override __str__ method.
    # Return a str with the str representation of the items and one item per line.
    # @param self The object pointer
    def __str__(self):
        res = "\n"
        model = self.model()
        for index in range(model.rowCount()):
            res += str(model.item(index)) + "\n"
        return res

    ##
    # ListView text method.
    # Return a str with the str representation of the items and one item per line.
    # @param self The object pointer
    def text(self):
        return str(self)

    ##
    # ListView get_items method.
    # Return all items in the listview
    # @param self The object pointer
    def get_items(self):
        return [self.model().item(index) for index in range(self.model().rowCount())]

    ##
    # ListView in_bold method.
    # display all items in bold_items in bold
    # (not used anymore already did it in the Constructor)
    # @param self The object pointer
    # @param bold_items list of ListItem
    def in_bold(self, bold_items):
        model = self.model()
        for index in range(model.rowCount()):
            item = model.item(index)
            if item in bold_items:
                font = item.font()
                font.setBold(True)
                item.setFont(font)

    ##
    # ListView clear method.
    # clear the list view
    # @param self The object pointer
    def clear(self):
        self.setModel(QtGui.QStandardItemModel())

    ##
    # ListView set_view method.
    # Change current view
    # @param self The object pointer
    # @param view new view type (ex: "external_id", "name", "id_name") (str)
    def set_view(self, view):
        if self.current_view == view:
            return
        self.current_view = view
        model = self.model()
        for index in range(model.rowCount()):
            item = model.item(index)
            item.setText(view)

    ##
    # ListView add_items method.
    # add list of ListItem to the list view
    # @param self The object pointer
    # @param items items to add (list of ListItem)
    # @param bold  if True items is displayed in bold in the top of the listview (bool)
    def add_items(self, items, bold=False):
        for item in items:
            self.add_item(item, bold)

    ##
    # ListView add_item method.
    # add ListItem to the list view
    # @param self The object pointer
    # @param item Item to add (ListItem)
    # @param bold if True Item is displayed in bold in the top of the listview (bool)
    def add_item(self, item, bold=False):
        if item is not None:
            item.setText(self.current_view)
            if bold:
                font = item.font()
                font.setBold(True)
                item.setFont(font)
                self.model().insertRow(self.bold_index, item)
                self.bold_index += 1
            else:
                self.model().appendRow(item)

    ##
    # ListView _getattr method.
    # Return the 'att' of all techniques from self.list
    # @param self The object pointer
    # @param attr attribute to get (str) ex: name, external_id or id
    def _getattr(self, attr):
        res = []
        for e in [item.elem for item in self.get_items()]:  # self.list:
            res.append(e.get(attr))
        return res

    ##
    # ListView get_names method.
    # Return the name of all techniques from self.list
    # @param self The object pointer
    def get_names(self):
        return self._getattr("name")

    ##
    # ListView get_ext_ids method.
    # Return the external_id of all techniques from self.list
    # @param self The object pointer
    def get_ext_ids(self):
        return self._getattr("external_id")

    ##
    # ListView get_ids method.
    # Return the id of all techniques from self.list
    # @param self The object pointer
    def get_ids(self):
        return self._getattr("id")
