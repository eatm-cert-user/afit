from PySide6 import QtGui


##
# @ingroup actions
#

##
# DefaultAction
# default QAction for listview options.
#
class DefaultAction(QtGui.QAction):
    ##
    # @var menu
    # QMenu of the action
    #

    ##
    # DefaultAction Constructor.
    # @param self The object pointer
    # @param text Text display on the option
    # @param parent parent (QWidget)
    # @param menu QMenu of the action
    # @param show bool if True, the action add it self to the menu
    #
    def __init__(self, text, parent, menu=None, show=True):
        super(DefaultAction, self).__init__(text, parent)

        self.menu = menu
        # Add itself to menu if there is one
        if self.menu is not None and show:
            self.menu.addAction(self)

    ##
    # DefaultAction action_from_menu method.
    # apply the action to the selected items of the list
    # @param self The object pointer
    # @param selected_list list of the index of the selected items
    #
    def action_from_menu(self, selected_list=[]):
        pass

    ##
    # DefaultAction action method.
    # apply the action to the obj
    #
    # @param self The object pointer
    # @param obj_list list of NeoObj
    #
    def action(self, obj_list):
        pass
