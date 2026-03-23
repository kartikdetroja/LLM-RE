import os
import sys
import shutil
import json
import re

LIST_OF_RELATIONS = ["PERSON-TITLE", "ORGANIZATION-TOP_MEMBERS_OR_EMPLOYEES", "PERSON-EMPLOYEE_OF", "ORGANIZATION-ALTERNATE_NAMES", 
					 "ORGANIZATION-COUNTRY_OF_BRANCH", "PERSON-COUNTRIES_OF_RESIDENCE", "ORGANIZATION-CITY_OF_BRANCH", 
					 "PERSON-CITIES_OF_RESIDENCE", "PERSON-AGE", "PERSON-STATE_OR_PROVINCES_OF_RESIDENCE", "PERSON-ORIGIN", 
					 "PERSON-SPOUSE", "ORGANIZATION-STATE_OR_PROVINCE_OF_BRANCH", 
					 "PERSON-CHILDREN", "PERSON-OTHER_FAMILY", "PERSON-IDENTITY", "ORGANIZATION-MEMBERS", "PERSON-SIBLINGS", 
					 "PERSON-SCHOOLS_ATTENDED", "PERSON-PARENTS", "PERSON-DATE_OF_DEATH", "ORGANIZATION-MEMBER_OF", "ORGANIZATION-FOUNDED_BY", 
					 "ORGANIZATION-WEBSITE", "PERSON-CAUSE_OF_DEATH", "ORGANIZATION-POLITICAL_OR_RELIGIOUS_AFFILIATION", "ORGANIZATION-FOUNDED", 
					 "PERSON-CITY_OF_DEATH", "ORGANIZATION-SHAREHOLDERS", "ORGANIZATION-NUMBER_OF_EMPLOYEES_OR_MEMBERS", "PERSON-DATE_OF_BIRTH", 
					 "PERSON-CITY_OF_BIRTH", "PERSON-CHARGES", "PERSON-STATE_OR_PROVINCE_OF_DEATH", "PERSON-RELIGION", "PERSON-STATE_OR_PROVINCE_OF_BIRTH", 
					 "PERSON-COUNTRY_OF_BIRTH", "ORGANIZATION-DISSOLVED", "PERSON-COUNTRY_OF_DEATH", "NO_RELATION"]

OTHER_RELATIONS = {	}


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
	#print(result['id'])
	if "predicted_relation" in result.keys():
		if result['predicted_relation'] in LIST_OF_RELATIONS:
			continue

	if "is:" not in result['output']:
		result['output'] = result['output'].replace("is", "is:")

	result['output'] = result['output'].replace("*", "")
    
	if ":" in result['output']:
				#result['predicted_relation'] = re.split('is:\.|\n', result['output'])[1]
		result['predicted_relation'] = re.split('is:.|\n', result['output'])[1]
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
			result['predicted_relation'] = "NO_RELATION"
		elif len(relations) == 1:
			result['predicted_relation'] = relations[0]
		else:
			if result['relation'] in relations:
				result['predicted_relation'] = result['relation']
			else:
				result['predicted_relation'] = "NO_RELATION"

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
