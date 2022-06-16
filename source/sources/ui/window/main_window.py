from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFileDialog

from sources.back.neo.mitre import last_version
from sources.back.neo.request_neo import get_version
from sources.back.static_class.config import Config, new_property, ask_dir_path, ask_file_path
from sources.back.exit_status import ExitStatus, Status
from sources.back.static_class.input import Input
from sources.ui.display_options.display_button_box import DisplayButtonBox
from sources.ui.listview.techniques.technique_list_view import TechniqueListView
from sources.ui.window.section.result import Result
from sources.back.tools import Tools


##
# @ingroup window
#

##
# MainWindow
# App main Window.
#
class MainWindow(QtWidgets.QMainWindow):
    ##
    # @var result
    # Result Section on the center (Result class).
    #
    # @var menu
    # Menu on top (QToolBar).
    #
    # @var techniques
    # Technique Section on the left (QToolBar).
    #
    # @var techniques_list
    # custom list view (TechniqueListView) representing the techniques given as input.
    #
    # @var configButton
    # Config settings (QToolButton).
    #
    # @var idButton
    # QRadioButton used to add the technique by id.
    #
    # @var nameButton
    # QRadioButton used to add the technique by name.
    #
    # @var lineEdit
    # QLineEdit used to add a single technique.

    ## 
    # MainWindow Constructor.
    # @param self The object pointer
    # @param icon Path to the icon of the window (str)
    def __init__(self, icon="eurocontrol.ico"):
        super(MainWindow, self).__init__()

        # Load Config
        Config().from_json(self)
        # Title and Icon of the Window
        self.setWindowTitle("AFiT")
        self.setWindowIcon(QtGui.QIcon(icon))
        self.setContextMenuPolicy(Qt.NoContextMenu)

        # Creating Widget for Main Window
        self.result = Result(self)
        self.menu = QtWidgets.QToolBar(self)
        self.menu.setMovable(False)
        self.menu.setWindowTitle("menu")
        self.techniques = QtWidgets.QToolBar(self)
        self.techniques.setMovable(False)
        self.techniques.setWindowTitle("techniques")

        # Adding Actions to the Menu (tool bar top)
        self.menu.addAction("Reset").setData(0)
        self.load = self.menu.addAction("Load Mitre Att&&ck Data")
        self.load.setData(1)
        self.menu.addAction("Open Neo4j Desktop").setData(2)
        self.menu.addAction("Start Neo4j DataBase").setData(3)
        self.menu.addAction("Stop Neo4j DataBase").setData(4)
        self.menu.addAction("Open Neo4j Browser").setData(5)

        self.configButton = QtWidgets.QToolButton(self.menu)
        self.configButton.setText("Edit Config")
        config_menu = QtWidgets.QMenu(self.menu)
        # create action (edit config and connect them to their methods_
        tech_dir_action = config_menu.addAction("Set techniques directory")
        tech_dir_action.triggered.connect(self.new_tech_dir)
        save_dir_action = config_menu.addAction("Set save directory")
        save_dir_action.triggered.connect(self.new_save_dir)
        neo_dir_action = config_menu.addAction("Set Neo4j directory")
        neo_dir_action.triggered.connect(self.new_neo_dir)
        neo_file_action = config_menu.addAction("Set Neo4j Desktop exe file")
        neo_file_action.triggered.connect(self.new_neo_file)
        # self._action = config_menu.actionTriggered.connect(self.config_trigger)
        self.configButton.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.configButton.setMenu(config_menu)
        self.configButton.setToolTip("Config")
        self.menu.addWidget(self.configButton)

        self.menu.actionTriggered.connect(self.on_actionTriggered)

        # Creating element for Techniques
        barTitle = QtWidgets.QLabel("Techniques", self.techniques)
        displayBox = DisplayButtonBox(self)
        self.techniques_list = TechniqueListView(remove=True, parent=self)
        self.lineEdit = QtWidgets.QLineEdit(self.techniques)
        addItem = QtWidgets.QLabel("Add Technique", self.techniques)
        addButton = QtWidgets.QPushButton("Add Item", self.techniques)
        openFileButton = QtWidgets.QPushButton("Open File", self.techniques)

        # Adding elements to Techniques (Toolbar Left)
        self.techniques.addWidget(barTitle)
        self.techniques.addWidget(displayBox)
        self.techniques.addWidget(self.techniques_list)
        self.techniques.addWidget(addItem)
        self.techniques.addWidget(self.lineEdit)
        self.techniques.addWidget(addButton)
        self.techniques.addWidget(openFileButton)

        # Adding Widgets to the Main Window
        self.setCentralWidget(self.result)  # Result
        self.addToolBar(Qt.TopToolBarArea, self.menu)
        self.addToolBar(Qt.LeftToolBarArea, self.techniques)

        addButton.clicked.connect(self.add)
        openFileButton.clicked.connect(self.open_file)

        Input.refresh_result = self.result.refresh_table
        Input.set_techniques(self.techniques_list)

    ## 
    # Override MainWindow closeEvent method.
    # Before closing the app a close confirmation is displayed and if the configuration has changed a message is 
    # displayed to ask if it should be saved.
    # @param self The object pointer
    # @param event
    def closeEvent(self, event):
        event.ignore()
        if Config().need_save() and QtWidgets.QMessageBox.question(self, "Config",
                                                                   "Configuration changed. Do you want to save it?",
                                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.Yes:
            Config().save()
        if QtWidgets.QMessageBox.question(self, "Close Confirmation", "Exit?",
                                          QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.Yes:
            event.accept()

    ##
    # MainWindow check_graph_version method.
    # Compare version of the graph and version of MitreAtt&ck.
    # Displays a message if an update is needed.
    # @param self The object pointer
    def check_graph_version(self):
        if (status := get_version(self)).is_ok():
            graph_version = status.content
            mitre_version = last_version()
            if graph_version != mitre_version:
                update = QtWidgets.QMessageBox.question(self, "New Att&ck version is available. Do you want to update Neo4j graph?", QtWidgets.QMessageBox.Yes,
                                                        QtWidgets.QMessageBox.No)
                if update == QtWidgets.QMessageBox.Yes:
                    Tools.load_ma(self)

    ## 
    # MainWindow on_actionTriggered method.
    # Link Menu (top) actions to their respective functions.
    # @param self The object pointer
    # @param action Action triggered
    @QtCore.Slot()
    def on_actionTriggered(self, action):
        if (x := action.data()) == 0:
            Tools.reset(self)
        elif x == 1:
            Tools.load_ma(self)
        elif x == 2:
            Tools.open_neo()
        elif x == 3:
            Tools.neo4j_command("start")
            # check version mitre Att&ck
            self.check_graph_version()
        elif x == 4:
            Tools.neo4j_command("stop")
        elif x == 5:
            Tools.open_neo_browser()

    ## 
    # MainWindow new_tech_dir method.
    # Set a new path for the technique directory.
    # @param self The object pointer
    @QtCore.Slot()
    def new_tech_dir(self):
        new_property("Techniques directory", ask_dir_path, False)

    ## 
    # MainWindow new_save_dir method.
    # Set a new path for the save directory.
    # @param self The object pointer
    @QtCore.Slot()
    def new_save_dir(self):
        new_property("Save directory", ask_dir_path, False)

    ## 
    # MainWindow new_save_dir method.
    # Set a new path for the Neo4j directory.
    # @param self The object pointer
    @QtCore.Slot()
    def new_neo_dir(self):
        new_property("Neo4j directory", ask_dir_path, False)

    ## 
    # MainWindow new_save_dir method.
    # Set a new path for the Neo4j Desktop executable file.
    # @param self The object pointer
    @QtCore.Slot()
    def new_neo_file(self):
        new_property("Neo4j Desktop executable file", ask_file_path, False)

    ##
    # MainWindow add method.
    # Add item form the Line Edit.
    # @param self The object pointer
    @QtCore.Slot()
    def add(self):
        x = self.lineEdit.text()
        self.lineEdit.clear()
        r = self.techniques_list.add_neo_obj(x)
        if r != ExitStatus(Status.Ok):
            err_text = str(r)
            if err_text == "":
                err_text = "Error while adding " + x
            self.techniques_list.msgBox.setText(err_text)
            self.techniques_list.msgBox.exec()
            self.techniques_list.msgBox.setDetailedText("")
        else:
            self.result.refresh_table()

    ##
    # MainWindow open_file method.
    # Add a list of items by opening a file
    # @param self The object pointer
    @QtCore.Slot()
    def open_file(self):
        file_window = QFileDialog(directory=Config().get_tech_dir(), parent=self)
        file_window.setFileMode(QFileDialog.ExistingFile)
        file_window.setNameFilter("Text (*.txt)")
        if file_window.exec():
            file = open(file_window.selectedFiles()[0], 'r')
            lines = file.readlines()
            res = []
            for i in lines:
                i = i.replace("\n", "")
                if len(i) != 0:
                    res.append(i)
            file.close()
            
            if (msg_box := self.techniques_list.add_list(res)) is not None:
                if msg_box.exec():
                    self.result.refresh_table()
                msg_box.setDetailedText("")
            else:
                self.result.refresh_table()
    ##
    # MainWindow display_names method.
    # Set and change the display of the technique list to names.
    # @param self The object pointer
    @QtCore.Slot()
    def display_names(self):
        self.techniques_list.set_view("name")

    ##
    # MainWindow display_ids method.
    # Set and change the display of the technique list to ids.
    # @param self The object pointer
    @QtCore.Slot()
    def display_ids(self):
        self.techniques_list.set_view("external_id")

    ##
    # MainWindow display_id_name method.
    # Set and change the display of the technique list to ids and names
    # @param self The object pointer
    @QtCore.Slot()
    def display_id_name(self):
        self.techniques_list.set_view("id_name")
