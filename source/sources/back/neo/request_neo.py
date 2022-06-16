import sys
import time

from PySide6 import QtWidgets
from PySide6.QtWidgets import QMessageBox, QComboBox
from neo4j import GraphDatabase
from py2neo import Graph

from sources.back.exit_status import ExitStatus, Status
from sources.back.neo.neoobj import NeoObj

##
# @ingroup neo
#
##
# Request Neo run_single_result function.
from sources.back.object_selector import ObjectSelector


def version_query(tx, parent):
    res = tx.run("match (n:Version) return n").data()
    if not res or len(res) == 0:
        return ExitStatus(Status.Error, "No version found in the graph.", parent=parent)
    return ExitStatus(Status.Ok, res[0]["n"]["id"], parent=parent)



##
# @ingroup neo
#
##
# Request Neo run_single_result function.
# 
# @param tx
# @param query Query to run (Query object)
# @param parent parent (QWidget)
# @param column Result column
# @param no_mitigation True if it can not have any Mitigation node in the result
# @return ExitStatus result of the query from the database
def run_single_result(tx, query, parent, column, no_mitigation=True):
    res = tx.run(query).data()
    if no_mitigation:
        
        res = [NeoObj(record[column]) for record in res if record[column] is not None and
               record[column]["type"] != "course-of-action"]
    else:
        res = [NeoObj(record[column]) for record in res if record[column] is not None]

    if not res or len(res) == 0:
        return ExitStatus(Status.Error, query.input_value + ": No result Found", parent=parent)

    if len(res) == 1:
        return ExitStatus(Status.Ok, res[0], parent=parent)
    else:
        if query.input_type == "id" or query.input_type == "external_id":
            result = "name"
        else:
            result = "external_id"
        msg_box = QMessageBox(parent)
        msg_box.setWindowTitle("Multiple Results")
        msg_box.setText("Found multiple result for " + query.input_type + " " + query.input_value)
        msg_box.addButton(QMessageBox.Ok)
        msg_box.addButton(QMessageBox.Cancel)
        # Object Selector
        msg_box.layout().addWidget((select := ObjectSelector(res, result, msg_box)), 1, 1)
        if msg_box.exec() == QMessageBox.Ok:
            return ExitStatus(Status.Ok, select.get_elem(), parent=parent)
        else:
            return ExitStatus(Status.Cancel, parent=parent)


##
# @ingroup neo
#
##
# Request Neo run_mult_result function.
# 
# @param tx
# @param query Query to run (Query object)
# @param parent parent (QWidget)
# @param column Result column
# @param no_mitigation True if it can not have any Mitigation node in the result
# @return ExitStatus result of the query from the database
def run_mult_result(tx, query, parent, column, no_mitigation=False):
    res = tx.run(query).data()
    if not res or len(res) == 0:
        return ExitStatus(Status.Error, query.input_value + ": No result Found", parent=parent)
    if no_mitigation:
        res = [NeoObj(record[column]) for record in res if record[column] is not None and
               record[column]["type"] != "course-of-action"]
    else:
        res = [NeoObj(record[column]) for record in res if record[column] is not None]
    return ExitStatus(Status.Ok, res, parent=parent)


##
# @ingroup neo
#
##
# Request Neo get_version function.
# Run the query to get the version of the graph.
#
# @param parent parent (QWidget)
# @return ExitStatus result of the query from the database
def get_version(parent):
    uri = "bolt://127.0.0.1:7687"
    auth = ("neo4j", "mitre")
    try:
        Graph(uri, auth=auth)
    except Exception:
        sys.stderr.write("Connection failed\n")
        return ExitStatus(Status.Error, "Connection failed", parent=parent)
    driver = GraphDatabase.driver(uri, auth=auth)
    with driver.session() as session:
        data = session.read_transaction(version_query, parent)
    driver.close()
    return data


##
# @ingroup neo
#
##
# Request Neo get_data function.
# Run query with the specific transaction.
#
# @param transaction transaction
# @param query Query to run (Query object)
# @param parent parent (QWidget)
# @param column Result column
# @return ExitStatus result of the query from the database
def get_data(transaction, query, parent, column):

    uri = "bolt://127.0.0.1:7687"
    auth = ("neo4j", "mitre")
    try:
        Graph(uri, auth=auth)
    except Exception:
        sys.stderr.write("Connection failed\n")
        return ExitStatus(Status.Error, "Connection failed", parent=parent)
    driver = GraphDatabase.driver(uri, auth=auth)
    with driver.session() as session:
        data = session.read_transaction(transaction, query, parent, column)
    driver.close()
    return data
