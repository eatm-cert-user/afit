import os
import platform

from PySide6 import QtWidgets
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QApplication

from sources.back.static_class.config import Config, new_property, ask_file_path, ask_dir_path
from sources.back.neo.mitre import import_mitre, last_version
from sources.back.neo.request_neo import get_version
from sources.ui.listview.groups.group_list_view import GroupListView


##
# @ingroup back
#


##
# Tools.
# Function used to create result table and the functions linked to Menu on top.
#
class Tools:
    ##
    # get_display_list function.
    # Create the Result Table
    # @param groups List of groups and their corresponding number of matching techniques
    # @param att Display mode
    # @param parent Parent QWidget
    # @return list[list[int, listView]]
    #
    @staticmethod
    def get_display_list(groups, att, parent=None):
        res = []
        for e in groups:
            if e:
                res.append([e[0], GroupListView(e[1], att, parent)])
        return res

    ##
    # reset function.
    # Reset Technique List and Table Result.
    #
    @staticmethod
    def reset(main_window):
        main_window.techniques_list.clear()
        main_window.result.refresh_table()

    ##
    # load_ma function.
    # Load Mitre Att&ck data in neo4j.
    #
    @staticmethod
    def load_ma(main_window):
        msg_wait = QtWidgets.QDialog(parent=main_window)
        msg_wait.setLayout((layout := QtWidgets.QVBoxLayout(msg_wait)))
        layout.addWidget((label := QtWidgets.QLabel("Loading Mitre Att&ck Data... Please wait.")))
        msg_wait.setWindowTitle("Loading Mitre Att&ck Data")
        msg_wait.show()
        QApplication.processEvents()
        res = import_mitre()
        msg_wait.hide()
        msg_box = QtWidgets.QMessageBox(main_window)
        msg_box.setWindowTitle("Load Mitre Att&ck Data")
        msg_box.setText(res)
        msg_box.exec()

    ##
    # open_neo_browser function.
    # Open Neo4j Browser.
    #
    @staticmethod
    def open_neo_browser():
        QDesktopServices.openUrl("http://localhost:7474/browser/")

    ##
    # neo4j_command function.
    # Run a Neo4j command.
    #
    # @param command Command (str) (ex: start, stop, status)
    #
    @staticmethod
    def neo4j_command(command):

        if (system := platform.system()) == 'Windows':
            try:
                if command == "start" and os.system(Tools.neo4j_windows('status')) == 0:
                    return
                elif (res := os.system(Tools.neo4j_windows(command))) == 1 and new_property("Neo4j directory", ask_dir_path):
                    if command == "start":
                        os.system(Tools.neo4j_windows("install-service"))
                    Tools.neo4j_command(command)
                else:
                    if command == "start":
                        os.system(Tools.neo4j_windows("install-service"))
                        os.system(Tools.neo4j_windows(command))

                    # print(res)

            except Exception:
                if new_property("Neo4j directory", ask_dir_path):
                    Tools.neo4j_command(command)

        elif system == 'Linux':
            os.system(Tools.neo4j_linux(command))

    ##
    # neo4j_windows function.
    # Run a Neo4j command for Windows System.
    #
    # @param command Command (str) (ex: start, stop, status)
    #
    @staticmethod
    def neo4j_windows(command):
        print("--------------------------- "+command)
        neo4j_folder = Config().get_neo_dir()
        return 'cmd /c ""' + neo4j_folder + '\\bin\\neo4j\" ' + command + '\"'

    ##
    # neo4j_linux function.
    # Run a Neo4j command for Linux System.
    #
    # @param command Command (str) (ex: start, stop, status)
    #
    @staticmethod
    def neo4j_linux(command):
        return 'systemctl ' + command + ' neo4j.service'

    ##
    # open_neo function.
    # Open Neo4j Desktop.
    #
    @staticmethod
    def open_neo():
        neo_exe = Config().get_neo_exe()
        try:
            if neo_exe is not None:
                os.startfile(neo_exe)
        except Exception:
            if new_property("Neo4j Desktop executable file", ask_file_path):
                Tools.open_neo()
