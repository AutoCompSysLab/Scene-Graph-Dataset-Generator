import os
import json
import random

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.pyplot import text
from mpl_toolkits.mplot3d import Axes3D

import numpy as np

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
    with open(os.path.join(BASE_DIR, "ACSL", obj_file_name), "r") as obj_file:
        obj_scans = json.load(obj_file).get("scans")
        # obj_scans : scan list
    with open(os.path.join(BASE_DIR, "3DSSG", rel_file_name), "r") as rel_file:
        rel_scans = json.load(rel_file).get("scans")
        # rel_scans : scan list
    
    return (obj_scans, rel_scans)

def find_objects_by_scan(scan_id, obj_scans) -> list:
    for obj_scan in obj_scans:
        if obj_scan.get("scan") == scan_id:
            return obj_scan.get("objects")
    return None
    
def find_obj(objs, obj_id) -> dict:
    for obj in objs:
        if obj_id == int(obj["id"]):
            return obj
    return None

def make_edges_objs(objs, rels):
    edge_set = set()
    # To save label by obj_id
    obj_dict = {}
    rel_dict = {}
    label_color = {}
    for i in range(len(rels)):
        relation = rels[i]
        start_id = relation[0]
        end_id = relation[1]
        
        start_obj = find_obj(objs, start_id)
        start_label = start_obj.get("label").replace(" ", "\n")
        start_name = start_label+"\n"+str(start_id)
        start_position = start_obj.get("position")
        
        end_obj = find_obj(objs, end_id)
        end_label = end_obj.get("label").replace(" ", "\n")
        end_position = end_obj.get("position")
        end_name = end_label +"\n"+str(end_id)
        
        relation_label = relation[3].replace(" ", "\n")
        relation_position = np.sum([start_position, end_position], axis=0)/2
        relation_name = relation_label + "\n" + str(i)

        # type(edge keys) = tuple
        edge1 = (start_name, relation_name)
        edge2 = (relation_name, end_name)
        edge_set.add(edge1)
        edge_set.add(edge2)
        
        # update obj_id_label dict
        if start_name not in obj_dict.keys():
            # coloring
            if start_label in label_color.keys():
                color = label_color[start_label]
            else:
                color = "#"+''.join([random.choice('789ABCDEF') for j in range(6)]) 
                label_color[start_label] = color
            
            obj_dict[start_name] = {
                "name" :  start_name,
                "label" : start_label,
                "position" : start_position,
                "color" : color
            }
            
        if end_name not in obj_dict.keys():
            # coloring
            if end_label in label_color.keys():
                color = label_color[end_label]
            else:
                color = "#"+''.join([random.choice('789ABCDEF') for j in range(6)])
                label_color[end_label] = color
            
            obj_dict[end_name] = {
                "name" : end_name,
                "label" : end_label,
                "position" : end_position,
                "color" : color
            }
        
        if relation_name not in rel_dict.keys():
            # coloring
            if relation_label in label_color.keys():
                color = label_color[relation_label]
            else:
                color = "#"+''.join([random.choice('0123') for j in range(6)])
                label_color[relation_label] = color
            
            rel_dict[relation_name] = {
                "name" : relation_name,
                "label" : relation_label,
                "position" : relation_position,
                "color" : color
            }
            
    return obj_dict, rel_dict, edge_set, label_color

def make_position_color(node_lst:list) -> tuple:
    pos = {}
    for node in node_lst:
        pos[node[0]] = node[1]["position"][0:2]
    color = list(map(lambda node: node[1]["color"], node_lst))
    return pos, color
    

def draw_graph(objs, edge_set: set, obj_dict: dict, rel_dict: dict):
    # network X
    graph = nx.DiGraph()
    node_lst = []
    for key in obj_dict:
        obj = obj_dict[key]
        node = (
            key,
            {
                "name": key,
                "label": obj.get("label"),
                "position": obj.get("position"),
                "color": obj.get("color") 
            }
        )
        node_lst.append(node)
    rel_node_lst = []
    for key in rel_dict:
        rel = rel_dict[key]
        node = (
            key,
            {
                "name": key,
                "label": rel.get("label"),
                "position": rel.get("position"),
                "color": rel.get("color") 
            }
        )
        rel_node_lst.append(node)
    # obj node 추가
    graph.add_nodes_from(node_lst)

    # 각 node들의 위치를 생성하는 함수
    pos_obj, color_obj = make_position_color(node_lst)
    pos_rel, color_rel = make_position_color(rel_node_lst)
    # edge label 추가
    pos = pos_obj.copy()
    pos.update(pos_rel)
    """
    edge_dict = {
        (start_id, end_id): relations labels,
    }
    """
    obj_dict_copy = obj_dict.copy()
    obj_dict_copy.update(rel_dict)
    
    for edges in edge_set:
        graph.add_edge(obj_dict_copy[edges[0]]["name"], obj_dict_copy[edges[1]]["name"])

    labels = nx.get_edge_attributes(graph, "name")
    """
    s : square, o: circle, ^: triangle, > : right triangle, v : bottom triangle, < : left triangle
    d : diamond, p : pentagon, h : hexagon, 8 : octagonal
    """
    nx.draw(graph, pos, with_labels=False, nodelist=list(map(lambda node: node[0], node_lst)), node_size=700, node_shape='s', node_color=color_obj, linewidths=5)
    # nx.draw(graph, pos, with_labels=False, nodelist=list(map(lambda node: node[0], rel_node_lst)), node_size=100, node_shape='s', alpha=0.1, node_color=color_rel, linewidths=5)
    # nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels, alpha=0.5, label_pos=0.3, verticalalignment='top')
    nx.draw_networkx_edges(graph, pos)
    for node, (x, y) in pos.items():
        text(x, y, node, fontsize=8, ha='center', va='center')
    plt.show()

def visualizer_3d():
    # load class, relationships class
    c_lines, r_lines = load_classes("classes.txt", "relationships.txt")
    
    # load object, relationships instances data
    obj_scans, rel_scans = load_data("objects_sample.json", "relationships.json")

    # search all relations by scan
    for rel_scan in rel_scans:
        rels = rel_scan.get("relationships")
        scan = rel_scan.get("scan")
        # TEST
        # TODO : Delete this when it will be deployed
        if scan != "0988ea72-eb32-2e61-8344-99e2283c2728":
            continue
        # Check when the scan code of obj_scans same with it of rel_scans
        objs = find_objects_by_scan(scan, obj_scans)
        # Make edges & label by obj_id 
        obj_dict, rel_dict, edge_set, label_color = make_edges_objs(objs, rels)
        # Draw Graph
        draw_graph(objs, edge_set, obj_dict, rel_dict)
        break

visualizer_3d()

# if __name__ == '__main__':
#     visualizer_3d()