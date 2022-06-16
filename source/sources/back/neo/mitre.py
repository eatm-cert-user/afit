import urllib

from sources.attack2neo.attack2neo import *

##
# @ingroup neo
#
# get last version of Att&ck from github
def last_version():
    url = "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"

    json_file = urllib.request.urlopen(url)
    try:
        """
        with open(json_file) as fh:
            data = json.load(fh)
        fh.close()"""
        data = json.load(json_file)
    except Exception as e:
        sys.stderr.write('[ERROR] reading configuration file %s\n' % json_file)
        sys.stderr.write('[ERROR] %s\n' % str(e))
        return "Error reading json file"
    return data['id']





##
# @ingroup neo
#

##
# import_mitre function.
# Import json from mitre github
def import_mitre():
    # import json from mitre github
    url = "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"

    json_file = urllib.request.urlopen(url)

    try:
        """
        with open(json_file) as fh:
            data = json.load(fh)
        fh.close()"""
        data = json.load(json_file)
    except Exception as e:
        sys.stderr.write('[ERROR] reading configuration file %s\n' % json_file)
        sys.stderr.write('[ERROR] %s\n' % str(e))
        return "Error reading json file"

    # open graph connection
    graph_bolt = "bolt://127.0.0.1:7687"
    graph_auth = ("neo4j", "mitre")

    try:
        graph = Graph(graph_bolt, auth=graph_auth)
    except Exception:
        sys.stderr.write("Connection failed\n")
        return "Connection failed"

    # Delete existing nodes and edges
    graph.delete_all()

    # Create Node with mitre version
    node_version = Node("Version", id=last_version())
    graph.merge(node_version, "Version", 'id')

    # Global names
    gnames = {}

    #
    # Walk through JSON objects to create nodes
    for obj in data['objects']:
        if obj['type'] == 'intrusion-set':
            gnames[obj['id']] = obj['name']
            build_objects(obj, 'aliases', graph)

        """
        if obj['type']=='malware':
            gnames[ obj['id'] ] = obj['name']
            build_objects(obj,'x_mitre_aliases', graph)

        if obj['type']=='tool':
            gnames[ obj['id'] ] = obj['name']
            build_objects(obj,'x_mitre_aliases', graph)
        """

        # `course of action` are the mitigations remove left part of the 'or' to import only attacks
        if obj['type'] == 'attack-pattern' or obj['type'] == 'course-of-action':
            gnames[obj['id']] = obj['id']
            build_objects(obj, None, graph)
            

        # label = build_label(obj['type'])
        # node_main = Node(label, name=obj['name'], id=obj['id'])
        # graph.merge(node_main,label,'name')
        # print('%s: "%s"' % (label,obj['name']) ) if dbg_mode else None

    # Walk through JSON objects to create edges
    for obj in data['objects']:
        if obj['type'] == 'relationship':
            build_relations(obj, gnames, graph)
    return "Graph created"
