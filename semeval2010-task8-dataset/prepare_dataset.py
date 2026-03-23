import os
import sys
import json

relation_mapping = {
    'Cause-Effect(e1,e2)' : "CAUSE-EFFECT",
    'Cause-Effect(e2,e1)' : "CAUSE-EFFECT",
    'Component-Whole(e1,e2)' : "COMPONENT-WHOLE",
    'Component-Whole(e2,e1)' : "COMPONENT-WHOLE",
    'Content-Container(e1,e2)' : "CONTENT-CONTAINER",
    'Content-Container(e2,e1)' : "CONTENT-CONTAINER",
    'Entity-Destination(e1,e2)' : "ENTITY-DESTINATION",
    'Entity-Destination(e2,e1)' : "ENTITY-DESTINATION",
    'Entity-Origin(e1,e2)' : "ENTITY-ORIGIN",
    'Entity-Origin(e2,e1)' : "ENTITY-ORIGIN",
    'Instrument-Agency(e1,e2)' : "INSTRUMENT-AGENCY",
    'Instrument-Agency(e2,e1)' : "INSTRUMENT-AGENCY",
    'Member-Collection(e1,e2)' : "MEMBER-COLLECTION",
    'Member-Collection(e2,e1)' : "MEMBER-COLLECTION",
    'Message-Topic(e1,e2)' : "MESSAGE-TOPIC",
    'Message-Topic(e2,e1)' : "MESSAGE-TOPIC",
    'Product-Producer(e1,e2)' : "PRODUCT-PRODUCER",
    'Product-Producer(e2,e1)' : "PRODUCT-PRODUCER",
    'Other' : "NONE"
}

# patterns around the entities 1 and 2
e1_start_pattern = "<e1>"
e1_end_pattern = "</e1>"
e2_start_pattern = "<e2>"
e2_end_pattern = "</e2>"


dataset_dir = sys.argv[1]

files = os.listdir(dataset_dir)
dataset_files = []
for file in files:
    if ".json" in file:
        dataset_files.append(file)


for ex_file in dataset_files:
    
    old_examples = []
    # open the JSON file
    with open(os.path.join(dataset_dir, ex_file)) as ex_file_hndlr: 
        
        # read all json objects as example dictionaries and store in the example list
        for json_obj in ex_file_hndlr:
            example = json.loads(json_obj)
            old_examples.append(example)

        # Close the file
        ex_file_hndlr.close()

    new_example_list = [ ]
    for old_ex in old_examples:
        new_ex = {}

        text = " ".join(old_ex['sentence'])
        #print(text)
        
        # get Entity-1
        idx1 = text.index(e1_start_pattern) + len(e1_start_pattern)
        idx2 = text.index(e1_end_pattern)
        en_1 = text[idx1: idx2].strip()

        # get Entity-2
        idx1 = text.index(e2_start_pattern) + len(e2_start_pattern)
        idx2 = text.index(e2_end_pattern)
        en_2 = text[idx1: idx2].strip()

        # remove <e1>, </e1>, <e2> and </e2> from the text
        text = text.replace("<e1> ", "").replace("</e1> ", "").replace("<e2> ", "").replace("</e2> ", "")


        new_ex["id"] = old_ex["id"]
        new_ex["relation"] = relation_mapping[old_ex['relation']]
        new_ex["sentence"] = text
        new_ex["e1"] = en_1
        new_ex["e2"] = en_2
        #print(new_ex, "\n")

        new_example_list.append(new_ex)
        
    
    with open(os.path.join("dataset", ex_file), 'w') as fp:
        json.dump(new_example_list, fp)
        fp.close()
