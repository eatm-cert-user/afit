from PySide6 import QtWidgets

from sources.back.neo.neoobj import NeoType
from sources.ui.listview.list_view import ListView
from sources.ui.listview.list_item import ListItem
from sources.ui.listview.mitigations.mitigation_list_view import MitigationListView
from sources.ui.listview.mitigations.mitigation_options import MitigationOptions


##
# @ingroup listview
#

##
# color_items function.
# Set the background of the given items
# @param items list of items (list of QStandardItem)
# @param color color (QColor)
def color_items(items, color):
    for item in items:
        item.setBackground(color)


##
# @ingroup listview
#

##
# TechniqueMitigationView class.
# Widget to display Techniques given with their related mitigations in two distinct listview.
#
class TechniqueMitigationView(QtWidgets.QWidget):
    ##
    # @var mitigation_view
    # ListViews for Mitigations.
    #
    # @var technique_view
    # ListViews for Techniques.
    #
    # @var m_data
    # Dictionary (key:, value:). Link the mitigations to their corresponding ListItem
    #
    # @var t_data
    # Dictionary (key: ListItem index, value: NeoObj (type Technique)).
    # Link all techniques to their position in the list
    #

    ##
    # TechniqueMitigationView Constructor.
    # @param self The object pointer
    # @param data Dictionary with techniques as keys and list of mitigation as values (dict <NeoObj, list of NeoObj>)
    # @param parent parent widget (QWidget)
    def __init__(self, data, parent=None):
        super(TechniqueMitigationView, self).__init__(parent)
        self.setLayout(QtWidgets.QGridLayout(self))
        # self.setLayout(self.layout)

        # ListViews for Techniques and Mitigations
        self.mitigation_view = MitigationListView(parent=self)
        self.technique_view = ListView(options=MitigationOptions, query_type=[NeoType.Group], parent=parent)

        # Add labels and listviews to the layout
        self.layout().addWidget(QtWidgets.QLabel("Techniques", self), 0, 0)
        self.layout().addWidget(QtWidgets.QLabel("Mitigations", self), 0, 1)
        self.layout().addWidget(self.technique_view, 1, 0)
        self.layout().addWidget(self.mitigation_view, 1, 1)

        # Dictionary (key:, value:)
        # link the mitigations to their corresponding ListItem
        self.m_data = {}
        # Dictionary (key: ListItem index, value: NeoObj (type Technique))
        # Link all techniques to their position in the list
        self.t_data = {}

        # add data to listviews and dictionaries
        for elem in data.keys():
            technique_item = ListItem(elem, "id_name")
            self.technique_view.add_item(technique_item)
            self.t_data[technique_item.index()] = technique_item
            for m in data.get(elem):
                if self.m_data.get(m) is None:
                    mitigation_item = ListItem(m, "id_name")
                    self.m_data[m] = mitigation_item
        self.mitigation_view.add_items(list(self.m_data.values()))

    ##
    # TechniqueMitigationView get_selected_techniques method.
    # 
    # @param self The object pointer
    def get_selected_techniques(self):
        """
        Returns selected ListItems
        :return: list of ListItem
        """
        return [self.t_data.get(index) for index in self.technique_view.selectionModel().selectedIndexes() if
                index is not None]

    ##
    # TechniqueMitigationView get_current_technique method.
    # 
    # @param self The object pointer
    def get_current_technique(self):
        """
        Returns the current ListItem
        :return: ListItem
        """
        return self.t_data.get(self.technique_view.selectionModel().currentIndex())

    ##
    # TechniqueMitigationView get_all method.
    # 
    # @param self The object pointer
    def get_all(self):
        """
        Return all items from both list
        :return: list of ListItem
        """
        values = list(self.t_data.values())
        values.extend(self.m_data.values())
        return values

    ##
    # TechniqueMitigationView color method.
    # 
    # @param self The object pointer
    def color(self, items, color):
        """
        Sets all item's background in 'items'
        @param items list of items
        @param color color
        :type items: ListItem QtGui.QStandardItem()
        :type color: QColor
        :return:
        """
        for elem in items:
            item = self.m_data.get(elem) if not isinstance(elem, ListItem) and self.m_data.get(elem) is not None else elem
            item.setBackground(color)
