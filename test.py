'''
code = "def check_answer(sentence):\n    words = sentence.split()\n    for word in words:\n        if len(word) >= 5 and word.lower() == word[::-1].lower():\n            return True\n    return False"

def execute_code(code: str):
    try:
        exec(code, globals())
    except Exception as e:
        print(f"An error occurred while executing the code: {e}")



execute_code(code)

print(globals()["check_answer"]("Before Eevee's racecar was admired, the cow saw the radar."))

import re

def create_prompt(template: str, values: dict) -> str:
    # 使用正则表达式找到所有花括号内的名称
    keys = re.findall(r"{(.*?)}", template)
    
    print(keys)

    # 根据在字典中找到的键值对替换花括号内的名称
    for key in keys:
        if key in values:
            template = template.replace("{" + key + "}", str(values[key]))

    return template

# 示例用法
text = "This is an example article."
template = "Summary follow article: {text} \n TLDR:"

# 使用字典传递参数名和对应的值
values = {'text': text}

prompt = create_prompt(template, values)
print(prompt)
'''
import requests
import json
url = "http://10.50.212.248:8001/conversation/stream"

payload = json.dumps({
            "prompt": "你好",
            "seed": 1,
            "history": []
        })
headers = {
  'Authorization': '85577713-4c52-48bd-bf65-57112ce337d2',
  'Content-Type': 'application/json; charset=utf-8'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)