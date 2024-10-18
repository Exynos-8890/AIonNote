import numpy as np
try:
    from read_db import read
except:
    from tools.read_db import read

width = 8

def db2mermaid_code():
    node_content, node_structure = read()
    flow_definition = f'''graph LR;
classDef red stroke:#f00,stroke-width:{width}px
classDef green stroke:#0f0,stroke-width:{width}px
classDef blue stroke:#00f,stroke-width:{width}px
'''
    for _, row in node_content.iterrows():
        flow_definition += f"{row['id']}[{row['summary']}]\n"
        if row.isnull().any():
            flow_definition += f"{row['id']}:::red\n"
        else:
            flow_definition += f"{row['id']}:::green\n"
    
    for _, row in node_structure.iterrows():
        print(row)
        # if row['reference'] == -1:
        #     continue
        flow_definition += f"{row['reference']} --> {row['id']}\n"

    return flow_definition
    # for index, row in df.iterrows():
    #     # print(row)
    #     flow_definition += f"{index}[{row['summary']}]\n"
    #     if row.isnull().any() :
    #         flow_definition += f"{index}:::red\n" 
    #     else:
    #         flow_definition += f"{index}:::green\n"
    # for index, row in df.iterrows():
    #     if row['reference'] == -1:
    #         continue
    #     for i in row['reference']:
    #         if i == -1:
    #             break
    #         flow_definition += f"{i} --> {index}\n"
    # return flow_definition

if __name__ == '__main__':
    print(db2mermaid_code())

