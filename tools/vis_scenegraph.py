import networkx as nx
import graphviz
import json
import argparse
import webcolors


parser = argparse.ArgumentParser()

parser.add_argument('--obj_path', default='/home/dongmin/Downloads/3DSSG/objects.json')
parser.add_argument('--rel_path', default='/home/dongmin/Downloads/3DSSG/relationships.json')
parser.add_argument('--scene_num', default=0)

args = parser.parse_args()

scene_num = args.scene_num

def save_graph_as_svg(dot_string, output_file_name):
    if type(dot_string) is str:
        g = graphviz.Source(dot_string)
    elif isinstance(dot_string, (graphviz.Digraph, graphviz.Graph)):
        g = dot_string
    g.format='svg'
    g.filename = output_file_name
    g.directory = '../results/'
    g.render(view=False)
    return g

print("Loading Json File...")
with open(args.obj_path) as f:
    print(args.obj_path)
    objects = json.load(f)

with open(args.rel_path) as f:
    print(args.rel_path)
    relationships = json.load(f)
print("Finish!")

print(json.dumps(relationships["scans"][scene_num], indent="\t"))

#networkx setup
G = nx.Graph()
dg = graphviz.Digraph()
tomato_rgb = [236,93,87]
blue_rgb = [81,167,250]
tomato_hex = webcolors.rgb_to_hex(tomato_rgb)
blue_hex = webcolors.rgb_to_hex(blue_rgb)

#import object node
for object_num in range(len(objects["scans"][scene_num]["objects"])):
    object = objects["scans"][scene_num]["objects"][object_num]

    #object class
    dg.node(("objects_" + str(object["id"])), shape='box', style='filled,rounded',
            label= (str(object["label"]) + "_" + str(object["id"])),
            margin= '0.11, 0.0001', width='0.11', height='0',
            fillcolor= tomato_hex, fontcolor = 'black')
    
    #attributes
    for i in range(len(object["attributes"])):
        list_keys = list(object["attributes"].keys())
        for attribute_num in range(len(object["attributes"][list_keys[i]])):
            attribute = object["attributes"][list_keys[i]][attribute_num]
            dg.node(("objects_" + str(object["id"]) + attribute), shape='box', style='filled,rounded',
                    label= (attribute),
                    margin= '0.11, 0.0001', width='0.11', height='0',
                    fillcolor= blue_hex, fontcolor = 'black')
            dg.edge(("objects_" + str(object["id"])), ("objects_" + str(object["id"]) + attribute))

#import relation node

dg.render("/home/dongmin/Scene-Graph-Dataset-Generator/results/test", view=True)




  