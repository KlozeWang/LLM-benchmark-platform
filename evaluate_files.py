import os
from evaluation.metrics import evaluate_file

model_name = "GPT3"
pred_dir = "./outputs/llm/GPT3/prediction"
eval_dir = f"./result/{model_name}"
files = os.listdir(pred_dir)
for file in files:
    try:
        file_path = os.path.join(pred_dir, file)
        save_path = os.path.join(eval_dir, file.replace("predict", "evaluate"))
        evaluate_file(file_path, save_path)
    except Exception as e:
        print(f"{file} exception {e}")
        continue
