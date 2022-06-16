import copy

from sources.back.neo.neoobj import NeoType


##
# @ingroup neo
#
##
# get_input_id function.
# Return id of the object of not none.
# @param obj object
# @return str
#
def get_input_id(obj):
    if obj is None:
        return None
    else:
        return obj.id


##
# @ingroup neo
#
##
# get_node_input function.
# Return value of the type (NeoType) of obj
# @param obj object
# @return str
#
def get_node_input(obj):
    if obj is None:
        return None
    else:
        return obj.type.value


##
# @ingroup neo
#
##
# Where class
# Build Where Clauses
# combine two Where Object with & (and) and | (or) operators
# ex: newObj = obj1 & obj2
# newObj = obj1 | obj2
#
class Where:
    ##
    # Where Constructor.
    #
    # @param self The object pointer
    # @param node node where the condition is applied ("input" or "output")
    # @param field field of the node were the condition is applied (ex: "name", "id"...)
    # @param value value of the field
    #
    def __init__(self, node, field, value):
        if node != "input" and node != "output":
            raise TypeError("Invalid argument node")
        if field is None or len(node) == 0:
            raise TypeError("node can not be empty")
        if value is None or len(node) == 0:
            raise TypeError("node can not be empty")
        self.condition = " " + ("n" if node == "input" else "res") + "." + field + " = \"" + value + "\""

    ##
    # Where __str__ method.
    # Override str to get the where clause
    # @param self The object pointer
    def __str__(self):
        return "\nwhere" + self.condition

    ##
    # Where __and__ method.
    #  & operator
    # @param self The object pointer
    def __and__(self, other):
        res = copy.deepcopy(self)
        res.condition += " and" + other.condition
        return res

    ##
    # Where __or__ method.
    # | operator
    # @param self The object pointer
    def __or__(self, other):
        res = copy.deepcopy(self)
        res.condition += " or" + other.condition
        return res


##
# @ingroup neo
#
##
# use to generate a query
# to generate unions use QueryObject.union(SecondQueryObject) as many time as you want.
# Then, generate the query by calling str on the new Object.
# ex: newObject = FirstObject.union(SecondObject).union(ThirdObject)
#     query = str(newObject)
#
# ex2:
# query = Query(node_input="Mitigation",
#                 input_type="name",
#                 input_value="Privileged Account Management",
#                 node_output="Technique",
#                 where=Where("output", "id", "attack-pattern--34e793de-0274-4982-9c1a-246ed1c19dee") |
#                                 Where("output", "id", "attack-pattern--565275d5-fcc3-4b66-b4e7-928e4cac6b8c"))
#
# str(query)
#
#     'match (n:Mitigation {name: "Privileged Account Management"}) Optional match (res:Technique)<--(n) where res.id = attack-pattern--34e793de-0274-4982-9c1a-246ed1c19dee or res.id = attack-pattern--565275d5-fcc3-4b66-b4e7-928e4cac6b8c return n, res'
#
#
class Query:
    ##
    # @var node_input
    # Node Label of the input
    #
    # @var input_type
    # Field used to find the node
    #
    # @var input_value
    # Value of the field used to find the Node
    #
    # @var node_output
    # Node Label of the result
    #
    # @var result_column
    # name of the result column
    #
    # @var input_column
    # name of the first column
    #
    # @var where
    # Where clause
    #
    # @var relation
    # Relation type between Input and Output Nodes
    #
    # @var empty
    # boolean is the node empty
    #
    # @var others
    # list query linked by union
    #

    ##
    # Query __init__ method.
    # use:
    #     __init__(self, node_input, input_type, input_value, node_output, relation=None, where=None, result=None, input_name=None, empty=False)
    #     __init__(self, input_obj, node_output, relation=None, where=None, result=None, input_name=None, empty=False)
    #
    # The parameters can not be None except relation, where, input_name and result.
    #
    # @param self The object pointer
    # @param node_input Node Label of the input (ex: "Group", "Mitigation", "Technique") (str)
    # @param input_type Field used to find the node (ex: "id", "name"...) (str)
    # @param input_value Value of the field used to find the Node (str)
    # @param input_obj Object containing the information above (NeoObj)
    # @param node_output Node Label of the result (ex: "Group", "Mitigation", "Technique") (str)
    # @param relation Relation type between Input and Output Nodes (str)
    # @param where Where clause (str or Where Object)
    # @param result name of the result column (str)
    # @param input_name name of the first column (str)
    # @param empty create an empty query (bool)
    def __init__(self, *args, **kwargs):
        if kwargs.get("empty", False):
            self.node_input = None
            self.input_type = None
            self.input_value = None
            self.node_output = None
            self.result_column = None
            self.input_column = None
            self.where = None
            self.relation = None
            self.empty = True
            self.others = []
        else:
            self.node_input = kwargs.get("node_input", get_node_input(kwargs.get("input_obj")))
            self.input_type = kwargs.get("input_type", "id")
            self.input_value = kwargs.get("input_value", get_input_id(kwargs.get("input_obj")))
            self.node_output = kwargs.get("node_output")
            self.result_column = kwargs.get("result", "res")
            self.input_column = kwargs.get("input_name", "input")
            self.where = kwargs.get("where", "")
            if self.node_input is None:
                raise TypeError("missing node_input or input_obj argument")
            if self.input_type is None:
                raise TypeError("missing input_type or input_obj argument")
            if self.input_value is None:
                raise TypeError("missing input_value or input_obj argument")
            if self.node_output is None:
                raise TypeError("missing node_output argument")
            relation = kwargs.get("relation")
            self.relation = "[r:" + relation + "]" if relation is not None and len(relation) != 0 else ""
            self.others = []
            self.empty = False

    ##
    # Query __str__ method.
    # Override str to get the query
    # @param self The object pointer
    def __str__(self):
        if self.empty:
            return ""
        res = "match (n:" + self.node_input + " {" + self.input_type + ": \"" + self.input_value
        res += "\"})\nOptional match (res"
        if self.node_output != NeoType.All.value:
            res += ":" + self.node_output
        res += ")"
        relation = "-" + self.relation + "-"
        if self.node_input == "Technique":
            relation += ">"
        else:
            relation = "<" + relation
        res += relation + "(n)" + str(
            self.where) + "\nreturn n as " + self.input_column + ", res as " + self.result_column
        for e in self.others:
            res += "\nunion\n" + str(e)
        return res

    ##
    # Query union method.
    # union between two query return new Query instance
    # @param self The object pointer
    # @param other Other object pointer
    def union(self, other):
        if self.empty:
            return copy.deepcopy(other)
        if other.empty:
            return copy.deepcopy(self)
        res = copy.deepcopy(self)
        res.others.append(other)
        return res
