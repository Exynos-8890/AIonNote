from openai import OpenAI

# print openai version
# print(OpenAI.__version__)
client = OpenAI(
    api_key="sk-Gd0K8mOqI9PCW9rHjR99nDxsBMPFp5gzk0QHM5EK5ial6Yy1",
    base_url="https://api.moonshot.cn/v1",
)

completion = client.chat.completions.create(
  model="moonshot-v1-8k",
  messages=[
    # {"role": "system", "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"},
    {"role": "user", "content": "你好，我叫李雷，114*514等于多少？"}
  ],
  temperature=0.3,
)
 
print(completion.choices[0].message)