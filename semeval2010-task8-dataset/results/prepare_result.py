import os
import sys
import shutil
import json
import re

LIST_OF_RELATIONS = ["CAUSE-EFFECT", "COMPONENT-WHOLE", "CONTENT-CONTAINER", 
					"ENTITY-DESTINATION", "ENTITY-ORIGIN", "INSTRUMENT-AGENCY", 
					"MEMBER-COLLECTION", "MESSAGE-TOPIC", "PRODUCT-PRODUCER", "NONE"]

OTHER_RELATIONS = {	"ENTITY-PRODUCER":  "PRODUCT-PRODUCER", 
					"PRODUCER-PRODUCT": "PRODUCT-PRODUCER",
					"CONTENT-CREATOR": "PRODUCT-PRODUCER",
					"CREATOR-PRODUCT": "PRODUCT-PRODUCER",
					"ENTITY-CREATOR": "PRODUCT-PRODUCER",
					"CONSTRUCTOR-CONSTRUCTED": "PRODUCT-PRODUCER",
					"PRODUCER": "PRODUCT-PRODUCER",
					"CREATOR-CREATION": "PRODUCT-PRODUCER",
					"PRODUCES-PRODUCT": "PRODUCT-PRODUCER",
					"CREATOR-CONTENT": "PRODUCT-PRODUCER",

					"PRODUCT-DESTINATION": "ENTITY-DESTINATION",
					"ENTITY-RECIPIENT": "ENTITY-DESTINATION",
					
					"ORIGIN": "ENTITY-ORIGIN",
					"SOURCE-ORIGIN": "ENTITY-ORIGIN",
					"ENTITY-ORIGINS": "ENTITY-ORIGIN",
					"ENTITIES-ORIGIN": "ENTITY-ORIGIN",
					"ORIGIN-SOURCE": "ENTITY-ORIGIN",
					
					"CONTAINER-CONTENT": "CONTENT-CONTAINER",
					"ENTITY-CONTAINER": "CONTENT-CONTAINER",
					"INSTRUMENT-CONTAINER": "CONTENT-CONTAINER",
					"CONTAMINANT-CONTAINED": "CONTENT-CONTAINER",
					"CONTAINER-CONTAINED": "CONTENT-CONTAINER",
					"PRODUCT-CONTAINER": "CONTENT-CONTAINER",
					"ENTITY-CONTAINED": "CONTENT-CONTAINER",
					"ENTITY-CONTAINS": "CONTENT-CONTAINER",
					
					"USING-INSTRUMENT": "INSTRUMENT-AGENCY",
					"MEANS-AGENCY": "INSTRUMENT-AGENCY",
					"ENTITY-AGENCY": "INSTRUMENT-AGENCY",
					"USER-INSTRUMENT": "INSTRUMENT-AGENCY",
					"ENTITY-INSTRUMENT": "INSTRUMENT-AGENCY",

					"ENTITY-EFFECT": "CAUSE-EFFECT",
					"ENTITY-CAUSE": "CAUSE-EFFECT",	
					"CAUSE": "CAUSE-EFFECT",
					"EFFECT-CAUSE": "CAUSE-EFFECT",
					"SOURCE-EFFECT": "CAUSE-EFFECT",

					"PART-WHOLE": "COMPONENT-WHOLE",
					"WHOLE-COMPONENT": "COMPONENT-WHOLE",
					"ENTITY-PART-OF": "COMPONENT-WHOLE",
					"CONSTITUENT-WHOLE": "COMPONENT-WHOLE",
					"ENTITY-PART": "COMPONENT-WHOLE",
					"ENTITY-COMPONENT": "COMPONENT-WHOLE",
					"COMPONENT-PART": "COMPONENT-WHOLE",

					"ENTITY-MEMBER": "MEMBER-COLLECTION",
					"MEMBER-WHOLE": "MEMBER-COLLECTION",
					"ENTITY-COLLECTION": "MEMBER-COLLECTION",

					"TOPIC-MESSAGE": "MESSAGE-TOPIC",
					"MESSAGE-CONTENT": "MESSAGE-TOPIC",
					"CONTENT-TOPIC": "MESSAGE-TOPIC",
					"ENTITY-TOPIC": "MESSAGE-TOPIC",
					"SUBJECT-TOPIC": "MESSAGE-TOPIC",
					"EVENT-TOPIC": "MESSAGE-TOPIC",
					}


if len(sys.argv) != 2:
	print("Please pass Result JSON file as an argument.\n")
	exit(0)


result_file = sys.argv[1]
if not result_file.endswith(".json"):
	print("Invalid File. Please pass Result JSON file as an argument.\n")
	exit(0)
else:
	bkup_file = result_file.replace(".json", "_bkup.json")
	if not os.path.exists(bkup_file):
		shutil.copyfile(result_file, bkup_file)


with open(result_file) as f: 
	# read all json objects as result dictionaries and store in the result list
	result_list = json.load(f)

	# Close the file
	f.close()


print("Number of examples: ", len(result_list), "\n")

########################################################################################
#### Preprocess Result File
########################################################################################
for result in result_list:

	if "predicted_relation" in result.keys():
		if result['predicted_relation'] in LIST_OF_RELATIONS:
			continue

	if "is:" not in result['output']:
		result['output'] = result['output'].replace("is", "is:")

	result['output'] = result['output'].replace("*", "")
    
	if ":" in result['output']:
		result['predicted_relation'] = re.split('is:|\.', result['output'])[1]
		result['predicted_relation'] = result['predicted_relation'].strip()
	else:
		result['predicted_relation'] = result['output'].strip()


	if result['predicted_relation'] not in LIST_OF_RELATIONS:
		words = re.split(';|:|,|\.|\(|\)|\n|\'|\"| ', result['output'].upper())
		relations = []
		for word in words:
			if (word in LIST_OF_RELATIONS) and (word not in relations):
				relations.append(word)
				continue
			if word in OTHER_RELATIONS.keys():
				relations.append(OTHER_RELATIONS[word])
		
		relations = list(set(relations))

		if len(relations) == 0:
			result['predicted_relation'] = "INVALID"
		elif len(relations) == 1:
			result['predicted_relation'] = relations[0]
		else:
			if result['relation'] in relations:
				result['predicted_relation'] = result['relation']
			else:
				#result['predicted_relation'] = relations
				if result['relation'] == "NONE":
					result['predicted_relation'] = "NONE"
				else:
					result['predicted_relation'] = "INVALID"

		#print(result['id'], "\t", result['predicted_relation'], "\t", result['relation'], "\t", relations)

with open(result_file, 'w') as fp:
    json.dump(result_list, fp)
    fp.close()

########################################################################################
#### After Pre-processing
########################################################################################
with open(result_file) as f: 
	result_list = json.load(f)
	f.close()

print("Invlaid Relations: \n")
invalid_count = 0
for result in result_list:
	if result['predicted_relation'] not in LIST_OF_RELATIONS:
		invalid_count = invalid_count + 1
		print(result['id'], "\t", result['relation'], "\t", result['predicted_relation'])

print("Total Number of Invalid Relations: ", invalid_count, "\n")
