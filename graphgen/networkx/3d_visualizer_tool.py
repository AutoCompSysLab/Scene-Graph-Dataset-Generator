import os
import json

import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Load Classes
# https://github.com/3DSSG/3DSSG.github.io/blob/master/README.md 
"""
Input : classes.txt, relations.txt
1. classes.txt
1	air conditioner	a system that keeps air cool and dry	cooling_system	mechanism	device	instrumentality	artifact	whole	object	physical_entity	entity
2	apron	a garment of cloth or leather or plastic that is tied about the waist and worn to protect your clothing	protective_garment	clothing	covering
...

2. relations.txt
none
supported by
left
right
...

Output
"""
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  

def load_classes(classes_f_name, relationships_f_name) -> tuple:
    c_file = open(os.path.join(BASE_DIR, "3DSSG", classes_f_name), "r")
    r_file = open(os.path.join(BASE_DIR, "3DSSG", relationships_f_name), "r")
    
    c_lines = c_file.readlines()
    r_lines = r_file.readlines()
    
    return (c_lines, r_lines)

# LoadData
# https://github.com/3DSSG/3DSSG.github.io/blob/master/README.md
"""
Input : object.json, relations.json
Sample is in above link.
"""

def load_data(obj_file_name, rel_file_name) -> tuple:
    with open(os.path.join(BASE_DIR, "3DSSG", obj_file_name), "r") as obj_file:
        obj_scans = json.load(obj_file).get("scans")
    with open(os.path.join(BASE_DIR, "3DSSG", rel_file_name), "r") as rel_file:
        rel_scans = json.load(rel_file).get("scans")
    
    return (obj_scans, rel_scans)

def find_scan(scan, obj_scans):
    for obj_scan in obj_scans:
        if obj_scan.get("scan") == scan:
            return obj_scan.get("objects")
    return None
    
def find_obj(objs, obj_id):
    for obj in objs:
        if obj_id == int(obj["id"]):
            return obj
    return None

def make_edges_objs_label(objs, rels):
    edge_dict = {}
    # To save label by obj_id
    obj_id_label = {}
    for relation in rels:
        start_id = relation[0]
        end_id = relation[1]
        relation_id = relation[2]
        relation_label = relation[3]

        # type(edge keys) = tuple
        edge = (start_id, end_id)
        # edge values = string (ex. stand on in front)
        if edge in edge_dict.keys():
            edge_dict[edge] += relation_label +", "
        else:
            edge_dict[edge] = relation_label + ", "
        
        # update obj_id_label dict
        if start_id not in obj_id_label.keys():
            start_label = find_obj(objs, start_id).get("label")
            obj_id_label[start_id] = start_label + "_" + str(start_id)
        if end_id not in obj_id_label.keys():
            end_label = find_obj(objs, end_id).get("label")
            obj_id_label[end_id] = end_label +"_"+str(end_id)
            
    return edge_dict, obj_id_label
        
def draw_graph(objs, edge_dict: dict, obj_id_label: dict):
    # network X
    graph = nx.DiGraph()
    obj_lists = [(val, {'id':key}) for key, val in obj_id_label.items()]
    # obj_labels = list(obj_id_label.values())
    # obj node 추가
    # TODO : 여기서 이름이 같으면 add_nodes_from에서 하나로 보여져요...
    graph.add_nodes_from(obj_lists)

    print(graph.nodes)
    # 각 node들의 위치를 생성하는 함수
    pos = make_position(obj_lists)
    # pos = make_position(list(obj_id_label.values()))
    
    # edge label 추가
    """
    edge_dict = {
        (start_id, end_id): relations labels,
        ...
    }
    """
    for edges in edge_dict:
        graph.add_edge(obj_id_label[edges[0]], obj_id_label[edges[1]], name=edge_dict[edges])
        
    labels = nx.get_edge_attributes(graph, "name")

    nx.draw(graph, pos, with_labels=True)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels, verticalalignment='top')
    
    plt.show()
    

def make_position(obj_lists:list) -> dict:
    pos = {}
    for obj in obj_lists:
        if obj[1]['id'] % 2 == 0:
            pos_lst = [obj[1]['id'], len(obj_lists) - obj[1]['id']]
        else:
            pos_lst = [obj[1]['id'], obj[1]['id']]
    
        pos[obj[0]]=pos_lst
    return pos


def visualizer_3d():
    # load class, relationships class
    c_lines, r_lines = load_classes("classes.txt", "relationships.txt")
    
    # load object, relationships instances data
    obj_scans, rel_scans = load_data("objects.json", "relationships.json")

    # search all relations by scan
    for rel_scan in rel_scans:
        rels = rel_scan.get("relationships")
        scan = rel_scan.get("scan")
        # TEST
        # TODO : Delete this when it will be deployed
        if scan != "6bde60c6-9162-246f-8d25-4df09330450c":
            continue
        # Check when the scan code of obj_scans same with it of rel_scans
        objs = find_scan(scan, obj_scans)
        # Make edges & label by obj_id 
        edge_dict, obj_id_label = make_edges_objs_label(objs, rels)
        # Draw Graph
        """
        objs = [object instances(dict)]
        edge_dict = {
            (start_id, end_id): relations labels,
            ...
        }
        obj_id_label = {
            1 : "wall",
            2 : "floor",
            ...
        }
        """
        draw_graph(objs, edge_dict, obj_id_label)
        break

visualizer_3d()

# if __name__ == '__main__':
#     visualizer_3d()