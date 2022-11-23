import json
 


with open('redline_ids.json', 'r') as openfile:
 
    json_object = json.load(openfile)


name_to_id_dict = {}
zipcode_to_id_dict = {}

for i, each in enumerate(json_object):
    name_to_id_dict[each["name"]] = each["id"]


    if "zipcode" in each:
        zipcode_to_id_dict[each["zipcode"]] = each["id"]


with open("name_to_id.json", "w") as outfile:

    outfile.write(json.dumps(name_to_id_dict, indent=4))
 

with open("zipcode_to_id.json", "w") as outfile:

    outfile.write(json.dumps(zipcode_to_id_dict, indent=4))

