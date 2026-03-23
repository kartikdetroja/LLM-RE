rel_list = [
"no_relation",
"per:title",
"org:top_members/employees",
"per:employee_of",
"org:alternate_names",
"org:country_of_headquarters",
"per:countries_of_residence",
"org:city_of_headquarters",
"per:cities_of_residence",
"per:age",
"per:stateorprovinces_of_residence",
"per:origin",
"org:subsidiaries",
"org:parents",
"per:spouse",
"org:stateorprovince_of_headquarters",
"per:children",
"per:other_family",
"per:alternate_names",
"org:members",
"per:siblings",
"per:schools_attended",
"per:parents",
"per:date_of_death",
"org:member_of",
"org:founded_by",
"org:website",
"per:cause_of_death",
"org:political/religious_affiliation",
"org:founded",
"per:city_of_death",
"org:shareholders",
"org:number_of_employees/members",
"per:date_of_birth",
"per:city_of_birth",
"per:charges",
"per:stateorprovince_of_death",
"per:religion",
"per:stateorprovince_of_birth",
"per:country_of_birth",
"org:dissolved",
"per:country_of_death"
]

rel_dict = { }

for rel in rel_list:
	dict_key = rel
	r = rel

	if "per:" in r:
		r = r.replace("per:", "person-")
	elif "org:" in r:
		r = r.replace("org:", "organization-")

	if "/" in r:
		r = r.replace("/", "_or_")
	if "stateorprovince" in r:
		r = r.replace("stateorprovince", "state_or_province")

	r = r.upper()

	rel_dict[rel] = r

	print(f'{rel:30} ==> {r:30}')


#print(rel_dict)

for rel in rel_dict:
	print(rel_dict[rel])

