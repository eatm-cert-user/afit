from sources.back.neo.neoobj import NeoType
from sources.ui.listview.list_view import ListView
from sources.ui.listview.groups.group_options import GroupOptions


##
# @ingroup groups
#

##
# GroupListView
# Specific ListView for list of NeoObj type group.
#
class GroupListView(ListView):
    ##
    # GroupOptions Constructor.
    #
    # @param self The object pointer
    # @param content content of the list (list of NeoObj)
    # @param att display mode (id name ...) (str)
    # @param parent parent (QWidget)
    #
    def __init__(self, content=[], att="id_name", parent=None):
        super(GroupListView, self).__init__(GroupOptions, content, [], att,
                                            query_type=[NeoType.Technique, NeoType.Group], parent=parent)
