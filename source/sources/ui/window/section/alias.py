from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Qt

from sources.back.neo.neoobj import NeoType
from sources.back.neo.query import Query
from sources.back.neo.request_neo import get_data, run_mult_result
from sources.ui.listview.list_view import ListView


##
# @ingroup section
#

##
# Alias.
# QWidget to display aliases in show detail window.
#
class Alias(QtWidgets.QWidget):
    ##
    # @var button
    # QPushButton to show or hide list of alias
    #
    # @var listview
    # ListView containing the aliases
    #

    ##
    # MitigationWindow Constructor.
    # 
    # @param self The object pointer
    # @param obj NeoObj represent the group
    # @param parent Parent (QWidget)
    def __init__(self, obj, parent=None):
        super(Alias, self).__init__(parent=parent)
        if obj.type != NeoType.Group:
            raise TypeError("NeoObj must have Group type.")
        self.button = QtWidgets.QPushButton("Show Associated Groups")
        self.button.clicked.connect(self.displaylist)
        query = Query(input_obj=obj, node_output="Group")
        if (status := get_data(run_mult_result, query, parent, query.result_column)).is_ok():
            content = status.content
        else:
            status.exec()
            return
        self.listview = ListView(content=content, view="name", parent=self, sort=False)

        self.setLayout(QtWidgets.QVBoxLayout(self))
        layout = self.layout()
        layout.addWidget(self.button)
        self.layout().addWidget(self.listview)

        self.listview.hide()

    ##
    # MitigationWindow displaylist method.
    # Show or hide Alias listview.
    # @param self The object pointer
    @QtCore.Slot()
    def displaylist(self):
        if self.button.text() == "Show Associated Groups":
            self.button.setText("Hide Associated Groups")
            self.listview.show()
        else:
            self.button.setText("Show Associated Groups")
            self.listview.hide()

    ##
    # MitigationWindow get_alias_widget method.
    # Create Alias Widget for obj and return it if at least one alias id found. If no alias were found returns a
    # QWidget.QLabel.
    # @param obj NeoObj (must be Group type)
    # @param parent parent (QWidget)
    # @return QWidget (QLabel or Alias)
    @staticmethod
    def get_alias_widget(obj, parent):
        res = Alias(obj, parent)
        if len(res.listview.get_items()) == 0:
            res = QtWidgets.QLabel("No Associated Group found.", parent)
            res.setAlignment(Qt.AlignRight)
        return res
