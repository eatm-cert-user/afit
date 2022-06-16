from PySide6.QtGui import QDesktopServices

from sources.ui.actions.default_action import DefaultAction


##
# @ingroup actions
#

##
# LinkAction
# Action Link (Go to Mitre Atta&ck Website).
#
class LinkAction(DefaultAction):
    ##
    # LinkAction Constructor.
    # @param self The object pointer
    # @param text Text display on the option
    # @param parent parent (QWidget)
    # @param menu QMenu of the action
    #
    def __init__(self, text, parent, menu=None):
        super(LinkAction, self).__init__(text, parent, menu)

    ##
    # LinkAction action_from_menu method.
    # apply the action to the selected items of the list
    # @param self The object pointer
    # @param selected_list list of the index of the selected items
    #
    def action_from_menu(self, selected_list=[]):
        if len(selected_list) == 1:
            self.action([self.parent().get_items()[selected_list[0].row()].elem])
        else:
            self.parent().msgBox.setText("Select only one item")
            self.parent().msgBox.exec()
            self.parent().msgBox.setText("")

    ##
    # LinkAction action method.
    # apply the action to the obj
    #
    # @param self The object pointer
    # @param obj_list list of NeoObj
    #
    def action(self, obj_list):
        QDesktopServices.openUrl(obj_list[0].get_link())



