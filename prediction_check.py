import json
import os
import jsonlines
import re
import string
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

file_name_eva = r"D:\Users\XuYifan\Documents\GitHub\LLM-benchmark\outputs\llm\ChatGLM\evaluation\\"
file_name_pre = r"D:\Users\XuYifan\Documents\GitHub\LLM-benchmark\outputs\llm\ChatGLM\prediction\\"
check_file = r"D:\Users\XuYifan\Documents\GitHub\LLM-benchmark\outputs\llm\ChatGLM\check\\"

files_eva = os.listdir(file_name_eva)
files_pre = os.listdir(file_name_pre)
def normalize_answer(s):
    """Lower text and remove punctuation, articles and extra whitespace."""

    def remove_articles(text):
        return re.sub(r"\b(a|an|the)\b", " ", text)

    def white_space_fix(text):
        return " ".join(text.split())

    def remove_punc(text):
        exclude = set(string.punctuation)
        return "".join(ch for ch in text if ch not in exclude)

    def lower(text):
        return text.lower()

    if len(s) < 3:
        return white_space_fix(remove_punc(lower(s)))
    return white_space_fix(remove_articles(remove_punc(lower(s))))

def word_bleu_score(reference, candidate):
    reference_tokens = list(reference)
    candidate_tokens = list(candidate)

    smoothie = SmoothingFunction().method4
    score = sentence_bleu([reference_tokens], candidate_tokens, smoothing_function=smoothie)
    return score

def acc_for_multi(predictions, ground_truths):
    acc = 0
    tt = len(predictions)
    if tt == 0:
        return 0
    smoothing = SmoothingFunction()
    idx = 0
    for prediction, ground_truth in zip(predictions, ground_truths):
        idx = idx + 1
        if not isinstance(prediction, str):
            print("Return error")
            continue
        is_correct = False
        if ground_truth[0].get("choices") == None:
            print("Acc only be valid in multi choices and NLI tasks currently.In this task, acc will be set 0.")
            return 0
        prediction = normalize_answer(prediction)
        for exact_answer in ground_truth[0]['targets']:
            if prediction == normalize_answer(exact_answer) or prediction in normalize_answer(exact_answer):
                acc = acc + 1
                is_correct = True
                break
        if is_correct:
            continue
        choices_bleu = []
        # 选择题经常是短选项，因此使用字母计算bleu。后续可考虑改成glm token F1 score
        for choice in ground_truth[0].get("choices"):
            choice = normalize_answer(choice)
            choices_bleu.append(word_bleu_score(choice, prediction))

        correct_index = ground_truth[0]['choices'].index(ground_truth[0]['targets'][0])
        if choices_bleu.index(max(choices_bleu)) == correct_index:
            acc = acc + 1

    return acc / tt
for eva,pre in zip(files_eva,files_pre):
    with jsonlines.open(file_name_pre + pre) as f,open(file_name_eva + eva) as f1,open(check_file + eva,'a') as f2:

        content = f1.read()
        eva = json.loads(content)
        predictions = []
        ground_truths = []

        for line in f:
            if line.get("prediction") == None:
                continue
            predictions.append(line["prediction"])
            ground_truths.append([line])
        acc = acc_for_multi(predictions, ground_truths)
        print(pre, acc)
        eva["ACC"] = acc
        f2.write(json.dumps(eva))

