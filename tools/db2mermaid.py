import numpy as np
# if __name__ == '__main__':
#     from read_db import read
# else:
#     from tools.read_db import read
try:
    from read_db import read
except:
    from tools.read_db import read

width = 8

def db2mermaid_code():
    df = read()
    # print(df)
    flow_definition = f'''graph LR;
classDef red stroke:#f00,stroke-width:{width}px
classDef green stroke:#0f0,stroke-width:{width}px
classDef blue stroke:#00f,stroke-width:{width}px
'''
    for index, row in df.iterrows():
        # print(row)
        flow_definition += f"{index}[{row['summary']}]\n"
        if row.isnull().any() :
            flow_definition += f"{index}:::red\n" 
        else:
            flow_definition += f"{index}:::green\n"
    for index, row in df.iterrows():
        for i in row['reference']:
            if i == -1:
                break
            flow_definition += f"{i} --> {index}\n"
    return flow_definition

if __name__ == '__main__':
    print(db2mermaid_code())

