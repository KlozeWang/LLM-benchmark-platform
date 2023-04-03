import os
import re
import math
import json
import random

import numpy as np
import torch

from typing import List, Union
from abc import ABC, abstractmethod

from .configs import BaseConfig, GenerationTaskConfig


class EvaluationDataset(torch.utils.data.Dataset, ABC):
    """
    Jsonlines of {
        "text": context
        "choices": [choice_id1,...], if not None, len(target) == 1
        "label": If generation task -1, else [0, len(choices))
    }
    If [MASK] not in context, will append [MASK] after text
    """

    def __init__(self, path: Union[str, List[str]], model, config: BaseConfig):
        self.path = path if isinstance(path, list) else [path]
        self.model = model
        self.config = config

        self.data = []
        for p in self.path:
            self.process_single_file(p)

    @property
    def has_collate_fn(self) -> bool:
        return False

    def collate_fn(self, samples):
        return None
    
    def few_shot(self, shots):
        assert shots < self.__len__(), "number of shots should lower than size of your dataset"
        tmp_data = []
        for data in self.data:
            examples = random.sample(self.data, self.config.shot)
            prompt = data[0]["text"]
            for example in examples:
                prompt = example[0]["text"] + "\n" + example[0]["targets"][0] + prompt
                prompt = self.cut_exceed_length(prompt)
            tmp_data.append(data)
        self.data = tmp_data
            
    def process_single_file(self, path):
        with open(os.path.join(path), "r", encoding="utf-8") as file:
            for line in file:
                item = json.loads(line)
                self.data.append(self.process_single_item(item))
            
            if self.config.shot > 0:
                self.few_shot(self.config.shot)
                
    @abstractmethod
    def process_single_item(self, item, **kwargs) -> List[dict]:
        pass
    
    def cut_exceed_length(self, text):
        if self.config.language == "en":
            if len(text.split(" ")) > self.config.max_length:
                length = len(text.split(" "))
                text = " ".join(text.split(" ")[length - self.config.max_length: ])
        elif self.config.language == "cn":
            if len(text) > self.config.max_length:
                text = text[len(text) - self.config.max_length: ]
        return text

    def __len__(self):
        return len(self.data)


class GenerationTaskDataset(EvaluationDataset):
    config: GenerationTaskConfig
    def create_prompt(self, template: str, values: dict) -> str:
        keys = re.findall(r"{(.*?)}", template)
        for key in keys:
            if key in values:
                template = template.replace("{" + key + "}", str(values[key]))
        return template

    def process_single_item(self, item, **kwargs):
        input = item.get("input")
        targets = item.get("targets")
        if self.config.prompt is not None:
            input = self.create_prompt(self.config.prompt, item)
        input = self.cut_exceed_length(input)
        return [{"text": input, "targets": targets, **kwargs}]

    @property
    def has_collate_fn(self) -> bool:
        return False

    def __getitem__(self, idx):
        item = self.data[idx]
        return item

'''
class LanguageModelTaskDataset(EvaluationDataset):
    config: LanguageModelTaskConfig
    left_weights: List[int]
    weights: List[int]

    def process_single_file(self, path):
        num_sequences = []
        with open(os.path.join(path), "r", encoding="utf-8") as file:
            raw_text = file.read()
            tokens = self.tokenizer.tokenize(raw_text)
            self.data.append(
                {
                    "raw_text": tokens,
                    "num_original_tokens": len(raw_text.strip().split(" ")),
                    "num_sequences": max(
                        math.ceil(
                            max(len(tokens) - (self.config.max_seq_length - 1), 0) / self.config.generation_length
                        )
                        + 1,
                        1,
                    ),
                }
            )
            num_sequences.append(self.data[-1]["num_sequences"])
        self.weights = list(accumulate(num_sequences))
        self.left_weights = [0] + self.weights[:-1]

    def process_single_item(self, item):
        pass

    def __len__(self):
        return self.data[0]["num_sequences"]

    def __getitem__(self, idx):
        document_idx = bisect_right(self.weights, idx)
        idx = idx - self.left_weights[document_idx]
        start_idx = idx * self.config.generation_length
        end_idx = start_idx + self.config.max_seq_length - 1  # for additional [gMASK]
        tokens = self.data[document_idx]["raw_text"][start_idx:end_idx]

        return self.model.build_language_model_sample(
            tokens,
            is_first_segment=idx == 0,
            max_seq_length=self.config.max_seq_length,
            generation_length=self.config.generation_length,
            unidirectional=self.config.unidirectional,
            use_gmask=self.config.use_task_mask,
        )
'''