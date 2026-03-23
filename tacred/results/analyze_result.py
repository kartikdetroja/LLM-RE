import os
import sys
import json

import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix

COL_WIDTH = 8
HEAD_WIDTH = 110


if len(sys.argv) != 2:
	print("Please pass Result JSON file as an argument.\n")
	exit(0)

result_file = sys.argv[1]
if not result_file.endswith(".json"):
	print("Invalid File. Please pass Result JSON file as an argument.\n")
	exit(0)


config_file = os.path.join(os.path.split(result_file)[0], "config.json")
if not os.path.exists(config_file):
	print("Config file doesnot exists")
	exit(0)

result_analysis_file = result_file.replace("result_", "result_analysis_").replace(".json", ".log")
log_file = open(result_analysis_file, 'w')


with open(config_file) as fp_config: 
	# read all json objects as configurations dictionaries and store in the result list
	config = json.load(fp_config)
	fp_config.close()


print("#"*HEAD_WIDTH, file=log_file)
print("Configurations:\n", file=log_file)
for key in config:
	print(key, " = ", config[key], file=log_file)


with open(result_file) as fp_result: 
	# read all json objects as result dictionaries and store in the result list and close
	result_list = json.load(fp_result)
	fp_result.close()


LIST_OF_RELATIONS = ["PERSON-TITLE", "ORGANIZATION-TOP_MEMBERS_OR_EMPLOYEES", "PERSON-EMPLOYEE_OF", "ORGANIZATION-ALTERNATE_NAMES", 
					 "ORGANIZATION-COUNTRY_OF_HEADQUARTERS", "PERSON-COUNTRIES_OF_RESIDENCE", "ORGANIZATION-CITY_OF_HEADQUARTERS", 
					 "PERSON-CITIES_OF_RESIDENCE", "PERSON-AGE", "PERSON-STATE_OR_PROVINCES_OF_RESIDENCE", "PERSON-ORIGIN", 
					 "ORGANIZATION-SUBSIDIARIES", "ORGANIZATION-PARENTS", "PERSON-SPOUSE", "ORGANIZATION-STATE_OR_PROVINCE_OF_HEADQUARTERS", 
					 "PERSON-CHILDREN", "PERSON-OTHER_FAMILY", "PERSON-ALTERNATE_NAMES", "ORGANIZATION-MEMBERS", "PERSON-SIBLINGS", 
					 "PERSON-SCHOOLS_ATTENDED", "PERSON-PARENTS", "PERSON-DATE_OF_DEATH", "ORGANIZATION-MEMBER_OF", "ORGANIZATION-FOUNDED_BY", 
					 "ORGANIZATION-WEBSITE", "PERSON-CAUSE_OF_DEATH", "ORGANIZATION-POLITICAL_OR_RELIGIOUS_AFFILIATION", "ORGANIZATION-FOUNDED", 
					 "PERSON-CITY_OF_DEATH", "ORGANIZATION-SHAREHOLDERS", "ORGANIZATION-NUMBER_OF_EMPLOYEES_OR_MEMBERS", "PERSON-DATE_OF_BIRTH", 
					 "PERSON-CITY_OF_BIRTH", "PERSON-CHARGES", "PERSON-STATE_OR_PROVINCE_OF_DEATH", "PERSON-RELIGION", "PERSON-STATE_OR_PROVINCE_OF_BIRTH", 
					 "PERSON-COUNTRY_OF_BIRTH", "ORGANIZATION-DISSOLVED", "PERSON-COUNTRY_OF_DEATH", "NO_RELATION"]

#ALT_REL_NAME = {}
#ALT_REL_NAME["CAUSE-EFFECT"] = "CE"
#ALT_REL_NAME["COMPONENT-WHOLE"] = "CW"
#ALT_REL_NAME["CONTENT-CONTAINER"] = "CC"
#ALT_REL_NAME["ENTITY-DESTINATION"] = "ED"
#ALT_REL_NAME["ENTITY-ORIGIN"] = "EO"
#ALT_REL_NAME["INSTRUMENT-AGENCY"] = "IA"
#ALT_REL_NAME["MEMBER-COLLECTION"] = "MC"
#ALT_REL_NAME["MESSAGE-TOPIC"] = "MT"
#ALT_REL_NAME["PRODUCT-PRODUCER"] = "PP"
#ALT_REL_NAME["NONE"] = "NN"
#ALT_REL_NAME["INVALID"] = "IV"

for res in result_list:
	if (res['predicted_relation'] not in LIST_OF_RELATIONS):
		res['predicted_relation'] = "NO_RELATION"

rel_predicted = []
rel_actual = []
for res in result_list:
	rel_actual.append(res['relation'])
	rel_predicted.append(res['predicted_relation'])


#con_matrix = confusion_matrix(rel_actual, rel_predicted, labels=LIST_OF_RELATIONS)
##print(type(con_matrix))
#
## print header of confusion matrix
#print("#"*HEAD_WIDTH, "\n", file=log_file)
#print("Confusion Matrix".center(HEAD_WIDTH), "\n", file=log_file)
#
#
#print("".center(COL_WIDTH), end="", file=log_file)
#for i, rel in enumerate(LIST_OF_RELATIONS):
#	print(ALT_REL_NAME[rel].ljust(COL_WIDTH), end="", file=log_file)
#
#print("TOTAL".ljust(COL_WIDTH), file=log_file)
#print("-"*HEAD_WIDTH, file=log_file)
#
#
#actual_str = "ACTUAL ".center(len(LIST_OF_RELATIONS))
#predicted_str = "P R E D I C T E D"
#
#conf_matrix_row_sum = np.sum(con_matrix, axis=1)
#conf_matrix_col_sum = np.sum(con_matrix, axis=0)
#conf_matrix_tot_sum = np.sum(con_matrix)
#
## print confusion matrix
#for i, rel in enumerate(LIST_OF_RELATIONS):
#	print(ALT_REL_NAME[rel].ljust(COL_WIDTH), end="", file=log_file)
#
#	for j in range(len(LIST_OF_RELATIONS)):
#		print(str(con_matrix[i][j]).ljust(COL_WIDTH), end="", file=log_file)
#	
#	print(str(conf_matrix_row_sum[i]).ljust(COL_WIDTH), end="", file=log_file)
#
#	print(str(actual_str[i]).ljust(COL_WIDTH), file=log_file)
#
#print("-"*HEAD_WIDTH, file=log_file)
#
#
#print("TOTAL".ljust(COL_WIDTH), end="", file=log_file)
#for i, rel in enumerate(LIST_OF_RELATIONS):
#	print(str(conf_matrix_col_sum[i]).ljust(COL_WIDTH), end="", file=log_file)
#
#print(str(conf_matrix_tot_sum).ljust(COL_WIDTH), end="", file=log_file)
#
#print("\n\n" + predicted_str.center(HEAD_WIDTH), file=log_file)
#
#print("\n\nTotal number of Examples: ", conf_matrix_tot_sum, "\n", file=log_file)
#print("#"*HEAD_WIDTH, file=log_file)

print("#"*HEAD_WIDTH, file=log_file)

macro_f1 = f1_score(rel_actual, rel_predicted, average='macro', labels=LIST_OF_RELATIONS)
macro_precision = precision_score(rel_actual, rel_predicted, average='macro', labels=LIST_OF_RELATIONS)
macro_recall = recall_score(rel_actual, rel_predicted, average='macro', labels=LIST_OF_RELATIONS)
print("\nMacro F1 score = ", macro_f1, file=log_file)
print("Precision: ", macro_precision, file=log_file)
print("Recall: ", macro_recall, file=log_file)


weighted_f1 = f1_score(rel_actual, rel_predicted, average='weighted', labels=LIST_OF_RELATIONS)
weighted_precision = precision_score(rel_actual, rel_predicted, average='weighted', labels=LIST_OF_RELATIONS)
weighted_recall = recall_score(rel_actual, rel_predicted, average='weighted', labels=LIST_OF_RELATIONS)
print("\nWeighted F1 score = ", weighted_f1, file=log_file)
print("Precision: ", weighted_precision, file=log_file)
print("Recall: ", weighted_recall, file=log_file)


micro_f1 = f1_score(rel_actual, rel_predicted, average='micro', labels=LIST_OF_RELATIONS)
micro_precision = precision_score(rel_actual, rel_predicted, average='micro', labels=LIST_OF_RELATIONS)
micro_recall = recall_score(rel_actual, rel_predicted, average='micro', labels=LIST_OF_RELATIONS)
print("\nMicro F1 score = ", micro_f1, file=log_file)
print("Precision: ", micro_precision, file=log_file)
print("Recall: ", micro_recall, file=log_file)

class_f1_scores = f1_score(rel_actual, rel_predicted, average=None, labels=LIST_OF_RELATIONS)
print("\nClasswise F1 scores:", file=log_file)
for i, score in enumerate(class_f1_scores):
	print("\t", LIST_OF_RELATIONS[i], ": ", round(score, 2), sep="", file=log_file)

print("#"*HEAD_WIDTH, file=log_file)
