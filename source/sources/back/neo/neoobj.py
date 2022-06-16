import enum

from PySide6 import QtWidgets


##
# @ingroup neo
#
##
# NeoType Enum.
# Type of NeoObj.
class NeoType(enum.Enum):
    Unknown = ""
    Mitigation = "Mitigation"
    Group = "Group"
    Technique = "Technique"
    All = "All"


##
# @ingroup neo
#
##
# NeoObj class.
# Object representing a Neo4j node.
#
class NeoObj:
    ##
    # @var name
    #
    #
    # @var external_id
    #
    #
    # @var id
    #
    #
    # @var description
    #
    #
    # @var type
    #
    #

    ##
    # NeoObj Constructor.
    # 
    # @param self The object pointer
    # @param obj dist representing the object
    #
    def __init__(self, obj):
        super(NeoObj, self).__init__()
        self.name = obj.get("name")
        self.external_id = obj.get("external_id")
        self.id = obj.get("id")
        self.description = obj.get("description")
        if obj.get("type") == "course-of-action":
            self.type = NeoType.Mitigation
        elif obj.get("type") == "attack-pattern":
            self.type = NeoType.Technique
        elif obj.get("type") == "intrusion-set":
            self.type = NeoType.Group
        else:
            self.type = NeoType.Unknown

    ##
    # NeoObj Override __eq__ method.
    # return True if both object are the same node.
    # @param self The object pointer
    def __eq__(self, other):
        return self.id == other.id

    ##
    # NeoObj Override __hash__ method.
    # 
    # @param self The object pointer
    def __hash__(self):
        return hash(self.id)

    ##
    # NeoObj Override __len__ method.
    # 
    # @param self The object pointer
    def __len__(self):
        return 0

    ##
    # NeoObj get_id_name method.
    # return name and id of the object.
    # @param self The object pointer
    # @return str
    def get_id_name(self):
        return self.external_id + ": " + self.name

    ##
    # NeoObj get_name method.
    # Return name of the object.
    # @param self The object pointer
    # @return str
    def get_name(self):
        return self.name

    ##
    # NeoObj get_id method.
    # Return external id.
    # @param self The object pointer
    # @return str
    def get_id(self):
        return self.external_id

    ##
    # NeoObj get method.
    # Return value of a property of the object.
    # @param self The object pointer
    # @param att Name of the property.
    # @return str
    #
    def get(self, att):
        if att == "name":
            return self.name
        elif att == "id":
            return self.id
        elif att == "description":
            return self.description
        elif att == "type":
            return self.type
        elif att == "external_id":
            return self.external_id
        elif att == "id_name":
            return self.get_id_name()
        elif att == "link":
            return self.get_link()
        else:
            return None

    ##
    # NeoObj get_link method.
    # Return url link to Mitre Att&ck of the object.
    # @param self The object pointer
    # @return str
    #
    def get_link(self):
        base = "https://attack.mitre.org/"
        if self.type == NeoType.Group:
            type = "groups/"
        elif self.type == NeoType.Mitigation:
            type = "mitigations/"
        elif self.type == NeoType.Technique:
            type = "techniques/"
        else:
            raise TypeError("Invalid Neo Object type.")

        return base + type + self.external_id.replace(".", "/")
