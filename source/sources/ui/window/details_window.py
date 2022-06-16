from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Qt

from sources.back.neo.requests_groups import techniques_from_group
from sources.ui.actions.link_action import LinkAction
from sources.ui.display_options.display_button_box import DisplayButtonBox, default_display
from sources.ui.display_options.display_options import DisplayedObject, DisplayedType
from sources.ui.listview.techniques.technique_list_view import TechniqueListView
from sources.ui.window.section.alias import Alias


##
# @ingroup window
#

##
# DetailsWindow.
# Displays details about a specific group (NeoObj).
#
class DetailsWindow(QtWidgets.QDialog):
    ##
    # @var neo_obj
    # Group whose details are being displayed. (NeoObj with type group).
    #
    # @var techniques_filtered_view
    # ListView of the Techniques used by the group and contained in the technique list used as input.
    #
    # @var all_techniques_view
    # ListView of all the techniques used by the group.
    #
    # @var listView
    # ListView currently displayed.
    #
    # @var displayed_obj
    # Enum DisplayedObject representing the list displayed (filtered or all).
    #
    # @var displayed_type
    # Enum DisplayedType representing the current display mode.
    #
    # @var linkButton
    # Button linked to the page of Mitre Att&ck Website containing more details about the group.
    #
    # @var techniques_label
    # Label identifying the displayed list.
    #

    ##
    # DetailsWindow Constructor.
    # 
    # @param self The object pointer
    # @param neo_obj Group represented by a NeoObj (type: Group)
    # @param techniques Id of the input techniques (list of str)
    # @param parent Parent (QWidget)
    def __init__(self, neo_obj, techniques=None, parent=None):
        super(DetailsWindow, self).__init__(parent)
        self.neo_obj = neo_obj
        # get all techniques used by the group
        all_techniques = techniques_from_group(neo_obj.id)
        # techniques from input techniques used by the group
        filtered_techniques = techniques_from_group(neo_obj.id, techniques)

        # set ListView for filtered techniques and all techniques
        self.techniques_filtered_view = TechniqueListView(False,
                                                          filtered_techniques, self, filtered_techniques)
        self.all_techniques_view = TechniqueListView(False,
                                                     all_techniques, self, filtered_techniques)
        # set displayed techniques
        self.displayed_obj = DisplayedObject.Filtered
        # set displayed mode
        self.displayed_type = DisplayedType.IdName

        # Setting all window elements
        self.setLayout(QtWidgets.QVBoxLayout(self))
        self.setWindowTitle(neo_obj.get_id_name())

        # Title (name and id of the group)
        title = QtWidgets.QLabel(neo_obj.get_id_name(), self)
        font = title.font()
        font.setPointSize(20)
        font.setBold(True)
        title.setFont(font)

        # Go to Mitre Att&ck Website Button
        self.linkButton = QtWidgets.QToolButton(self.parent())
        self.linkButton.setDefaultAction(LinkAction("Go to MitreAtt&&ck Website", self.parent()))

        # Percentage of techniques from the group used
        percentage = QtWidgets.QLabel(str(int(len(self.techniques_filtered_view.get_items()) * 100.0 / len(
            self.all_techniques_view.get_items()))) + "% of techniques used", self)

        # Display option
        displayBox = DisplayButtonBox(self)

        # Widget to display the aliases (id no alias found return label 'No alias found')
        alias = Alias.get_alias_widget(self.neo_obj, self.parent())

        # Which type of techniques are currently displayed
        self.techniques_label = QtWidgets.QLabel("Techniques Used", self)

        # Current displayed ListView
        self.listView = self.techniques_filtered_view
        self.refresh()

        # button to choose which techniques to display
        buttonBox = QtWidgets.QDialogButtonBox(Qt.Horizontal, self)
        allButton = QtWidgets.QPushButton("All techniques")
        filterButton = QtWidgets.QPushButton("Only used techniques")
        buttonBox.addButton(filterButton, QtWidgets.QDialogButtonBox.ActionRole)
        buttonBox.addButton(allButton, QtWidgets.QDialogButtonBox.ActionRole)

        # Add widget to layout
        self.layout().addWidget(title)
        self.layout().addWidget(self.linkButton)
        self.layout().addWidget(percentage)
        self.layout().addWidget(alias)
        self.layout().addWidget(displayBox)
        self.layout().addWidget(self.techniques_label)
        self.layout().addWidget(self.all_techniques_view)
        self.layout().addWidget(self.techniques_filtered_view)
        self.layout().addWidget(buttonBox)

        # Connect buttons
        allButton.clicked.connect(self.display_all)
        filterButton.clicked.connect(self.display_filtered)
        self.linkButton.clicked.connect(self.link)

    ##
    # DetailsWindow link method.
    # Open the page of Mitre Att&ck Website dedicated to the specific groups (self.neo_obj).
    # @param self The object pointer
    @QtCore.Slot()
    def link(self):
        self.linkButton.defaultAction().action([self.neo_obj])

    ##
    # DetailsWindow display_all method.
    # Display all the techniques used by the group.
    # @param self The object pointer
    @QtCore.Slot()
    def display_all(self):
        if self.displayed_obj != DisplayedObject.All:
            self.displayed_obj = DisplayedObject.All
            self.refresh()

    ##
    # DetailsWindow display_filtered method.
    # Display the techniques used by the group that are lso contained in the technique input list.
    # @param self The object pointer
    @QtCore.Slot()
    def display_filtered(self):
        if self.displayed_obj != DisplayedObject.Filtered:
            self.displayed_obj = DisplayedObject.Filtered
            self.refresh()

    ##
    # DetailsWindow display_names method.
    # Displays the techniques by names.
    # @param self The object pointer
    @QtCore.Slot()
    def display_names(self):
        default_display(self, DisplayedType.Name)

    ##
    # DetailsWindow display_ids method.
    # Displays the techniques by ids.
    # @param self The object pointer
    @QtCore.Slot()
    def display_ids(self):
        default_display(self, DisplayedType.Id)

    ##
    # DetailsWindow display_id_name method.
    # Displays the techniques by ids and names.
    # @param self The object pointer
    @QtCore.Slot()
    def display_id_name(self):
        default_display(self, DisplayedType.IdName)

    ##
    # DetailsWindow refresh method.
    # Refresh the display of the listview.
    # @param self The object pointer
    def refresh(self):
        self.techniques_label.setText(self.displayed_obj.value)
        if self.displayed_obj == DisplayedObject.All:
            self.listView = self.all_techniques_view
            self.techniques_filtered_view.hide()
            self.listView.show()
        elif self.displayed_obj == DisplayedObject.Filtered:
            self.listView = self.techniques_filtered_view
            self.all_techniques_view.hide()
            self.listView.show()

        self.all_techniques_view.set_view(self.displayed_type.value)
        self.techniques_filtered_view.set_view(self.displayed_type.value)
