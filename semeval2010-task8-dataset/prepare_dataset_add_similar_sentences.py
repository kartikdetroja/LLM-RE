import os
import sys
import re
import json
import shutil

#######################################################################################
def get_examples(ds_file):
    # open the JSON file
    with open(ds_file) as f: 
        # read all json objects as example dictionaries and store in the example list
        examples_list = json.load(f)

        # Close the file
        f.close()

    # return list of examples: each example is dictionary
    return examples_list

def main():
    # get dataset file
    test_dataset_file = "dataset/test.json"
    similar_sentence_list_file = "dataset/similar_sentence_list.json"

    # get examples from json file
    list_test_examples = get_examples(test_dataset_file)
    list_similar_sentence = get_examples(similar_sentence_list_file)
        
    for index, example in enumerate(list_test_examples):
        id = str(int(example['id']) - 8000)
        
        example['similar_sentences'] = list_similar_sentence[id]


    # Save output dictionary list in a file.
    with open(test_dataset_file, 'w') as fp:
        json.dump(list_test_examples, fp)
        fp.close()

        
if __name__=="__main__":
    main() 