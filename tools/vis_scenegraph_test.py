import networkx as nx
import graphviz
import json
import argparse
import webcolors


parser = argparse.ArgumentParser()

parser.add_argument('--obj_path', default='/home/dongmin/Downloads/3DSSG/objects.json')
parser.add_argument('--rel_path', default='/home/dongmin/Downloads/3DSSG/relationships.json')
parser.add_argument('--scene_num', default=4)

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


scan_id = objects["scans"][scene_num]["scan"]
for relationship_num in range(len(relationships["scans"])):
    if relationships["scans"][relationship_num]["scan"] == scan_id:
        scan_rel_num = relationship_num
        break

print(scan_id)
print(json.dumps(relationships["scans"][scan_rel_num]["relationships"], indent="\t") )
#networkx setup
G = nx.Graph()
dg = graphviz.Digraph()
tomato_rgb = [236,93,87]
blue_rgb = [81,167,250]
pale_rgb = [112,191,64]
pale_hex = webcolors.rgb_to_hex(pale_rgb)
tomato_hex = webcolors.rgb_to_hex(tomato_rgb)
blue_hex = webcolors.rgb_to_hex(blue_rgb)
#import object node
for object_num in range(len(objects["scans"][scene_num]["objects"])):
    object = objects["scans"][scene_num]["objects"][object_num]

    #object class
    dg.node(("objects_" + str(object["id"])), shape='box', style='filled,rounded',
            label= (str(object["label"]) + "_" + str(object["id"])),
            margin= '0.11, 0.11', width='0.11', height='0',
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
for relationship_num in range(len(relationships["scans"][scan_rel_num]["relationships"])):
    relationship = relationships["scans"][scan_rel_num]["relationships"][relationship_num]
    #sorting 후 선 하나로 나타내기
    #relation class
    if relationship[2] < 27 or relationship[2] > 32:
        """dg.node(("relationship_" + str(relationship_num)), shape='box', style='filled,rounded',
                label= (relationship[3]),
                margin= '0.11, 0.0001', width='0.11', height='0',
                fillcolor= pale_hex, fontcolor = 'black')
        dg.edge(("objects_" + str(relationship[0])), ("relationship_" + str(relationship_num)))
        dg.edge(("relationship_" + str(relationship_num)), ("objects_" + str(relationship[1])))"""
        dg.edge(("objects_" + str(relationship[0])), ("objects_" + str(relationship[1])))


dg.render("/home/dongmin/Scene-Graph-Dataset-Generator/results/test", view=True)




  