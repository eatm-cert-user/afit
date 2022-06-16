from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFileDialog

from sources.back.static_class.config import Config
from sources.back.exit_status import ExitStatus, Status
from sources.back.file_type import FileType
from sources.back.save_result import SaveResult


##
# @ingroup window
#

##
# SaveWindow.
# Dialog window to save the result table.
#
class SaveWindow(QtWidgets.QDialog):
    ##
    # @var results
    # Result table (type list) (from Result Section).
    #
    # @var path
    # Path to the location of the file where the result will be saved. (str)
    #
    # @var msgBox
    # Message Box in case of error.
    #
    # @var file_type
    # Enum FileType to represent the extension of the file.
    #
    # @var path_label
    # Label used to display the path selected.
    #
    # @var sep_edit
    # Line Edit to choose the separator (Csv files)
    #
    # @var sep_widget
    # Widget containing a label 'Separator' and the line edit for the separator.
    # (hidden if the file selected is not a Csv file)
    #
    # @var row_limit
    # QSpinBox to selected the number of rows of the table to save.
    # If the number of rows is 0, all of them will be saved.
    #

    ##
    # SaveWindow Constructor.
    # 
    # @param self The object pointer
    # @param results Result table
    # @param parent Parent QWidget
    def __init__(self, results, parent=None):
        super(SaveWindow, self).__init__(parent=parent)
        self.results = results
        self.path = None
        self.msgBox = QtWidgets.QMessageBox(self)
        self.msgBox.setText("Invalid Path")

        # Type of selected file (none selected so invalid)
        self.file_type = FileType.Invalid

        # Setting window layout and title
        self.setLayout(QtWidgets.QVBoxLayout(self))
        self.setWindowTitle("Save Results")

        # Select Path Label
        select_path_label = QtWidgets.QLabel("Select Path", self)
        self.layout().addWidget(select_path_label)

        # Choose File
        file_layout = QtWidgets.QHBoxLayout()
        file_layout.addWidget(QtWidgets.QLabel("Path: ", self))
        self.path_label = QtWidgets.QLabel("No File", self)
        file_layout.addWidget(self.path_label)
        select_path_button = QtWidgets.QPushButton("Select Path", self)
        select_path_button.clicked.connect(self.select_path)
        file_layout.addWidget(select_path_button, alignment=Qt.AlignLeft)
        # add to layout
        tmp = QtWidgets.QWidget(self)
        tmp.setLayout(file_layout)
        self.layout().addWidget(tmp)

        # Choose Separator (should be displayed only for Csv files)
        sep_layout = QtWidgets.QHBoxLayout()
        sep_layout.addWidget(QtWidgets.QLabel("Separator: ", self))
        self.sep_edit = QtWidgets.QLineEdit(";", self)
        self.sep_edit.setMaxLength(1)
        sep_layout.addWidget(self.sep_edit, alignment=Qt.AlignLeft)

        # add to layout
        self.sep_widget = QtWidgets.QWidget(self)
        self.sep_widget.setLayout(sep_layout)
        self.layout().addWidget(self.sep_widget)
        self.sep_widget.hide()

        # Count limit
        self.layout().addWidget(QtWidgets.QLabel("Enter Row limit"))
        self.row_limit = QtWidgets.QSpinBox(self)
        self.row_limit.setMinimum(0)
        self.row_limit.setValue(0)
        self.layout().addWidget(self.row_limit)

        # Button Accept Cancel
        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, self)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        self.layout().addWidget(button_box)

    ##
    # SaveWindow select_path method.
    # Show a File Dialog to select the path where the results will be saved.
    # File Extension available: Csv (the file extension will determine also the format of the content of the file)
    # Accept Mode: Accept Save (will display a confirmation message before selecting an existing file)
    # Connected to select_path_button.
    # @param self The object pointer
    @QtCore.Slot()
    def select_path(self):
        file_window = QFileDialog(directory=Config().get_save_dir(), parent=self)
        # set file mode to anyfile (select a file, whether it exists or not)
        file_window.setFileMode(QFileDialog.AnyFile)
        file_window.setNameFilters(["CSV (Comma delimited) (*.csv)"])
        file_window.setAcceptMode(QFileDialog.AcceptSave)
        # if a file is selected an the extension is valid
        if file_window.exec() and (file_type := FileType.to_file_type(file_window.selectedNameFilter())) != FileType.Invalid:
            self.file_type = file_type
            self.path = file_window.selectedFiles()[0]
            self.path_label.setText(file_window.selectedFiles()[0])
            # Separator is only use for csv file. if selected file is not of type csv the separator widget is hide
            if self.file_type == FileType.Csv:
                self.sep_widget.show()
            else:
                self.sep_widget.hide()

    ##
    # Override exec method.
    # Get the result of exec function and convert it into Exit Status Ok or Cancel
    # @param self The object pointer
    # @return ExitStatus
    def exec(self):
        return ExitStatus(Status.Ok, "Results saved", parent=self.parent()) \
            if super(SaveWindow, self).exec() == 1 else ExitStatus(Status.Cancel, parent=self.parent())

    ##
    # Override accept method.
    # Created SaveResult, open the selected file and write results.
    # If error opens a message box.
    # @param self The object pointer
    def accept(self):
        if self.path is not None and self.file_type != FileType.Invalid:
            # Create new instance of SaveResult
            res = SaveResult(self.results, self.path, self.file_type, self.row_limit.value(), self.sep_edit.text(), self.parent())
            # open file from path
            try:
                save_file = open(self.path, "w")
            except Exception as e:
                self.msgBox.setText(str(e))
                self.msgBox.exec()
                return
            # write str(SaveResult) in file
            text = str(res)
            save_file.write(text)
            save_file.close()
            super(SaveWindow, self).accept()
        else:
            self.msgBox.exec()
