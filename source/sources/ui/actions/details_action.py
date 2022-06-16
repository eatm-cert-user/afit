from sources.ui.actions.default_action import DefaultAction
from sources.ui.window.details_window import DetailsWindow
from sources.ui.window.main_window import Input


##
# @ingroup actions
#

##
# DetailsAction
# Action Show details.
#
class DetailsAction(DefaultAction):
    ##
    # DetailsAction Constructor.
    # @param self The object pointer
    # @param text Text display on the option
    # @param parent parent (QWidget)
    # @param menu QMenu of the action
    #
    def __init__(self, text, parent, menu=None):
        super(DetailsAction, self).__init__(text, parent, menu)

    ##
    # DetailsAction action_from_menu method.
    # apply the action to the selected items of the list
    # @param self The object pointer
    # @param selected_list list of the index of the selected items
    #
    def action_from_menu(self, selected_list=[]):
        DetailsWindow(self.parent().get_items()[selected_list[0].row()].elem, Input.get_techniques().get_ids(),
                      self.parent()).show()
