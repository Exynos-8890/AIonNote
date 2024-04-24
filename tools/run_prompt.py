from read_db import read, write
from openai import OpenAI
import myapi

def run_index(running_ID):
    df = read()

    prompt_with_content = df['prompt'][running_ID]
    for index in df['reference'][running_ID]:
        if index == -1:
            continue
        if df['content'][index] == '':
            # stop the program and report error 
            print('Error: content is empty')
            exit(0)
        prompt_with_content = prompt_with_content + '\n' * 2  + df['summary'][index] + ': ' + df['content'][index]
    print(prompt_with_content)
    client = OpenAI(
        api_key= myapi.myapikey,
        base_url="https://api.moonshot.cn/v1",
    )
    completion = client.chat.completions.create(
    model="moonshot-v1-8k",
    messages=[
        {"role": "user", "content": prompt_with_content}
    ],
    temperature=0.3,
    )

    df.loc[running_ID, "content"] = completion.choices[0].message.content
    print(df["content"][running_ID])
    # write(df)

if __name__ == '__main__':  
    run_index(5)