from sources.back.neo.neoobj import NeoType
from sources.ui.actions.mitigations_action import MitigationsAction
from sources.ui.actions.remove_action import RemoveAction
from sources.ui.listview.options import Options


##
# @ingroup techniques
#

##
# TechniqueOptions
# Options for Technique ListViews.
#
class TechniqueOptions(Options):
    ##
    # @var remove
    # RemoveAction
    #
    # @var mitigations
    # MitigationsAction
    #

    ##
    # MitigationOptions Constructor.
    #
    # @param self The object pointer
    # @param list_view listview where the menu is applied
    # @param remove bool is remove option available
    # @param query_type list of Neo type to create query options
    #
    def __init__(self, list_view, remove=False, query_type=NeoType.Technique):
        super(TechniqueOptions, self).__init__(list_view, query_type)

        # Remove Action
        self.remove = RemoveAction('Remove', self.list_view, self.popMenu, remove)
        self.select_one_actions.append(self.remove)

        # See Mitigation Action
        self.mitigations = MitigationsAction('See Mitigations', self.list_view, self.popMenu)

    ##
    # MitigationOptions on_context_menu method.
    # Display popMenu get the selected action and calls the behaviour of the action selected.
    # Show context menu if at least one selected.
    # @param self The object pointer
    # @param point Point where the menu is displayed
    #
    def on_context_menu(self, point):
        # show context menu if at least one selected
        if len(self.list_view.selectionModel().selectedIndexes()) > 0:
            super(TechniqueOptions, self).on_context_menu(point)
