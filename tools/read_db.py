import pandas as pd
import numpy as np
import os
import json
try:
    from edit_config import config_read
except:
    from tools.edit_config import config_read
# file_name = 'test' 
# 获取当前工作目录
current_directory = os.getcwd()
# read ./settings/config.json

config = config_read()
db_name = config_read()['db_name']
db_type = config['db_type']

def read():
    db_name = config_read()['db_name']
    # db_type is a str
    if db_name.endswith('.json'):
        return read_json()
    else:
        return None

def write(data_content: pd.DataFrame, data_structure: pd.DataFrame):
    db_name = config_read()['db_name']
    if db_name.endswith('.csv'):
        write_csv(data_content, data_structure)
    else:
        return None
def read_json():
    db_name = config_read()['db_name']
    file_path = os.path.join(current_directory, 'db', db_name)
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    node_content = pd.DataFrame(data["node_content"])
    node_structure = pd.DataFrame(data["node_structure"])
    return node_content, node_structure

def write_json(node_content: pd.DataFrame, node_structure: dict):
    db_name = config_read()['db_name']
    file_path = os.path.join(current_directory, 'db', db_name)
    data = {
        "node_content": node_content.to_dict(orient='records'),
        "node_structure": node_structure.to_dict(orient='records')
    }
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# def write_json(df: pd.DataFrame):
#     db_name = config_read()['db_name']
#     file_path = os.path.join(current_directory, 'db', db_name)
#     # print(file_path)
#     data = df.to_dict(orient='records')
#     with open(file_path, 'w', encoding='utf-8') as f:
#         json.dump(data, f, ensure_ascii=False, indent=4)
               

if (__name__ == '__main__'):
    # print current directory
    # print(current_directory)
    a,b = read()
    row = a[a['id'] == 1]
    print(row['summary'].values[0])
    # write(df)
