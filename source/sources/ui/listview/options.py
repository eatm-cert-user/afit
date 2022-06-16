from PySide6 import QtCore
from PySide6.QtWidgets import QMenu

from sources.ui.actions.default_action import DefaultAction
from sources.ui.actions.link_action import LinkAction
from sources.ui.actions.query_action import QueryAction


##
# @ingroup listview
#

##
# Options
# Menu use in ListView.
#
class Options:
    ##
    # @var list_view
    # list view to which the menu is added
    #
    # @var popMenu
    # QMenu for the listview
    #
    # @var select_one_actions
    # list of action to display only if one item is selected
    #
    # @var link
    # Go to Mitre Att&ck Website (LinkAction)
    #
    # @var query
    # dictionary link a type of NeoObj with their corresponding query action (dict <NeoType, QueryAction>)
    #

    ##
    # Options Constructor.
    # 
    # @param self The object pointer
    # @param list_view listview where the menu is applied
    # @param query_type list of Neo type to create query options
    def __init__(self, list_view, query_type):
        self.list_view = list_view

        # set item context menu policy
        self.list_view.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.list_view.customContextMenuRequested.connect(self.on_context_menu)
        # create context menu
        self.popMenu = QMenu(self.list_view)
        self.select_one_actions = []

        # Action for all List type (either group or techniques)
        # Link to mitre Att&ck Action
        self.link = LinkAction('Go to MitreAtt&&ck Website', self.list_view, self.popMenu)
        self.select_one_actions.append(self.link)

        # Generate Query Action
        self.query = {}  # QueryAction('Generate Query', self.list_view, NeoType.Group.value, self.popMenu)

        for node_type in query_type:
            self.add_query_action(node_type)

        self.popMenu.addSeparator()

    ##
    # Options add_query_action method.
    # Generate Query Action for the menu
    # @param self The object pointer
    # @param node_output type of query to generate
    def add_query_action(self, node_output):
        # Generate Query Action
        if self.query.get(node_output) is None:
            self.query[node_output] = (
                QueryAction('Generate Query (relation with ' + node_output.value + ')', self.list_view,
                            node_output.value, self.popMenu))

    ##
    # Options on_context_menu method.
    # Display popMenu get the selected action and calls the behaviour of the action selected.
    # @param self The object pointer
    # @param point Point where the menu is displayed
    def on_context_menu(self, point):
        # show context menu only if one selected
        selected = self.list_view.selectionModel().selectedIndexes()
        if len(selected) == 0:
            return
        self.set_visibility(selected)
        action = self.popMenu.exec_(self.list_view.mapToGlobal(point))
        # Checks if action is a Default Action
        if isinstance(action, DefaultAction):
            action.action_from_menu(selected)

    ##
    # Options set_visibility method.
    # The action available for only one item selected are not displayed if the length of selected item is different
    # than 1
    # @param self The object pointer
    # @param selected list of selected items
    def set_visibility(self, selected):
        for action in self.select_one_actions:
            action.setVisible(len(selected) == 1)
