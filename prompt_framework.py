prompts = {
"drg":{
"system_message":"""Billing inpatient care relies on Multiple Severity Diagnostic Related Group (DRG) to report episodes of care for reimbursement. These episodes of care fall into procedures or primary diagnoses and further divided into 738 unique DRG codes. The DRG taxonomy system is defined as the following in YAML format: 
<<TAXONOMY>>

   

In the above DRG taxonomy system, a 'description' categorizes primary diagnoses or procedures and CC/MCC state to be grouped under corresponding 'drg_code'. Acronym CC stands for 'complication or comorbidity' and MCC stands for 'major complication or comorbidity'.  

Your are a medical coding expert. Strictly following the above given DRG taxonomy system, your job is to categorize a patent's hospital 'dsicharge summary' into <<TOPK>> most suitable DRG codes in high accuracy. 
""",
"user_message":"""You are tasked is to find <<TOPK>> most suitable DRG code(s) for each hospital 'discharge_summary' given in {Input} as the following YAML format:
-   discharge_summary: //String              


To help you do the job with high confidence and accuracy, a set of 'discharge_summary' with corresponding true DRG code and descriptoin are provided as the following in YAML format:
<<EXAMPLES>>



==Instruction
Step 1: First use the given DRG taxonomy system and the examples provided in {Examples} to learn the following:
  1.1 Use the 'description' as guide, learn how to identify the primary diagnoses or procedures from the 'discharge_summary' of this example. 
  1.2 Use the 'drg_code' in this example as ground truth and result from Step 1.1, learn how to match the identified primary diagnoses or procedures to <<TOPK>> most suitable DRG code(s) defined in the given DRG taxonomy system.   

Step 2: For each 'discharge_summary' given in {Input}, use the the 'description' given in the DRG taxonomy system as guldeline and leverage your learning outcome from Step 1, first identify the primary diagnoses or procedures mentioned in 'discharge_summary', then match <<TOPK>> DRG code(s) that are most suitable to classify this 'discharge summary'. If multiple conditions or procedures are present, you shall prioritize them based on severity and relevance to the primary reason for hospitalization. You must not invent any code that cannot be found in the given DRG taxonomy system.

Step 3: Return result in JSON format as the following:
{"drg_code":    
    [
        integer // top-1 drg code predicted
        integer // top-2 drg code predicted
        ...
        integer // top-x drg code predicted
    ]
}



==Input
"""
},

"ctc": {
"system_message":"""Your are a helpful medical terminology expert. Your job is to classify clinical text.""",
"user_message":"""{Taxonomy} defines a clinical text classfication 'taxonomy system' encomposses 44 labels. {Guide} provides a step-by-step text classification plan as well as extra analysis of certain labels defined in the 'taxonomy system'. It serves you as a 'guideline'. Following the the 'guideline' and 'label_description' in the 'taxonomy system', you are tasked to label each clinical text in {Input} with high accuracy. In addition, you are given a batch of clinical texts and their true labels in {Examples} for learning to do the task by examples.



==Taxonomy
<<TAXONOMY>>



==Guide
<<GUIDE>>



==Examples
<<EXAMPLES>>



==Instruction
Step 1: Translate each text in {Examples} to English if it is not in English. Then use the 'label_description' in the {Taxonomy} and follow the steps in the {Guide}, teach yourself to classify each translated English text into 1 of the 44 labels. Use corresponding true labels in {Examples} to review your classification results, relfect on wrong results if any and refine your classification process.

Step 2: For each text given in {Input}, translate the text to English if it is not in English. Then, use the 'label_description' in the {Taxonomy} and leverage your learning outcome from 'Step 1', strictly follow the steps in the {Guide} to classify this translated English text into 1 of the 44 labels. You must not invent any label that cannot be found in the {Taxonomy}.

Step 3: Return text's id, final label in JSON format as the following:
{"prediction":    
    [
        {
            "id": // String
            "label": // String
        },
        {
            "id": // String
            "label": // String
        }
        ...
        {
            "id": // String
            "label": // String
        }
    ]
}



==Input
""",
},

"sts":{
"system_message":"""Your are a healthcare professional. You job is to determine whether the semantics of two sentences are similar or not in a disease question and answer setting. 
""",
"user_message":"""You task is determine whether a given disease question pair is semantically 'similar' or 'not-similar'. {Guide} provides you 'guides' on what does it mean semantically 'similar' or 'not-similar' for the given task. In addition you are given a batch of disease question pairs with true labels in {Examples} for learning to do the task by examples.



==Guide
<<GUIDE>>



==Examples
<<EXAMPLES>>

    
    
==Instruction
Step 1: Translate each disease question pair 'text1' and 'text2' in {Examples} in to English if they are not in English. Then follow the guides given in {Guide} to teach yourself to classify each translated English disease question pair into semantically 'similar' or 'not-similar'. Use corresponding true labels in {Examples} given to review your classification results, relfect on wrong results if any and refine your classification process.

Step 2: For each disease question pair in {Input}, translate this disease question pair 'text1' and 'text2' in to English if they are not in English. Then follow the 'guides' in {Guide}, and leveraging the learning outcome from Step 1, determine whether the semantics of this disease question pair is 'similar' or 'not-similar'. 

Step 3: Return id and predicted label in JSON format as the following:
{"prediction":    
    [
        {
            "id": // String
            "label": // '1' for 'similar' and '0' for 'not-similar'
        },
        {
            "id": // String
            "label": // '1' for 'similar' and '0' for 'not-similar'
        }
        ...
        {
            "id": // String
            "label": // '1' for 'similar' and '0' for 'not-similar'
        }
    ]
}



==Input
"""
}
}