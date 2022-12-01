import os
import json
import pprint
import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from matplotlib.pyplot import text
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d

from networkx_viewer import Viewer

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
    edge_dict = {}
    # To save label by obj_id
    obj_dict = {}
    label_color = {}
    
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
        if start_id not in obj_dict.keys():
            start_obj = find_obj(objs, start_id)
            start_label = start_obj.get("label").replace(" ", "\n")
            start_position = start_obj.get("position")
            
            # coloring
            if start_label in label_color.keys():
                color = label_color[start_label]
            else:
                color = "#"+''.join([random.choice('789ABCDEF') for j in range(6)]) 
                label_color[start_label] = color
            
            obj_dict[start_id] = {
                "name" :  start_label + "\n" + str(start_id),
                "label" : start_label,
                "position" : start_position,
                "color" : color
            }
            
        if end_id not in obj_dict.keys():
            end_obj = find_obj(objs, end_id)
            end_label = end_obj.get("label").replace(" ", "\n")
            end_position = end_obj.get("position")
            
            # coloring
            if end_label in label_color.keys():
                color = label_color[end_label]
            else:
                color = "#"+''.join([random.choice('789ABCDEF') for j in range(6)])
                label_color[end_label] = color
            
            obj_dict[end_id] = {
                "name" : end_label +"\n"+str(end_id),
                "label" : end_label,
                "position" : end_position,
                "color" : color
            }
            
    return obj_dict, edge_dict, label_color

def make_position_color(node_lst:list) -> tuple:
    pos = {}
    for node in node_lst:
        pos[node[0]] = node[1]["position"]
    color = list(map(lambda node: node[1]["color"], node_lst))
    return pos, color

def draw_graph(objs, edge_dict: dict, obj_dict: dict):
    # network X
    graph = nx.DiGraph()
    node_lst = []
    node_pos = []
    for id in obj_dict:
        obj = obj_dict[id]
        node = (
            obj.get("name"),
            {
                "id": id,
                "label": obj.get("label"),
                "position": obj.get("position"),
                "color": obj.get("color") 
            }
        )
        node_lst.append(node)
        print(obj.get("position"))
        node_pos.append(obj.get("position"))
    # obj node 추가
    node_xyz = np.array(node_pos)
    graph.add_nodes_from(node_lst)

    # 각 node들의 위치를 생성하는 함수
    pos, color = make_position_color(node_lst)
    
    # edge label 추가
    """
    edge_dict = {
        (start_id, end_id): relations labels,
    }
    """
    
    edge_pos = []
    edge_lst = []
    for edges in edge_dict:
        graph.add_edge(obj_dict[edges[0]]["name"], obj_dict[edges[1]]["name"], name=edge_dict[edges][:-2])
        start_pos, end_pos = obj_dict[edges[0]]["position"], obj_dict[edges[1]]["position"]
        edge_pos.append((start_pos, end_pos))
        edge_lst.append(edge_dict[edges][:-2])
    edge_xyz = np.array(edge_pos)
        
    labels = nx.get_edge_attributes(graph, "name")
    """
    s : square, o: circle, ^: triangle, > : right triangle, v : bottom triangle, < : left triangle
    d : diamond, p : pentagon, h : hexagon, 8 : octagonal
    """
    # nx.draw(graph, pos, with_labels=False, node_size=700, node_shape='s', node_color=color, linewidths=5)
    # nx.draw_networkx_edges(graph, pos, alpha=0.5)
    # for node, (x, y) in pos.items():
    #    text(x, y, node, fontsize=8, ha='center', va='center')
    
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")
    # ax.scatter(*node_xyz.T, ec="w")

    for i in range(len(node_xyz)):
        ax.scatter(np.array(node_xyz[i,0]), np.array(node_xyz[i,1]), np.array(node_xyz[i,2]), s=400, ec="w", c=node_lst[i][1]["color"], alpha=0.4)
        ax.text(node_xyz[i,0], node_xyz[i,1], node_xyz[i,2], '%s'%node_lst[i][1]["label"], size=10, color="black", visible=True, wrap=True, fontweight=1000)

    for vizedge in edge_xyz:
        ax.plot(*vizedge.T, color="tab:gray")
        
    _format_axes(ax)
    def distance(edge, event):
        """Return distance between mouse position and given data point

        Args:
            point (np.array): np.array of shape (3,), with x,y,z in data coords
            event (MouseEvent): mouse event (which contains mouse position in .x and .xdata)
        Returns:
            distance (np.float64): distance (in screen coords) between mouse pos and data point
        """
        point = (edge[0]+edge[1])/2
        assert point.shape == (3,), "distance: point.shape is wrong: %s, must be (3,)" % point.shape

        # Project 3d data space to 2d data space
        x2, y2, _ = proj3d.proj_transform(point[0], point[1], point[2], plt.gca().get_proj())
        # Convert 2d data space to 2d screen space
        x3, y3 = ax.transData.transform((x2, y2))

        return np.sqrt ((x3 - event.x)**2 + (y3 - event.y)**2)


    def calcClosestDatapoint(X, event):
        """"Calculate which data point is closest to the mouse position.

        Args:
            X (np.array) - array of points, of shape (numPoints, 3)
            event (MouseEvent) - mouse event (containing mouse position)
        Returns:
            smallestIndex (int) - the index (into the array of points X) of the element closest to the mouse position
        """
        # edgepose -> start_end tuple
        distances = [distance (X[i], event) for i in range(X.shape[0])]
        return np.argmin(distances)


    def annotatePlot(edge_pos, index):
        """Create popover label in 3d chart

        Args:
            X (np.array) - array of points, of shape (numPoints, 3)
            index (int) - index (into points array X) of item which should be printed
        Returns:
            None
        """
        # If we have previously displayed another label, remove it first
        if hasattr(annotatePlot, 'label'):
            annotatePlot.label.remove()
        X =(edge_pos[index][0]+edge_pos[index][1])/2
        # Get data point from array of points X, at position index
        x2, y2, _ = proj3d.proj_transform(X[0], X[1], X[2], ax.get_proj())
        annotatePlot.label = plt.annotate( "%s" % edge_lst[index],
            xy = (x2, y2), xytext = (-20, 20), textcoords = 'offset points', ha = 'right', va = 'bottom',
            bbox = dict(boxstyle = 'round,pad=0.5', fc = 'lightblue', alpha = 0.5),
            arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
        fig.canvas.draw()


    def onMouseMotion(event):
        """Event that is triggered when mouse is moved. Shows text annotation over data point closest to mouse."""
        closestIndex = calcClosestDatapoint(np.array(edge_pos), event)
        annotatePlot (np.array(edge_pos), closestIndex)

    fig.canvas.mpl_connect('motion_notify_event', onMouseMotion)  # on mouse motion
    # fig.tight_layout()
    plt.show()
    
def _format_axes(ax):
    """
    Visualization options for the 3D axes.
    """
    # Turn gridlines off
    ax.grid(False)
    # Suppress tick labels
    for dim in (ax.xaxis, ax.yaxis, ax.zaxis):
        dim.set_ticks([])
    # Set axes labels
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
        

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
        obj_dict, edge_dict, label_color = make_edges_objs(objs, rels)
        # Draw Graph
        draw_graph(objs, edge_dict, obj_dict)
        break

visualizer_3d()

# if __name__ == '__main__':
#     visualizer_3d()