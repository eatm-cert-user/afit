import enum


##
# @ingroup back
#

##
# FileType.
# Enum representing file type
#
class FileType(enum.Enum):
    Invalid = 0
    Txt = 1
    Json = 2
    Csv = 3

    ##
    # to_file_type function.
    # Convert a str representing a file type to its corresponding FileType(Enum)
    # @param f_type file type (str)
    # @return FileType
    @staticmethod
    def to_file_type(f_type):
        if f_type == "Json (*.json)":
            return FileType.Json
        elif f_type == "Text (*.txt)":
            return FileType.Txt
        elif f_type == "CSV (Comma delimited) (*.csv)":
            return FileType.Csv
        else:
            return FileType.Invalid

