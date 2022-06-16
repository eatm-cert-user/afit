from enum import Enum


##
# @ingroup display_options
#

##
# DisplayedObject
# Used in 'show details' (Groups). Specifies which are the techniques displayed.
# All: All the techniques used by the group.
# Filtered: Techniques used by the group contained in the MainWindow Technique area.
#
class DisplayedObject(Enum):
    All = "All Techniques"
    Filtered = "Techniques Used"


##
# Type Use to display NeoObj in a ListView
# Id: external id of the NeoObj (ex: T1602)
# Name: Name of the NeoObj (ex: Data from Configuration Repository)
# IdName: External id and Name of the NeoObj (ex: T1602: Data from Configuration Repository)
#
class DisplayedType(Enum):
    Id = "external_id"
    Name = "name"
    IdName = "id_name"
