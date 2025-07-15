"""Created on 14-Jul-2025
    This script generates sample code prediction prompt that implements meta-prompt framework proposed in https://doi.org/10.21203/rs.3.rs-5750190/v1
"""
import sys
import json
import yaml
import codecs
import numpy as np
import pandas as pd
from prompt_framework import prompts

def drg_system_knowledge(drg_knowledge='drg_34_dissection.csv', top30drg_code='DRG30.csv'):
    df = pd.read_csv(drg_knowledge)
    df["cc/mcc_label"] = [int(c) for c in df["CC/MCC"].tolist()] 
    df["basedrg_label"] = [int(c) for c in df["principal_diagnosis_lable"].tolist()] 
    df["drg_code"] = [int(c) for c in df["DRG"].tolist()]

    df = df[["Description", "principal_diagnosis", "drg_code", "basedrg_label", "cc/mcc_label"]]

    df2 = pd.read_csv(top30drg_code)
    topk_drgcode = df2["drg_code"].tolist() 
    df = df[df["drg_code"].isin(topk_drgcode)]

    return df

def construct_drg_prompt(guidelines_file, sample_file, topk=1):
    system_message = prompts['drg']['system_message']
    user_message = prompts['drg']['user_message']

    # system message
    guidelines={}
    with open(guidelines_file, "r") as f:
        for guide in json.load(f):
            guidelines[int(guide["drg_code"])] = guide["description"]

    df_knowledge = drg_system_knowledge()
    taxonomy = {}
    drgcodes_procedure = [int(df_knowledge.iloc[i]["drg_code"]) for i in range(len(df_knowledge)) if df_knowledge.iloc[i]["cc/mcc_label"]==4 ]
    drgcodes_diagnoses = [int(df_knowledge.iloc[i]["drg_code"]) for i in range(len(df_knowledge)) if df_knowledge.iloc[i]["cc/mcc_label"]!=4 ]
    taxonomy["procedures"] = [{"drg_code": c, "description": guidelines[c]} for c in drgcodes_procedure ]
    taxonomy["primary diagnoses"] = [{"drg_code": c, "description": guidelines[c]} for c in drgcodes_diagnoses]      

    system_message = system_message.replace("<<TAXONOMY>>", yaml.dump(taxonomy, indent=4)).replace("<<TOPK>>", str(topk))
    print(system_message)

    # user massage
    sample_file = sample_file.replace('.json', '.csv')
    df_samples = pd.read_csv(sample_file)
    sample_no = df_samples['sample_no'].unique()
    np.random.shuffle(sample_no)
    sample_no = sample_no[0]
    
    similar_examples = df_samples[(df_samples['sample_no']==sample_no) & (df_samples['sample_type']=='N_shot')][['discharge_summary','drg_code']]
    similar_examples = similar_examples.to_dict(orient='records')
    similar_examples_yaml = yaml.dump(similar_examples, sort_keys=False)
    user_message = user_message.replace("<<EXAMPLES>>", similar_examples_yaml).replace("<<TOPK>>", str(topk))

    test_input = df_samples[(df_samples['sample_no']==sample_no) & (df_samples['sample_type']=='test')]['discharge_summary'].tolist()
    user_message = user_message + yaml.dump([{"discharge_summary": text} for text in test_input], indent=4)
    
    return system_message,user_message


def construct_ctc_prompt(guidelines_file, sample_file):
    system_message = prompts['ctc']['system_message']
    user_message = prompts['ctc']['user_message']

    with open(guidelines_file, "r") as f:
        content = json.load(f)
        taxonomy = content["taxonomy"]
        guide_str = content["context"]

    taxonomy_str = ""
    for label, description in taxonomy.items():
        description = description[-1] if type(description) is list else description
        taxonomy_str += f'-   "label": "{label}"\n' 
        taxonomy_str += f'    "label_description" : "{description}"\n\n' 

    with codecs.open(sample_file, "r", encoding="utf-8") as f: samples = json.load(f)
    idx = np.arange(len(samples))
    np.random.shuffle(idx)
    input_text = samples[idx[0]]['text']
    similar_examples = samples[idx[0]]['N_shots']

    user_message = user_message.replace("<<TAXONOMY>>", taxonomy_str)
    user_message = user_message.replace("<<GUIDE>>", guide_str)
    user_message = user_message.replace("<<EXAMPLES>>", yaml.dump(similar_examples, indent=4, allow_unicode=True))
    user_message += yaml.dump(input_text, indent=4, allow_unicode=True)    

    return system_message,user_message

def construct_sts_prompt(guidelines_file, sample_file):
    system_message = prompts['sts']['system_message']
    user_message = prompts['sts']['user_message']

    with codecs.open(sample_file, "r", encoding="utf-8") as f: samples = json.load(f)
    idx = np.arange(len(samples))
    np.random.shuffle(idx)
    similar_examples = samples[idx[0]]['N_shots']
    del samples[idx[0]]['N_shots']
    input_text = samples[idx[0]]

    with open(guidelines_file, "r") as f: guidelines = json.load(f)
    user_message = user_message.replace("<<GUIDE>>", yaml.dump(guidelines, indent=4))

    user_message = user_message.replace("<<EXAMPLES>>", yaml.dump(similar_examples, indent=4, allow_unicode=True))
    user_message += yaml.dump(input_text, indent=4, allow_unicode=True) 

    return system_message,user_message


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_sample_prompt.py <task_no>\n\ttask_no be 1, 2 or 3")
        sys.exit(1)

    task_no = sys.argv[1].strip()
    if task_no not in ["1", "2", "3"]:
        print("Valid task_no are 1, 2 or 3.")
        sys.exit(1)

    tasks = {"1":"sts", "2":"ctc", "3":"drg"}
    sample_file = f'{tasks[task_no]}_samples.json'
    guidelines_file = f'{tasks[task_no]}_guidelines.json'

    if tasks[task_no]=='drg': system_message,user_message = construct_drg_prompt(guidelines_file, sample_file)
    elif tasks[task_no]=='ctc': system_message,user_message = construct_ctc_prompt(guidelines_file, sample_file)
    elif tasks[task_no]=='sts': system_message,user_message = construct_sts_prompt(guidelines_file, sample_file)

    gpt_message = [   
                {"role":"system", "content": system_message},
                {"role":"user", "content": user_message},  
            ]
    print("==GPT prompt ==\n")
    print(yaml.dump(gpt_message, allow_unicode=True))

main()