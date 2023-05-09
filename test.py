# '''
# code = "def check_answer(sentence):\n    words = sentence.split()\n    for word in words:\n        if len(word) >= 5 and word.lower() == word[::-1].lower():\n            return True\n    return False"

# def execute_code(code: str):
#     try:
#         exec(code, globals())
#     except Exception as e:
#         print(f"An error occurred while executing the code: {e}")



# execute_code(code)

<<<<<<< HEAD
print(globals()["check_answer"]("Before Eevee's racecar was admired, the cow saw the radar."))

import re
=======
# print(globals()["check_answer"]("Before Eevee's racecar was admired, the cow saw the radar."))
# '''
# import re
>>>>>>> d890d662cc8244cefec297e56cb2966fb020f097

# def create_prompt(template: str, values: dict) -> str:
#     # 使用正则表达式找到所有花括号内的名称
#     keys = re.findall(r"{(.*?)}", template)
    
#     print(keys)

#     # 根据在字典中找到的键值对替换花括号内的名称
#     for key in keys:
#         if key in values:
#             template = template.replace("{" + key + "}", str(values[key]))

#     return template

# # 示例用法
# text = "This is an example article."
# template = "Summary follow article: {text} \n TLDR:"

# # 使用字典传递参数名和对应的值
# values = {'text': text}

<<<<<<< HEAD
prompt = create_prompt(template, values)
print(prompt)
'''
import requests
import json

url = "http://45.41.95.10:10001/api/openai/chat-completion" #yuhao提供的接口
model = "gpt-3.5-turbo"


payload = json.dumps({
    "model": model,
    "messages": [
    {
        "role": "user",
        "content": "你好，请帮我写一份实验报告，内容是chatgpt使用的技术"
        }
    ]
    })
headers = {
    'Content-Type': 'application/json'
    }

response = requests.request("POST", url, headers=headers, data=payload)

print(json.loads(response.text).get("choices")[0].get("message").get("content"))
    
=======
# prompt = create_prompt(template, values)
# print(prompt)

import os
data_dir = "./tasks/llm/processed_data"
for file in os.listdir(data_dir):
    print(f"  {file[:-16]}: \"**/{file}\"")
>>>>>>> d890d662cc8244cefec297e56cb2966fb020f097
