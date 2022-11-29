import json
import os
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 

def load_obj_json(obj_file_name: str) -> list:
    with open(os.path.join(BASE_DIR, "3DSSG", obj_file_name), "r") as obj_file:
        obj_scans = json.load(obj_file).get("scans")
        # obj_scans : scan list
    return obj_scans

def find_objects_by_scan(scan: str, obj_scans: list) -> list:
    for obj_scan in obj_scans:
        if obj_scan.get("scan") == scan:
            return obj_scan.get("objects")
    return None

def find_obj(objs, obj_id) -> object:
    for obj in objs:
        if obj_id == int(obj["id"]):
            return obj
    return None

# class Object3DSSG():
#     def __init__(self) -> None:

def make_random_position(rand_range:int) -> list:
    # 0~rand_range 사이 random float list (ex - [24.14, 27.25, 2.54])
    pos = [round(random.random() * rand_range ,2) for val in range(0,3)]
    return pos

def pop_key(object, obj_keys: list, attr_keys: list) -> object:
    obj_origin_keys = list(object.keys()).copy()
    for obj_key in obj_origin_keys:
        if obj_key not in obj_keys:
            object.pop(obj_key)
        attr = object.get("attributes")
        attr_origin_keys = list(attr.keys()).copy()
        if attr is not None:
            for attr_key in attr_origin_keys:
                if attr_key not in attr_keys:
                    attr.pop(attr_key)
    
    object["attributes"] = attr
    return object
    
def make_json_with_pos(obj_file_name: str, new_file_path: str):
    # new file path can be the relative path
    obj_scans = load_obj_json(obj_file_name=obj_file_name)
    scan_id = "0988ea72-eb32-2e61-8344-99e2283c2728"
    objects = find_objects_by_scan(scan=scan_id, obj_scans=obj_scans)
    
    obj_keys = ["label", "id", "global_id", "attributes", "position"]
    attr_keys = ["color", "shape", "state", "size"]
    
    random_range = 50
    for object in objects:
        pop_key(object, obj_keys, attr_keys)
        object["position"] = make_random_position(random_range)
    
    output = {
        "scans" : [
            {
                "scan" : "0988ea72-eb32-2e61-8344-99e2283c2728",
                "objects" : objects
            }
        ]
    }
    
    with open(new_file_path, 'w') as outfile:
        json.dump(output, outfile, indent=4)
        
obj_file_name = "objects.json"
new_file_path = "graphgen/networkx/ACSL/objects_sample.json"

make_json_with_pos(obj_file_name, new_file_path)