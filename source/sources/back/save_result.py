import json

from sources.back.file_type import FileType


##
# @ingroup back
#

##
# SaveResult
# Class to format and save Result
#
class SaveResult:
    ##
    # @var result
    # Result table as list.
    #
    # @var path
    # path to the file used to save the results
    #
    # @var file_type
    # FileType Enum. Type of the file use for the format of the output.
    #
    # @var row
    # Number of row to save. If 0, all the rows will be saved.
    #
    # @var sep
    # Separator (str, length 1) if needed (used for csv files).
    #
    # @var parent
    # Parent (QWidget).
    #

    ##
    # SaveResult __init__ method.
    # 
    # @param self The object pointer
    # @param result Result table (as a list)
    # @param path str path to the file used to save the result.
    # @param file_type FileType Enum represent type of the file. Use to format the output.
    # @param row_limit number of row to save. If 0, all the rows will be saved.
    # @param sep Separator (str of length 1) used for Csv files.
    # @param parent Parent QWidget
    #
    def __init__(self, result=[[]], path=None, file_type=FileType.Invalid, row_limit=None, sep=";", parent=None):
        self.result = result
        self.path = path
        self.file_type = file_type
        self.row = row_limit if row_limit is not None else 0
        self.sep = sep
        self.parent = parent

    ##
    # SaveResult __str__ method.
    # Convert the first 'self.row' rows of the result list to str.
    # @param self The object pointer
    def __str__(self):
        if self.path is None or self.file_type == FileType.Invalid:
            return ""
        res = []
        m = min(self.row, len(self.result)) if self.row != 0 else len(self.result)
        for i in range(m):
            res.append(self.result[i])
        return self.to_str(res)

    ##
    # SaveResult to_str method.
    # Convert result_list to str according to the file_type.
    # @param self The object pointer
    # @param result_list List to convert to str
    def to_str(self, result_list):
        # Json File (not used anymore)
        if self.file_type == FileType.Json:
            return json.dumps(result_list, indent=4)
        # Txt File (not used anymore)
        elif self.file_type == FileType.Txt:
            if not result_list or result_list == [[]]:
                return ""
            res = ""
            for e in result_list:
                res += str(e[0]) + "\n"
                for elem in e[1]:
                    res += elem["name"] + ";" + elem["external_id"] + "\n"
            return res
        # Csv File
        elif self.file_type == FileType.Csv:
            if not result_list or result_list == [[]]:
                return ""
            res = ""
            for e in result_list:
                res += "\"" + str(e[0].text()).replace("\n", " - ") + "\""
                groups = self.sep + "\""
                for elem in e[1]:
                    groups += elem.get(self.parent.displayed_type.value) + ";"
                if len(groups) > 2:
                    groups += '\"'
                else:
                    groups = ""
                res += groups + "\n"
            return res
        # Invalid File
        return ""
