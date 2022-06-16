from sources.back.neo.neoobj import NeoType
from sources.ui.listview.list_view import ListView
from sources.ui.listview.mitigations.mitigation_options import MitigationOptions


##
# @ingroup mitigations
#

##
# MitigationListView
# Specific ListView for list of NeoObj type mitigation.
#
class MitigationListView(ListView):
    ##
    # MitigationListView Constructor.
    #
    # @param self The object pointer
    # @param content content of the list (list of NeoObj)
    # @param att display mode (id name ...) (str)
    # @param parent parent (QWidget)
    #
    def __init__(self, content=[], att="id_name", parent=None):
        super(MitigationListView, self).__init__(MitigationOptions, content, [], att, query_type=[NeoType.Technique], parent=parent)

