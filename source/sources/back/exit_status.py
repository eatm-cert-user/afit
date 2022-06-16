from enum import Enum

from PySide6 import QtWidgets


##
# @ingroup back
#

##
# Status.
# Used in ExitStatus. represent the status at the end of a process.
#
class Status(Enum):
    Ok = [1, "Ok"]
    Error = [2, "Error"]
    Cancel = [3, "Cancel"]


##
# ExitStatus.
# Contain exist status of a function or method and the output value
# 
class ExitStatus:
    ##
    # @var status
    # Status Enum
    #
    # @var msgBox
    # Message box (mostly in case of error)
    #
    # @var content
    # Object
    #

    ##
    # ExitStatus Constructor.
    # 
    # @param self The object pointer
    # @param status Status Enum
    # @param content Object (if is a str instance set the msgBox text)
    # @param parent Parent (QWidget)
    def __init__(self, status, content="", parent=None):
        self.status = status
        self.content = content
        if status == Status.Cancel and len(content) == 0:
            self.content = "Operation Canceled"
        self.msgBox = QtWidgets.QMessageBox(parent)
        self.msgBox.setWindowTitle(self.status.value[1])
        if isinstance(self.content, str) and len(self.content) != 0:
            self.msgBox.setText(self.content)

    ##
    # ExitStatus __eq__ method.
    # Used to compare status.
    # @param self The object pointer
    def __eq__(self, other):
        return self.status == other.status

    ##
    # ExitStatus __str__ method.
    # override str method. returns content.
    # @param self The object pointer
    def __str__(self):
        return self.content

    ##
    # ExitStatus is_ok method.
    # True is status is Status.Ok else False.
    # @param self The object pointer
    def is_ok(self):
        return self.status == Status.Ok

    ##
    # ExitStatus exec method.
    # calls exec on the messageBox.
    # @param self The object pointer
    def exec(self):
        self.msgBox.exec()

    ##
    # ExitStatus setDetailedText method.
    # Set detailed text of the message box.
    # @param self The object pointer
    # @param text Detailed text to set.
    def setDetailedText(self, text):
        self.msgBox.setDetailedText(text)

    ##
    # ExitStatus set_content method.
    # Set content and the text of the message box if text is str instance.
    # @param self The object pointer
    # @param text Object
    def set_content(self, text):
        self.content = text
        if len(text) == 0 and self.status == Status.Cancel:
            self.content = "Operation Canceled"
        if isinstance(self.content, str) and len(self.content) != 0:
            self.msgBox.setText(self.content)

    ##
    # ExitStatus set_status method.
    # Change the status of the object.
    # @param self The object pointer
    # @param status New status
    def set_status(self, status):
        self.status = status
        if len(self.content) == 0 and status == Status.Cancel:
            self.content = "Operation Canceled"
        self.msgBox.setWindowTitle(self.status.value[1])
        self.msgBox.setText(self.content)
