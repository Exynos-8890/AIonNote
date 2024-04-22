from read_db import read, write
from openai import OpenAI
import myapi

ID = 5

df = read()

prompt_with_content = df['prompt'][ID]
for id in df['reference'][ID]:
    if id == -1:
        continue
    if df['content'][id] == '':
        # stop the program and report error 
        print('Error: content is empty')
        exit(0)
    prompt_with_content = prompt_with_content + '\n' * 2  + df['summary'][id] + ': ' + df['content'][id]
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

df.loc[ID, "content"] = completion.choices[0].message.content
print(df["content"][ID])
write(df)