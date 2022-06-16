import sys

from neo4j import GraphDatabase
from sources.back.neo.neoobj import NeoObj


##
# @ingroup neo
#
##
# Request get_techniques function.
# Get techniques used by a specific groups.
#
# @param tx
# @param group_id Group id
# @param where_clause where clause to apply to the query
def get_techniques(tx, group_id, where_clause=""):
    query = "match (g:Group {id:\"" + group_id + "\"})-[r:uses]->(t:Technique) " \
            + where_clause + " return t, g"
    result = tx.run(query).data()
    techniques = [NeoObj(record["t"]) for record in result]
    """
    for record in result:
        techniques.append(record["t"]["external_id"] + ": " + record["t"]["name"])
        """
    return techniques


##
# @ingroup neo
#
##
# Request techniques_from_group function.
# Get the list of techniques used by a specific group. if 'techniques' is not None, it only return
# techniques contained in 'techniques' and used by this group.
#
# @param group_id Group id
# @param techniques list of techniques
def techniques_from_group(group_id, techniques=None):
    if techniques is None or techniques == []:
        res = exec_transaction(group_id, get_techniques)
    else:
        where_clause = "where t.id = \"" + techniques[0]
        for i in range(1, len(techniques)):
            where_clause += "\" or t.id = \"" + techniques[i]
        where_clause += "\""
        res = exec_transaction(group_id, get_techniques, where_clause)
    return res


##
# @ingroup neo
#
##
# Request get_groups function.
# Get list of groups known to use specific techniques and the number of techniques used by each of them.
#
# @param techniques list of techniques
# @return list of groups ordered by the number of technique used (descending)
def get_groups(techniques):
    groups = exec_transaction(techniques, get_groups_neo4j)
    return order_groups(groups)


##
# @ingroup neo
#
##
# Request get_groups_neo4j function.
# Get list of groups known to use specific techniques.
#
# @param tx tx
# @param techniques list of techniques
# @return list containing groups and the number of techniques used from the technique input list.
def get_groups_neo4j(tx, techniques):
    if len(techniques) < 1:
        sys.stderr.write('[ERROR] get_groups: Empty List \n')
        sys.exit(1)
    query = "match (g:Group)-[r:uses]->(t:Technique) where t.id = \"" + techniques[0] + "\""
    for i in range(1, len(techniques)):
        query += " or t.id = \"" + techniques[i] + "\""
    query += " return g, count(r) as c"
    #query = "match (res)-->(n) where n.id = \"" + techniques[0] + "\" return res as res"
    result = tx.run(query).data()
    groups = []
    for record in result:
        groups.append([record["g"], record["c"]])
     #  groups.append([record["res"], 1])
    return groups


##
# @ingroup neo
#
##
# Request exec_transaction function.
# Run transaction with one or two parameter
#
# @param arg first parameter of the transaction
# @param transaction Transaction
# @param arg2 second parameter od the transaction (can be none)
def exec_transaction(arg, transaction, arg2=None):
    uri = "bolt://127.0.0.1:7687"
    auth = ("neo4j", "mitre")
    driver = GraphDatabase.driver(uri, auth=auth)
    with driver.session() as session:
        if arg2:
            groups = session.read_transaction(transaction, arg, arg2)
        else:
            groups = session.read_transaction(transaction, arg)
    driver.close()
    return groups


##
# @ingroup neo
#
##
# Request order_groups function.
# Return list of groups ordered by the number of technique used (descending).
#
# @param groups list of groups
# @return list
def order_groups(groups):
    groups_order = []
    for (g, n) in groups:
        while len(groups_order) < n:
            groups_order.append([])
        groups_order[n - 1].append(g)
    groups_order.reverse()
    res = []
    match_count = len(groups_order)
    for group in groups_order:
        if len(group) > 0:
            res.append((match_count, group))
        match_count -= 1
    return res
