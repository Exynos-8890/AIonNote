import pandas as pd
import numpy as np
import os
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
    if db_name.endswith('.csv'):
        return read_csv()
    elif db_name.endswith('.json'):
        return read_json()
    else:
        return None

def write(df: pd.DataFrame):
    db_name = config_read()['db_name']
    if db_name.endswith('.csv'):
        write_csv(df)
    elif db_name.endswith('.json'):
        write_json(df)
    else:
        return None


def read_csv():
    db_name = config_read()['db_name']
    file_path = os.path.join(current_directory, 'db', (db_name))
    df = pd.read_csv(file_path,index_col=0)
    df['reference'] = df['reference'].apply(eval)
    # turn df to dataframe
    df = pd.DataFrame(df)
    return df
def read_json():
    db_name = config_read()['db_name']
    file_path = os.path.join(current_directory, 'db', db_name)
    df = pd.read_json(file_path
                      , orient='records'
                    #   , lines=True
                      )
    return df

def write_csv(df: pd.DataFrame):
    db_name = config_read()['db_name']
    file_path = os.path.join(current_directory, 'db', db_name)
    df.to_csv(file_path, index=True, encoding='utf-8')

def write_json(df: pd.DataFrame):
    db_name = config_read()['db_name']
    file_path = os.path.join(current_directory, 'db', db_name)
    data = df.to_dict(orient='records')
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
               

if (__name__ == '__main__'):
    # print current directory
    # print(current_directory)
    df = read()
    
    # print(df.iloc[0]['reference'][0])
    new_row = pd.DataFrame({'summary': 'test', 'reference': [-1], 'prompt': 'test', 'content': 'test'})
    df = pd.concat([df, new_row], ignore_index=True)
    print(db_name)
    print(df)
    # write(df)
