from sources.ui.actions.default_action import DefaultAction
from sources.ui.window.see_mitigation_window import MitigationWindow


##
# @ingroup actions
#

##
# MitigationsAction
# See Mitigations action.
#
class MitigationsAction(DefaultAction):
    ##
    # MitigationsAction Constructor.
    # @param self The object pointer
    # @param text Text display on the option
    # @param parent parent (QWidget)
    # @param menu QMenu of the action
    #
    def __init__(self, text, parent, menu=None):
        super(MitigationsAction, self).__init__(text, parent, menu)

    ##
    # MitigationsAction action_from_menu method.
    # apply the action to the selected items of the list
    # @param self The object pointer
    # @param selected_list list of the index of the selected items
    #
    def action_from_menu(self, selected_list=[]):
        techniques = [self.parent().get_items()[elem.row()] for elem in selected_list]
        MitigationWindow([item.elem for item in techniques], self.parent()).show()
