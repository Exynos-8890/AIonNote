# myapikey="sk-Gd0K8mOqI9PCW9rHjR99nDxsBMPFp5gzk0QHM5EK5ial6Yy1"
kimikey = "sk-Onio9mkTwP9YWBwk0yfoDeed1gRSlwzV0PnzBTJAPivWqSVq"
zhipukey = "ea8ad5cea35fd28aaeff160416ca5b10.CnX9MoBwFXijanfC"
from openai import OpenAI
from zhipuai import ZhipuAI
import requests
def get_zhipu_response(prompt_with_content="你好"):
    client = ZhipuAI(api_key=zhipukey) # 填写您自己的APIKey
    response = client.chat.completions.create(
        model="glm-4",  # 填写需要调用的模型名称
        messages=[
            {"role": "user", "content": prompt_with_content}
        ],
    )
    return response.choices[0].message.content


def get_kimi_response(prompt_with_content="你好"):
    client = OpenAI(
        api_key= kimikey,
        base_url="https://api.moonshot.cn/v1",
    )
    try:
        completion = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=[
            {"role": "user", "content": prompt_with_content}
        ],
        temperature=0.3,
        )
    except Exception as e:
        print('访问限制，1分钟后重试',e)
        exit(0)
    return completion.choices[0].message.content

def get_kimi_balance():
    url = "https://api.moonshot.cn/v1/users/me/balance"
    headers = {"Authorization": kimikey}
    response = requests.get(url, headers=headers)
    # print(response.json())
    balance = response.json()['data']['available_balance']
    return balance

if __name__ == '__main__':
    print(get_kimi_balance())

