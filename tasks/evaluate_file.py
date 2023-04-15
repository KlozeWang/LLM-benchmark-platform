import json
import os
import jsonlines
import pandas as pd

file_name_eva = r"D:\Users\XuYifan\Documents\GitHub\LLM-benchmark\outputs\llm\GPT3\\"
df = pd.DataFrame()
files_eva = os.listdir(file_name_eva)
for eva in files_eva:
    if "evaluate" not in eva:
        continue
    with open(file_name_eva + eva) as f1:
        content = f1.read()
        result = json.loads(content)
        model_name = eva.split('.')[0]
        dataset_name = eva.split('.')[1]
        result["model"] = model_name
        result["dataset"] = dataset_name
        df = df.append(result,ignore_index=True)
file_name_eva = r"D:\Users\XuYifan\Documents\GitHub\LLM-benchmark\outputs\llm\ChatGPT\\"

files_eva = os.listdir(file_name_eva)
for eva in files_eva:
    if "evaluate" not in eva:
        continue
    with open(file_name_eva + eva) as f1:
        content = f1.read()
        result = json.loads(content)
        model_name = eva.split('.')[0]
        dataset_name = eva.split('.')[1]
        result["model"] = model_name
        result["dataset"] = dataset_name
        df = df.append(result,ignore_index=True)
file_name_eva = r"D:\Users\XuYifan\Documents\GitHub\LLM-benchmark\outputs\llm\ChatGLM\check\\"

files_eva = os.listdir(file_name_eva)
for eva in files_eva:
    with open(file_name_eva + eva) as f1:
        content = f1.read()
        result = json.loads(content)
        model_name = eva.split('.')[0]
        dataset_name = eva.split('.')[1]
        result["model"] = model_name
        result["dataset"] = dataset_name
        df = df.append(result,ignore_index=True)


df.to_excel("all.xlsx")


