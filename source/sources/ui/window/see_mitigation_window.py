from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from sources.back.neo.query import Query
from sources.back.neo.request_neo import get_data, run_mult_result
from sources.ui.display_options.display_button_box import DisplayButtonBox, default_display
from sources.ui.display_options.display_options import DisplayedType
from sources.ui.listview.list_item import ListItem
from sources.ui.listview.technique_mitigation_view import TechniqueMitigationView


##
# @ingroup window
#

##
# MitigationWindow.
# Window used to display techniques and mitigations.
#
class MitigationWindow(QtWidgets.QDialog):
    ##
    # MitigationWindow Constructor.
    # create new Mitigation Window, find the mitigations related to the techniques given.
    # @param self The object pointer
    # @param list of techniques (techniques are represented by NeoObj)
    # @param parent QWidget parent of the MitigationWindow
    def __init__(self, techniques, parent=None):
        ##
        # @var displayed_type
        # Enum DisplayedType representing the current display mode.
        #
        # @var dict_mitig
        # Dictionary (key: technique (NeoObj), value: list of related mitigations (list of NeoObj)).
        #
        # @var dict_query
        # Dictionary (key: technique (NeoObj), value: corresponding query to find related mitigations (Query)).
        #
        # @var list_views
        # Widget (TechniqueMitigationView class) to display both listviews and their label.
        #
        # @var query
        # Query class representing a query.
        #
        # @var queryText
        # Text zone (QTextEdit) to display the query (if query is empty, queryText will be hidden).

        super(MitigationWindow, self).__init__(parent)
        self.setWindowTitle("Mitigation Window")

        self.displayed_type = DisplayedType.IdName

        self.dict_query = {}
        self.dict_mitig = {}

        # Adding data to dictionaries
        for tech in techniques:
            query = Query(input_obj=tech, node_output="Mitigation")
            if (status := get_data(run_mult_result, query, parent, query.result_column)).is_ok():
                self.dict_query[tech] = query
                self.dict_mitig[tech] = status.content
            else:
                status.exec()

        self.setLayout(QtWidgets.QVBoxLayout(self))

        # Manage Background color
        colorButton = QtWidgets.QPushButton("Set background", self)
        resetButton = QtWidgets.QPushButton("Reset background", self)
        # use a button box
        buttonBox = QtWidgets.QDialogButtonBox(Qt.Horizontal, self)
        buttonBox.addButton(colorButton, QtWidgets.QDialogButtonBox.ActionRole)
        buttonBox.addButton(resetButton, QtWidgets.QDialogButtonBox.ActionRole)
        # Connect buttons
        colorButton.clicked.connect(self.color)
        resetButton.clicked.connect(self.reset_color)
        self.layout().addWidget(buttonBox)

        # Display Options
        displayBox = DisplayButtonBox(self)
        self.layout().addWidget(displayBox)

        self.list_views = TechniqueMitigationView(self.dict_mitig, parent)
        self.layout().addWidget(self.list_views)

        # Query Buttons
        queryButton = QtWidgets.QPushButton("Generate query", self)
        copyButton = QtWidgets.QPushButton("Copy query", self)
        hideButton = QtWidgets.QPushButton("Hide query", self)
        # use a button box
        buttonBox = QtWidgets.QDialogButtonBox(Qt.Horizontal, self)
        buttonBox.addButton(queryButton, QtWidgets.QDialogButtonBox.ActionRole)
        buttonBox.addButton(copyButton, QtWidgets.QDialogButtonBox.ActionRole)
        buttonBox.addButton(hideButton, QtWidgets.QDialogButtonBox.ActionRole)
        self.layout().addWidget(buttonBox)

        # Query and its display zone (if query is empty, queryText will be hidden)
        self.query = Query(empty=True)
        self.queryText = QtWidgets.QTextEdit("", self)
        self.queryText.setReadOnly(True)
        self.queryText.setAcceptRichText(True)
        self.layout().addWidget(self.queryText)
        self.queryText.hide()

        # Connect buttons
        queryButton.clicked.connect(self.generate_query)
        copyButton.clicked.connect(self.copy)
        hideButton.clicked.connect(self.hide_query)

    ##
    # MitigationWindow generate_query method.
    # Generate a Query to display all selected techniques (or all techniques in the list if non is selected) and all
    # related mitigation and display it in a TextEdit.
    # Connected to queryButton (see Constructor __init__).
    # @param self The object pointer
    @QtCore.Slot()
    def generate_query(self):
        query = Query(empty=True)
        select = [obj.elem for obj in self.list_views.get_selected_techniques()]
        for elem in self.dict_query.keys():
            if elem in select or len(select) == 0:
                query = query.union(self.dict_query.get(elem))
        self.query = query
        self.queryText.setText(str(query) if query is not None else "")
        self.queryText.show()

    ##
    # MitigationWindow copy method.
    # Copy the query if it has been generated
    # Connected to copyButton (see Constructor __init__).
    # @param self The object pointer
    @QtCore.Slot()
    def copy(self):
        if self.query is not None:
            QApplication.clipboard().setText(str(self.query))

    ##
    # MitigationWindow hide_query method.
    # Hide the TextEdit where the query is displayed and resets the query.
    # Connected to hideButton (see Constructor __init__).
    # @param self The object pointer
    @QtCore.Slot()
    def hide_query(self):
        self.query = None
        self.queryText.setText("")
        self.queryText.hide()

    ##
    # MitigationWindow color method.
    # Open Color Dialog and change color background of selected techniques (or all techniques if none is selected)
    # and their related mitigations.
    # Connected to colorButton (see Constructor __init__).
    # @param self The object pointer
    @QtCore.Slot()
    def color(self):
        color = QtWidgets.QColorDialog.getColor(parent=self, title="Choose background color")
        select = self.list_views.get_selected_techniques()
        if len(select) == 0:
            items = self.list_views.get_all()
        else:
            items = []
            for current in select:
                items.append(current)
                mitig = current if not isinstance(current, ListItem) else self.dict_mitig.get(current.elem)
                for e in mitig:
                    items.append(e)
        self.list_views.color(items, color)

    ##
    # MitigationWindow reset_color method.
    # Set the background color to the default color for all items in both listview
    # Connected to resetButton (see Constructor __init__).
    # @param self The object pointer
    @QtCore.Slot()
    def reset_color(self):
        self.list_views.color(self.list_views.get_all(), QtGui.QStandardItem().background())

    ##
    # MitigationWindow display_names method.
    # Change the current display of both list to name and refresh display of all items.
    # Connected to displayBox (see Constructor __init__).
    # @param self The object pointer
    @QtCore.Slot()
    def display_names(self):
        default_display(self, DisplayedType.Name)

    ##
    # MitigationWindow display_ids method.
    # Change the current display of both list to id (external_id) and refresh display of all items.
    # Connected to displayBox (see Constructor __init__).
    # @param self The object pointer
    @QtCore.Slot()
    def display_ids(self):
        default_display(self, DisplayedType.Id)

    ##
    # MitigationWindow display_id_name method.
    # Change the current display of both list to id (external_id) and name and refresh display of all items.
    # Connected to displayBox (see Constructor __init__).
    # @param self The object pointer
    @QtCore.Slot()
    def display_id_name(self):
        default_display(self, DisplayedType.IdName)

    ##
    # MitigationWindow refresh method.
    # Refresh display of items in both listview.
    # @param self The object pointer
    def refresh(self):
        for elem in self.list_views.get_all():
            elem.setText(self.displayed_type.value)
