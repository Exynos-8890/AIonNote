import json,os
current_directory = os.getcwd()
def config_read() -> dict: 
    with open(os.path.join(current_directory, 'settings', 'config.json'), 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config

def config_enable_csv():
    with open(os.path.join(current_directory, 'settings', 'config.json'), 'r+', encoding='utf-8') as f:
        config = json.load(f)
        config['db_type'] = "csv"
        f.seek(0)
        json.dump(config, f, ensure_ascii=False, indent=4)

def config_enable_json():
    with open(os.path.join(current_directory, 'settings', 'config.json'), 'r+', encoding='utf-8') as f:
        config = json.load(f)
        config['db_type'] = "json"
        f.seek(0)
        json.dump(config, f, ensure_ascii=False, indent=4)

def config_update_db_name(db_name:str):
    with open(os.path.join(current_directory, 'settings', 'config.json'), 'r+') as f:
        config = json.load(f)
        config['db_name'] = db_name
        f.seek(0)
        f.truncate(0)
        json.dump(config, f, ensure_ascii=False, indent=4)

if (__name__ == '__main__'):
    config_enable_json()
    print(config_read())
