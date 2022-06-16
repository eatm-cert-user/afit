from PySide6 import QtGui


##
# @ingroup listview
#

##
# Custom item for ListView.
#
class ListItem(QtGui.QStandardItem):
    ##
    # @var elem
    # NeoObj represented by this item
    #
    # @var current_display
    # current display for the item (ex: external_id, name...)
    #

    ##
    # Constructor.
    # Note that the text of the ListItem will be empty if display is not valid.
    # @param self The object pointer
    # @param obj content of the item (NeoObj)
    # @param display display type of the object (usually external_id, name or id_name) (str)
    def __init__(self, obj, display):
        self.elem = obj
        self.current_display = display
        if (text := obj.get(display)) is not None:
            super(ListItem, self).__init__(text)
        else:
            super(ListItem, self).__init__("")
        self.setEditable(False)

    ##
    # Override __str__ method:
    # Returns text of the list item.
    # @param self The object pointer
    def __str__(self):
        return self.text()

    ##
    # Override setText method:
    # Set new text according to the new display type.
    # If the display type (text) is None the new text will be empty. If 'text' is not valid, the text will remain
    # unchanged.
    # @param self The object pointer
    # @param text New display type
    def setText(self, text):
        if self.elem is None:
            super(ListItem, self).setText("")
        else:
            if (new_text := self.elem.get(text)) is not None:
                self.current_display = text
                super(ListItem, self).setText(new_text)
