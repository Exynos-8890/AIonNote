# from read_db import read, write
try:
    from read_db import read, write
except:
    from tools.read_db import read, write

try:
    from myapi import get_zhipu_response, get_kimi_response
except:
    from tools.myapi import get_zhipu_response, get_kimi_response

def run_index(running_ID):
    df = read()

    prompt_with_content = df['prompt'][running_ID]
    if df['reference'][running_ID] == [-1]:
        pass
    else:
        for index in df['reference'][running_ID]:
            if df['content'][index] == '':
                # stop the program and report error 
                print('Error: content is empty')
                exit(0)
            prompt_with_content = prompt_with_content + '\n' * 2  + df['summary'][index] + ': ' + df['content'][index]
    # print(prompt_with_content)
    

    df.loc[running_ID, "content"] = get_zhipu_response(prompt_with_content)
    # get_kimi_response(prompt_with_content)
    print(df["content"][running_ID])
    write(df)

if __name__ == '__main__':  
    run_index(5)