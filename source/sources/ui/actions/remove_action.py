from PySide6 import QtWidgets

from sources.back.static_class.input import Input
from sources.ui.actions.default_action import DefaultAction


##
# @ingroup actions
#

##
# RemoveAction
# Remove action.
#
class RemoveAction(DefaultAction):
    ##
    # RemoveAction Constructor.
    # @param self The object pointer
    # @param text Text display on the option
    # @param node_output Type of the query node output
    # @param parent parent (QWidget)
    # @param menu QMenu of the action
    # @param show bool if True, the action add it self to the menu
    #
    def __init__(self, text, parent, menu=None, show=False):
        super(RemoveAction, self).__init__(text, parent, menu, show)

    ##
    # RemoveAction action_from_menu method.
    # apply the action to the selected items of the list
    # @param self The object pointer
    # @param selected_list list of the index of the selected items
    #
    def action_from_menu(self, selected_list=[]):
        if len(selected_list) == 1:
            index = selected_list[0].row()
            technique = self.parent().get_items()[index].elem
            # Confirmation
            answer = QtWidgets.QMessageBox.question(self.parent().parent(),
                                                    "Remove Confirmation",
                                                    "Are you sure you want to remove technique " + technique.get(
                                                        "id_name") + "?",
                                                    QtWidgets.QMessageBox.Yes,
                                                    QtWidgets.QMessageBox.No)
            if answer == QtWidgets.QMessageBox.Yes:
                # remove from list_view
                self.parent().model().takeRow(index)
                # self.parent().list.pop(index)
                # refresh table
                Input.refresh_result()
                # self.parent().refresh_res()
        else:
            self.parent().msgBox.setText("Select only one item")
            self.parent().msgBox.exec()
            self.parent().msgBox.setText("")
