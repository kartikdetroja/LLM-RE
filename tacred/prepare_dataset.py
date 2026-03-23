import os
import sys
import json

org_dataset_dir = sys.argv[1]
dataset_files = os.listdir(org_dataset_dir)
#print(dataset_files)

relations_dict = {'no_relation': 'NO_RELATION', 'per:title': 'PERSON-TITLE', 
                'org:top_members/employees': 'ORGANIZATION-TOP_MEMBERS_OR_EMPLOYEES', 
                'per:employee_of': 'PERSON-EMPLOYEE_OF', 'org:alternate_names': 'ORGANIZATION-ALTERNATE_NAMES', 
                'org:country_of_headquarters': 'ORGANIZATION-COUNTRY_OF_HEADQUARTERS', 
                'per:countries_of_residence': 'PERSON-COUNTRIES_OF_RESIDENCE', 
                'org:city_of_headquarters': 'ORGANIZATION-CITY_OF_HEADQUARTERS', 'per:cities_of_residence': 'PERSON-CITIES_OF_RESIDENCE', 
                'per:age': 'PERSON-AGE', 'per:stateorprovinces_of_residence': 'PERSON-STATE_OR_PROVINCE_OF_RESIDENCE', 
                'per:origin': 'PERSON-ORIGIN', 'org:subsidiaries': 'ORGANIZATION-SUBSIDIARIES', 
                'org:parents': 'ORGANIZATION-PARENTS', 'per:spouse': 'PERSON-SPOUSE', 
                'org:stateorprovince_of_headquarters': 'ORGANIZATION-STATE_OR_PROVINCE_OF_HEADQUARTERS', 
                'per:children': 'PERSON-CHILDREN', 'per:other_family': 'PERSON-OTHER_FAMILY', 
                'per:alternate_names': 'PERSON-ALTERNATE_NAMES', 'org:members': 'ORGANIZATION-MEMBERS', 
                'per:siblings': 'PERSON-SIBLINGS', 'per:schools_attended': 'PERSON-SCHOOLS_ATTENDED', 
                'per:parents': 'PERSON-PARENTS', 'per:date_of_death': 'PERSON-DATE_OF_DEATH', 
                'org:member_of': 'ORGANIZATION-MEMBER_OF', 'org:founded_by': 'ORGANIZATION-FOUNDED_BY', 
                'org:website': 'ORGANIZATION-WEBSITE', 'per:cause_of_death': 'PERSON-CAUSE_OF_DEATH', 
                'org:political/religious_affiliation': 'ORGANIZATION-POLITICAL_OR_RELIGIOUS_AFFILIATION', 
                'org:founded': 'ORGANIZATION-FOUNDED', 'per:city_of_death': 'PERSON-CITY_OF_DEATH', 
                'org:shareholders': 'ORGANIZATION-SHAREHOLDERS', 
                'org:number_of_employees/members': 'ORGANIZATION-NUMBER_OF_EMPLOYEES_OR_MEMBERS', 
                'per:date_of_birth': 'PERSON-DATE_OF_BIRTH', 'per:city_of_birth': 'PERSON-CITY_OF_BIRTH', 
                'per:charges': 'PERSON-CHARGES', 'per:stateorprovince_of_death': 'PERSON-STATE_OR_PROVINCE_OF_DEATH', 
                'per:religion': 'PERSON-RELIGION', 'per:stateorprovince_of_birth': 'PERSON-STATE_OR_PROVINCE_OF_BIRTH', 
                'per:country_of_birth': 'PERSON-COUNTRY_OF_BIRTH', 'org:dissolved': 'ORGANIZATION-DISSOLVED', 
                'per:country_of_death': 'PERSON-COUNTRY_OF_DEATH'}

for ex_file in dataset_files:
    with open(os.path.join(org_dataset_dir, ex_file)) as ex_file_hndlr: 
        # read all json objects as configurations dictionaries and store in the result list
        old_examples = json.load(ex_file_hndlr)
        ex_file_hndlr.close()

    new_example_list = [ ]
    for ex_id, old_ex in enumerate(old_examples):
        new_ex = {}

        new_ex["id"] = str(ex_id + 1)
        new_ex["relation"] = relations_dict[old_ex["relation"]]
        new_ex["sentence"] = " ".join(old_ex["token"])
        new_ex["e1"] = " ".join(old_ex["token"][old_ex["subj_start"]:old_ex["subj_end"] + 1])
        new_ex["e2"] = " ".join(old_ex["token"][old_ex["obj_start"]:old_ex["obj_end"]+1])
        new_ex["sub_type"] = old_ex["subj_type"]
        new_ex["obj_type"] = old_ex["obj_type"]
        #print(new_ex, "\n")

        new_example_list.append(new_ex)

    with open(os.path.join("dataset", ex_file), 'w') as fp:
        json.dump(new_example_list, fp)
        fp.close()
