# QUESTION NO:62

import json
import yaml 

def clean_and_normalize_data(raw_content, is_yaml=False):
    
    try:
        if is_yaml:
            data = yaml.safe_load(raw_content)
        else:
            data = json.loads(raw_content)
            
    except Exception as e:
        return f"ERROR: Failed to parse (give the yaml or json)format ({e})"

    items_to_process = data if isinstance(data, list) else [data]
    cleaned_output = []

    for item in items_to_process:
        
        normalized_item = {
            key.lower(): value
            for key, value in item.items()
        }
        
        status_value = normalized_item.get('status')
        if status_value and isinstance(status_value, str):
            normalized_item['status'] = status_value.upper().strip() 
            
        if 'region' not in normalized_item:
            normalized_item['region'] = 'US_DEFAULT'
            
        cleaned_output.append(normalized_item)

    tidy_json_string = json.dumps(cleaned_output, indent=4)
    
    return tidy_json_string

MESSY_JSON_INPUT = """
[
    {"Item_ID": 1, "NAME": "Monitor", "stAtus": "active"}, 
    {"item_id": 2, "Name": "Keyboard", "STATUS": "PENDING "},
    {"item_id": 3, "Description": "Missing Status and Region"}
]
"""

CLEANED_RESULT = clean_and_normalize_data(MESSY_JSON_INPUT, is_yaml=False)

print("-- Cleaned and Normalized Output --")
print(CLEANED_RESULT)
