import pandas as pd
import numpy as np
import os
import json
file_name = 'test' 
# 获取当前工作目录
current_directory = os.getcwd()
# read ./settings/config.json

with open(os.path.join(current_directory, 'settings', 'config.json'), 'r', encoding='utf-8') as f:
    config = json.load(f)
db_name = config['db_name']
db_type = config['db_type']

def read():
    if db_type == 'csv':
        return read_csv()
    elif db_type == 'json':
        return read_json()
    else:
        return None

def write(df: pd.DataFrame):
    if db_type == 'csv':
        write_csv(df)
    elif db_type == 'json':
        write_json(df)
    else:
        return None


def read_csv():
    file_path = os.path.join(current_directory, 'db', (file_name + '.csv'))
    df = pd.read_csv(file_path,index_col=0)
    df['reference'] = df['reference'].apply(eval)
    # turn df to dataframe
    df = pd.DataFrame(df)
    return df
def read_json():
    file_path = os.path.join(current_directory, 'db', file_name + '.json')
    df = pd.read_json(file_path
                      , orient='records'
                    #   , lines=True
                      )
    return df

def write_csv(df: pd.DataFrame):
    file_path = os.path.join(current_directory, 'db', file_name+'.csv')
    df.to_csv(file_path, index=True, encoding='utf-8')

def write_json(df: pd.DataFrame):
    file_path = os.path.join(current_directory, 'db', file_name+'.json')
    data = df.to_dict(orient='records')
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
               

if (__name__ == '__main__'):
    # print current directory
    # print(current_directory)
    df = read()
    
    print(df.iloc[0]['reference'][0])
    new_row = pd.DataFrame({'summary': 'test', 'reference': [-1], 'prompt': 'test', 'content': 'test'})
    df = pd.concat([df, new_row], ignore_index=True)
    print(df.iloc[-1])
    # write(df)
