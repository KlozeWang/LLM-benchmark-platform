import re
import math
import string
import functools
from rouge import Rouge
import numpy as np

from typing import List
from collections import Counter
from collections import defaultdict
#from SwissArmyTransformer import get_tokenizer
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

from .utils import print_rank_0

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

    return white_space_fix(remove_articles(remove_punc(lower(s))))

def bleu_score(predictions, ground_truths):
    bleu = []
    smoothing = SmoothingFunction()
    for prediction, ground_truth in zip(predictions, ground_truths):
        if not isinstance(prediction,str):
            print("Return error")
            continue
        prediction = normalize_answer(prediction).split()
        ground_truths = []
        for turth in ground_truth[0].get("targets"):
            ground_truths.append(normalize_answer(turth).split())
        bleu.append(sentence_bleu(ground_truths, prediction, smoothing_function=smoothing.method1))
    bleu_score = np.mean(bleu)
    return bleu_score

def rouge_score(predictions, ground_truths):
    rouge = Rouge()
    rouge_1_list = []
    rouge_2_list = []
    rouge_l_list = []
    for prediction, ground_truth in zip(predictions, ground_truths):
        if not isinstance(prediction,str):
            print("Return error")
            continue
        prediction = normalize_answer(prediction).split()
        ground_truths = []
        for turth in ground_truth[0].get("targets"):
            ground_truths.append(normalize_answer(turth).split())
        prediction = ' '.join(prediction)
        rouge_1 = 0
        rouge_2 = 0
        rouge_l = 0
        for turth in ground_truths:
            turth = " ".join(turth)
            rouge_1 = max(rouge_1, rouge.get_scores(turth, prediction)[0]['rouge-1']["f"])
            rouge_2 = max(rouge_2, rouge.get_scores(turth, prediction)[0]['rouge-2']["f"])
            rouge_l = max(rouge_l, rouge.get_scores(turth, prediction)[0]['rouge-l']["f"])
        
        rouge_1_list.append(rouge_1)
        rouge_2_list.append(rouge_2)
        rouge_l_list.append(rouge_l)

    rouge_1 = np.mean(rouge_1_list)
    rouge_2 = np.mean(rouge_2_list)
    rouge_l = np.mean(rouge_l_list)

    return {"ROUGE-1": rouge_1,"ROUGE-2": rouge_2,"ROUGE-L": rouge_l}

def calculate_perplexity(loss: List[float], data):
    return math.exp(min(20, np.sum(loss) / data[0]["num_original_tokens"]))


def special_for_dataset(predictions, examples):
    print_rank_0("Metrics not found, maybe dataset special metric or metric name error")
    return True


DEFAULT_METRICS = defaultdict(lambda: special_for_dataset)
DEFAULT_METRICS.update(
    {
        "BLEU": bleu_score,
        "ROUGE": rouge_score,
        "PPL": calculate_perplexity,
    }
)
