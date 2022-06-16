from PySide6.QtWidgets import QAbstractItemView

from sources.back.exit_status import ExitStatus, Status
from sources.back.neo.neoobj import NeoType
from sources.back.neo.query import Query
from sources.back.neo.request_neo import get_data, run_single_result
from sources.ui.listview.list_view import ListView
from sources.ui.listview.list_item import ListItem
from sources.ui.listview.techniques.technique_options import TechniqueOptions


##
# @ingroup techniques
#

##
# TechniqueListView
# Specific ListView for list of NeoObj type technique.
#
class TechniqueListView(ListView):
    ##
    # TechniqueListView Constructor.
    #
    # @param self The object pointer
    # @param remove is the remove option available (boolean)
    # @param content content of the list (list of NeoObj)
    # @param view display mode (id name ...) (str)
    # @param parent parent (QWidget)
    #
    def __init__(self, remove=False, content=[], parent=None, bold=[], view="id_name"):
        super(TechniqueListView, self).__init__(TechniqueOptions, content, bold, view,
                                                QAbstractItemView.MultiSelection, remove,
                                                [NeoType.Group, NeoType.Mitigation, NeoType.All], parent)

    ##
    # TechniqueListView add_neo_obj method.
    # Find node in the database, create NeoObj and add it to the list view
    #
    # @param self The object pointer
    # @param value value to identify the node (str)
    # @param field type of the value (name, external_id...) (str)
    #
    def add_neo_obj(self, value):

        if value[0] == "T" and value[1].isdigit():
            field = "external_id"
        else:
            field = "name"
        query = Query(node_input="Technique", input_type=field, input_value=value, node_output="None")
        obj = get_data(run_single_result, query, self.parent(), query.input_column)
        if obj == ExitStatus(Status.Ok):
            if obj.content in [item.elem for item in self.get_items()]:
                return ExitStatus(Status.Error, obj.content.get("id_name") + " already exists", self.parent())
            self.add_item(ListItem(obj.content, self.current_view))
        return obj

    ##
    # TechniqueListView add_list method.
    # Find nodes in the database, create NeoObj for all of them and add them to the list view
    #
    # @param self The object pointer
    # @param list list of values to identify the nodes (list of str)
    # @param field type of value (name, external_id...) (str)
    #
    def add_list(self, list):
        err = ""
        count = 0
        for e in list:
            status = self.add_neo_obj(e)
            if status != ExitStatus(Status.Ok):
                err += ("Error while adding " + e + "\n") if str(status) == "" else str(status) + "\n"
                count += 1
            if status == ExitStatus(Status.Error) and str(status) == "Connection failed":
                return status
        if count > 0:
            self.msgBox.setText("Couldn't add " + str(count) + " elements")
            self.msgBox.setDetailedText(err)
            self.msgBox.layout().setColumnMinimumWidth(1, 400)
            return self.msgBox
        return None
