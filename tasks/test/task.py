import re
import string
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from typing import *

import numpy as np


from evaluation import (
    GenerationTask,
)

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

class ExampleTask(GenerationTask):
    @property
    def metrics(self) -> Dict[str, Callable]:
        return {"BLEU-metric": self.bleu_score}

    def bleu_score(predictions, ground_truths):
        bleu = []
        smoothing = SmoothingFunction()
        for prediction, ground_truth in zip(predictions, ground_truths):
            prediction = normalize_answer(prediction).split()
            ground_truths = []
            for turth in ground_truth[0]["targets"]:
                ground_truths.append(normalize_answer(turth).split())
            bleu.append(sentence_bleu(ground_truths, prediction, smoothing_function=smoothing.method1))
        bleu_score = np.mean(bleu)
        # 返回值可以是一个数，则该metric名称选用def metrics(self)中指定的名称
        # 也可以是一个字典，{key:float}形式返回多个子metrics
        return bleu_score

    