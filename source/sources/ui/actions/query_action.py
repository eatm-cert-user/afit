from PySide6.QtWidgets import QApplication

from sources.back.neo.query import Query
from sources.ui.actions.default_action import DefaultAction


##
# @ingroup actions
#

##
# QueryAction
# Generate query action.
#
class QueryAction(DefaultAction):
    ##
    # @var node_output
    # Type of the query node output
    #

    ##
    # QueryAction Constructor.
    # @param self The object pointer
    # @param text Text display on the option
    # @param node_output Type of the query node output
    # @param parent parent (QWidget)
    # @param menu QMenu of the action
    #
    def __init__(self, text, parent, node_output, menu=None):
        super(QueryAction, self).__init__(text, parent, menu)
        self.node_output = node_output

    ##
    # QueryAction action_from_menu method.
    # apply the action to the selected items of the list
    # @param self The object pointer
    # @param selected_list list of the index of the selected items
    #
    def action_from_menu(self, selected_list=[]):
        # get selected techniques
        selected_items = [self.parent().get_items()[elem.row()] for elem in selected_list]
        query = Query(empty=True)
        for elem in [item.elem for item in selected_items]:
            other = Query(input_obj=elem, node_output=self.node_output)
            query = query.union(other)
        if (query_str := str(query)) != "":
            QApplication.clipboard().setText(query_str)
