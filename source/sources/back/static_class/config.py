import json

from PySide6 import QtWidgets
from PySide6.QtCore import QDir

from sources.back.exit_status import ExitStatus, Status


##
# @ingroup static_class
#

##
# get_config() function.
# Return Config with property from config.json
def get_config():
    try:
        json_file = open("config.json", 'r')
    except FileNotFoundError:
        print("Config not found")
        return None
    try:
        data = json.load(json_file)
    except json.decoder.JSONDecodeError:
        json_file.close()
        return None
    json_file.close()
    return data


##
# @ingroup static_class
#

##
# add_property function.
# Display a message asking if the user wants to change 'prop'
# @param prop str, name of the property
# @param parent Parent (QWidget)
def add_property(prop, parent=None):
    # Work without parent but no icon
    # msg_box = QtWidgets.QMessageBox(parent)
    reply = QtWidgets.QMessageBox.question(parent, "Config", prop + " not found.\nDo you want to add one?",
                                           QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
    return reply == QtWidgets.QMessageBox.Yes


##
# @ingroup static_class
#

##
# Open File Dialog to select an Executable File
# @param parent Parent (QWidget)
# @return ExitStatus
#
def ask_file_path(parent=None):
    file_window = QtWidgets.QFileDialog(parent)
    file_window.setFileMode(QtWidgets.QFileDialog.ExistingFile)
    file_window.setFilter(QDir.Executable | QDir.Files)
    if file_window.exec():
        return ExitStatus(Status.Ok, file_window.selectedFiles()[0], parent=parent)
    return ExitStatus(Status.Cancel, parent=parent)


##
# @ingroup static_class
#

##
# Open File Dialog to select an Existing Directory
# @param parent Parent (QWidget)
# @return ExitStatus
#
def ask_dir_path(parent=None):
    file_window = QtWidgets.QFileDialog(parent)
    file_window.setFileMode(QtWidgets.QFileDialog.Directory)
    file_window.setFilter(QDir.Dirs)
    if file_window.exec():
        return ExitStatus(Status.Ok, file_window.selectedFiles()[0], parent=parent)
    return ExitStatus(Status.Cancel, parent=parent)


##
# @ingroup static_class
#

##
# new_property function.
# Ask the user for a new value for a specific property.
# @param name Name of the property
# @param method function used to ge ta new value for the property
# @param confirm True if a confirmation message must be displayed before asking for a new value.
# @return bool
#
def new_property(name, method, confirm=True):
    if confirm:
        if not add_property(name, Config().get_parent()):
            return False
    if (exe := method(Config().get_parent())).is_ok():
        Config().set(name, str(exe))
        return True
    return False


##
# @ingroup static_class
#

##
# Singleton decorator for Config
#
def singleton(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance


##
# @ingroup static_class
#

##
# Config class.
# Singleton (only one instance of this class) calling multiple time the constructor will return the existing instance.
# Use for the configuration of the app
#
@singleton
class Config:
    ##
    # NeoConfig class.
    # Contain information about neo4j installation
    # @param self The object pointer
    # @var __exe_file Path to Neo4j executable file
    # @var __neo_dir Path to Neo4j directory
    #
    class Neo4jConfig:
        ##
        # Neo4jConfig Constructor.
        # @param self The object pointer
        # @param exe_file Path to Neo4j executable file
        # @param neo_dir Path to Neo4j directory
        #
        def __init__(self, exe_file=None, neo_dir=None):
            self.__exe_file = exe_file
            self.__neo_dir = neo_dir

        ##
        # __dict__ method.
        # Return all the properties of the Neo4jConfig in a dictionary.
        # @param self The object pointer
        # @return dict
        #
        def __dict__(self):
            return {
                "exe_file": self.__exe_file,
                "neo_dir": self.__neo_dir
            }

        ##
        # Set properties with data found in 'json'. If json is None or the properties are not found the values will
        # remain unchanged.
        # @param json
        # @return self
        #
        def from_json(self, json):
            if json is not None:
                if (dir := json.get("neo_dir")) is not None:
                    self.__neo_dir = dir
                if (exe := json.get("exe_file")) is not None:
                    self.__exe_file = exe
            return self

        ##
        # Neo4jConfig get_exe_file method.
        # Return the path to Neo4j Executable file. If none if found the user will be ask if he wants to add one.
        # @param self The object pointer
        # @return str
        #
        def get_exe_file(self):
            if self.__exe_file is None and not new_property("Neo4j Desktop executable file", ask_file_path):
                return None
            return self.__exe_file

        ##
        # Neo4jConfig set_exe_file method.
        # Set a new path to Neo4j executable file and set the save option of Config to True
        # (see var __save in Config class).
        # @param self The object pointer
        # @param file New path to the Neo4j executable file
        def set_exe_file(self, file):
            self.__exe_file = file
            Config().set_save()

        ##
        # Neo4jConfig get_neo_dir method.
        # Returns the path to neo4j root directory
        # @param self The object pointer
        # @return str
        def get_neo_dir(self):
            return self.__neo_dir

        ##
        # Neo4jConfig set_neo_dir method.
        # Set the path to neo4j root directory and set the save option of Config to True.
        # (see var __save in Config class).
        # @param self The object pointer
        # @param dir New path to neo4j root directory (str)
        def set_neo_dir(self, dir):
            self.__neo_dir = dir
            Config().set_save()

    ##
    # Config Constructor.
    #
    # @param self The object pointer
    # @param neo_exe_file Path to Neo4j executable path (str)
    # @param neo_dir Path to Neo4j root directory (str).
    # @param save_dir Path to the default directory for saving results (see select_path in save_window.py)
    # @param tech_dir Path to the default directory for loading techniques (see open_file in main_window.py)
    # @param parent Parent (QWidget)
    # @param save Set to True if Config has been changed since being loaded from config.json (bool)
    #
    def __init__(self, neo_exe_file=None, neo_dir=None, save_dir=None, tech_dir=None, parent=None, save=False):
        self.neo = self.Neo4jConfig(exe_file=neo_exe_file, neo_dir=neo_dir)
        self.tech_dir = tech_dir
        self.save_dir = save_dir
        self.__parent = parent
        self.__save = save

    ##
    # Config __dict__ method.
    # Return all the properties of the Neo4jConfig in a dictionary.
    # @param self The object pointer
    # @return dict
    def __dict__(self):
        return {
            "neo": self.neo.__dict__(),
            "save_dir": self.save_dir,
            "tech_dir": self.tech_dir
        }

    ##
    # Config set method.
    # Set the value of a specific property.
    # @param self The object pointer
    # @param prop Name of the property (str)
    # @param value New value of the property
    #
    def set(self, prop, value):
        if prop == "Neo4j Desktop executable file":
            self.neo.set_exe_file(value)
        elif prop == "Neo4j directory":
            self.neo.set_neo_dir(value)
        elif prop == "Techniques directory":
            self.set_tech_dir(value)
        elif prop == "Save directory":
            self.set_save_dir(value)

    ##
    # Config set_tech_dir method.
    # Set a new value for the path to the default directory for technique loading and set the save option of Config to
    # True.
    # @param self The object pointer
    # @param value New value for the path of technique directory.
    def set_tech_dir(self, value):
        self.tech_dir = value
        Config().set_save()

    ##
    # Config set_save_dir method.
    # Set a new value for the path to the default directory for saving results and set the save option of Config to
    # True.
    # @param self The object pointer
    # @param value New value for the path of save directory.
    def set_save_dir(self, value):
        self.save_dir = value
        Config().set_save()

    ##
    # Config get_tech_dir method.
    # Return the path to the technique directory or empty str if value is none
    # @param self The object pointer
    # @return str
    #
    def get_tech_dir(self):
        return self.tech_dir if self.tech_dir is not None else ""

    ##
    # Config get_save_dir method.
    # Return the path to the save directory or empty str if value is none
    # @param self The object pointer
    # @return str
    #
    def get_save_dir(self):
        return self.save_dir if self.save_dir is not None else ""

    ##
    # Config set_save method.
    # Set __save property.
    # @param self The object pointer
    def set_save(self, save=True):
        self.__save = save

    ##
    # Config from_json method.
    # Set property with the data found in 'config.json'
    # @param self The object pointer
    # @param parent Parent (QWidget)
    def from_json(self, parent=None):
        data = get_config()
        if data is not None:
            self.neo = self.neo_from_json(data.get("neo"))
            self.save_dir = data.get("save_dir")
            self.tech_dir = data.get("tech_dir")
        if parent is not None:
            self.__parent = parent
        self.__save = False

    ##
    # Config neo_from_json method.
    # Create new Neo4jConfig from data found in 'json'.
    # @param self The object pointer
    # @param json dict
    # @return Neo4jConfig
    def neo_from_json(self, json):
        return self.Neo4jConfig().from_json(json)

    ##
    # Config get_neo_exe method.
    # Return path to neo4j executable file.
    # @param self The object pointer
    # @return str
    def get_neo_exe(self):
        return self.neo.get_exe_file()

    ##
    # Config get_neo_dir method.
    # Return path to neo4j directory.
    # @param self The object pointer
    # @return str
    def get_neo_dir(self):
        return self.neo.get_neo_dir()

    ##
    # Config save method.
    # Save actual config in 'config.json' file.
    # @param self The object pointer
    def save(self):
        json_file = open("config.json", "w")
        json_file.write(self.to_json())
        json_file.close()
        self.set_save(False)

    ##
    # Config to_json method.
    # Serialize Config to a JSON formatted str
    # @param self The object pointer
    # @return str
    #
    def to_json(self):  # return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        return json.dumps(self.__dict__(), sort_keys=True, indent=4)

    ##
    # Config need_save method.
    # Return True if config has change since being loaded from json, and has to be saved.
    # @param self The object pointer
    # @return bool
    #
    def need_save(self):
        return self.__save

    ##
    # Config get_parent method.
    # Return parent (usually the main window).
    # @param self The object pointer
    # @return QWidget
    #
    def get_parent(self):
        return self.__parent
