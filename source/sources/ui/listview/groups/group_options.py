from sources.back.neo.neoobj import NeoType
from sources.ui.actions.details_action import DetailsAction
from sources.ui.listview.options import Options


##
# @ingroup groups
#

##
# GroupOptions
# Options for Group ListViews.
#
class GroupOptions(Options):
    ##
    # @var details
    # Show Detail Option
    #

    ##
    # GroupOptions Constructor.
    # 
    # @param self The object pointer
    # @param list_view listview where the menu is applied
    # @param remove bool is remove option available
    # @param query_type list of Neo type to create query options
    #
    def __init__(self, list_view, remove=False, query_type=[NeoType.Technique]):
        super(GroupOptions, self).__init__(list_view, query_type)

        # ShowDetails Action
        self.details = DetailsAction('Show Details', self.list_view, self.popMenu)
        self.select_one_actions.append(self.details)

    ##
    # GroupOptions on_context_menu method.
    # Display popMenu get the selected action and calls the behaviour of the action selected.
    # @param self The object pointer
    # @param point Point where the menu is displayed
    #
    def on_context_menu(self, point):
        # show context menu only if one selected
        # if len(self.list_view.selectionModel().selectedIndexes()) == 1:
        super(GroupOptions, self).on_context_menu(point)
