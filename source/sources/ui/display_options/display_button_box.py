from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialogButtonBox


##
# @ingroup display_options
#

##
# DisplayButtonBox
# Button box to change the display mode of listviews.
#
class DisplayButtonBox(QtWidgets.QDialogButtonBox):
    ##
    # DisplayButtonBox Constructor.
    # 
    # @param self The object pointer
    # @param parent parent (QWidget)
    #
    def __init__(self, parent=None):
        super(DisplayButtonBox, self).__init__(parent)
        self.setOrientation(Qt.Horizontal)
        namesButton = QtWidgets.QPushButton("by Names", self)
        idsButton = QtWidgets.QPushButton("by Ids", self)
        id_nameButton = QtWidgets.QPushButton("by Ids and Names", self)
        self.addButton(namesButton, QDialogButtonBox.ActionRole)
        self.addButton(idsButton, QDialogButtonBox.ActionRole)
        self.addButton(id_nameButton, QDialogButtonBox.ActionRole)

        namesButton.clicked.connect(parent.display_names)
        idsButton.clicked.connect(parent.display_ids)
        id_nameButton.clicked.connect(parent.display_id_name)


##
# default_display function.
# Change the current display to displayed_type and refresh the display of the item of the list.
# @param self The object pointer (listview)
# @param displayed_type new displayed type
#
def default_display(self, displayed_type):
    if self.displayed_type != displayed_type:
        self.displayed_type = displayed_type
        self.refresh()
