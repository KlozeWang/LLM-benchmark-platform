from random import choices
import random
import jsonlines
import os

def load_data(path):
    docs = []
    with jsonlines.open(path, "r") as reader:
        for doc in reader:
            docs.append(doc)
    print(f"{len(docs)} loaded")
    return docs

def transfer_ai2_arc(doc, i=0):
    labels = doc["choices"]["label"]
    if not doc["answerKey"]:
        return {}
    answer_index = labels.index(doc["answerKey"])
    new_doc = {
        "id": doc["id"],
        "label": "MUL",
        "question": doc["question"],
        "choices": doc["choices"]["text"],
        "answer": doc["choices"]["text"][answer_index]
    }
    return new_doc

def transfer_anli(doc, i=0):
    nli_map = {
        0: "entailment",
        1: "neutral",
        2: "contradiction"
    }
    premise = doc["premise"]
    hypothesis = doc["hypothesis"]
    label = doc["label"]
    new_doc = {
        "id": doc["uid"],
        "label": "NLI",
        "question": f"Tell me the logical relationship of two following sentences\n1. {premise}\n2. {hypothesis} ",
        "answer": nli_map[label],
        "choices": [ "entailment", "neutral", "contradiction" ],
    }
    return new_doc

def transfer_billsum(doc, i=0):
    new_doc = {
        "id": i,
        "label": "SUM",
        "question": doc["text"],
        "answer": doc["summary"]
    }
    return new_doc

def transfer_cnn_daily(doc, i):
    new_doc = {
        "id": doc["id"],
        "label": "SUM",
        "question": doc["article"],
        "answer": doc["highlights"]
    }
    return new_doc

def transfer_common_gen(doc, i):
    concepts = doc["concepts"]
    concepts_str = ", ".join(concepts)
    if not doc["target"]:
        return {}
    new_doc = {
        "id": doc["concept_set_idx"],
        "label": "QA",
        "question": f"use the following words to make a sentence: {concepts_str}\n",
        "answer": doc["target"]
    }
    return new_doc

def transfer_emo(doc, i):
    emo_map = {
        0: "others",
        1: "happy",
        2: "sad",
        3: "angry"
    }
    label = doc["label"]
    text = doc["text"]
    new_doc = {
        "id": i,
        "label": "MUL",
        "question": f"can you infer the emotions of the following sentence: {text}? ",
        "choices": ["happy", "sad", "angry", "others"],
        "answer": emo_map[label]
    }
    return new_doc

def transfer_fever(doc, i=0):
    fever_map = {
        "SUPPORTS": "yes",
        "REFUTES": "no",
        "NOT ENOUGH INFO": "not sure"
    }
    label = doc["label"].upper()
    claim = doc["claim"]
    new_doc = {
        "id": doc["id"],
        "label": "MUL",
        "question": f"This is a claim: {claim}, is it true? ",
        "answer": fever_map[label],
        "choices": [ "yes", "no", "not sure" ],
    }
    return new_doc

def transfer_hotpot(doc, i):
    sentences = doc["context"]["sentences"]
    info_ls = []
    for sen in sentences:
        info_ls.append(" ".join(sen))
    info_str = "\n".join(info_ls)
    new_doc = {
        "id": doc["id"],
        "label": "QA",
        "question": doc["question"],
        "answer": doc["answer"],
        "background": info_str
    }
    return new_doc

def transfer_imdb(doc, i):
    imdb_map = {
        0: "negative",
        1: "positive",
    }
    label = doc["label"]
    text = doc["text"]
    new_doc = {
        "id": i,
        "label": "MUL",
        "question": f"The following movie review expresses what sentiment? {text} ",
        "choices": ["negative", "positive"],
        "answer": imdb_map[label]
    }
    return new_doc

def transfer_math(doc, i):
    index_map = {
        "a": 0,
        "b": 1,
        "c": 2,
        "d": 3,
        "e": 4,
        "f": 5,
    }
    choices = doc["options"]
    choices = choices.split(",")
    choices = [choice.split(")")[-1].strip() for choice in choices if choice]
    new_doc = {
        "id": i,
        "label": "MUL",
        "question": "Solve this problem: " + doc["Problem"],
        "choices": choices,
        "answer": choices[index_map[doc["correct"].lower()]],
        "rationale": doc["Rationale"]
    }
    return new_doc

def transfer_multi_nli(doc, i=0):
    nli_map = {
        0: "entailment",
        1: "neutral",
        2: "contradiction"
    }
    premise = doc["premise"]
    hypothesis = doc["hypothesis"]
    label = doc["label"]
    new_doc = {
        "id": doc["promptID"],
        "label": "NLI",
        "question": f"Tell me the logical relationship of two following sentences\n1. {premise}\n2. {hypothesis} ",
        "answer": nli_map[label],
        "choices": [ "entailment", "neutral", "contradiction" ],
    }
    return new_doc

def transfer_openbook(doc, i=0):
    labels = doc["choices"]["label"]
    if not doc["answerKey"]:
        return {}
    answer_index = labels.index(doc["answerKey"])
    new_doc = {
        "id": doc["id"],
        "label": "MUL",
        "question": doc["question_stem"],
        "choices": doc["choices"]["text"],
        "answer": doc["choices"]["text"][answer_index],
        "background": doc.get("fact1", "")
    }
    return new_doc
    
def transfer_quoref(doc, i):
    new_doc = {
        "id": doc["id"],
        "label": "QA",
        "question": doc["question"],
        "answer": doc["answers"]["text"][0],
        "background": doc["context"]
    }
    return new_doc

def transfer_raceall(doc, i=0):
    ans_map = {
        "A": 0,
        "B": 1,
        "C": 2,
        "D": 3,
    }
    new_doc = {
        "id": i,
        "label": "MUL",
        "question": doc["question"],
        "choices": doc["options"],
        "answer": doc["options"][ans_map[doc["answer"].upper()]],
        "background": doc["article"]
    }
    return new_doc

def transfer_samsum(doc, i):
    new_doc = {
        "id": doc["id"],
        "label": "SUM",
        "question": doc["dialogue"],
        "answer": doc["summary"]
    }
    return new_doc

def transfer_sciq(doc, i=0):
    choices = [
        doc["distractor1"],
        doc["distractor2"],
        doc["distractor3"],
        doc["correct_answer"]
    ]
    random.shuffle(choices)
    new_doc = {
        "id": i,
        "label": "MUL",
        "question": doc["question"],
        "choices": choices,
        "answer": doc["correct_answer"],
        "background": doc["support"]
    }
    return new_doc

def transfer_snli(doc, i=0):
    nli_map = {
        0: "entailment",
        1: "neutral",
        2: "contradiction"
    }
    premise = doc["premise"]
    hypothesis = doc["hypothesis"]
    label = doc["label"]
    if label not in nli_map:
        return {}
    new_doc = {
        "id": i,
        "label": "NLI",
        "question": f"Tell me the logical relationship of two following sentences\n1. {premise}\n2. {hypothesis} ",
        "answer": nli_map[label],
        "choices": [ "entailment", "neutral", "contradiction" ],
    }
    return new_doc

def transfer_squad_v2(doc, i):
    if not doc["answers"]["text"]:
        return {}
    new_doc = {
        "id": doc["id"],
        "label": "QA",
        "question": doc["question"],
        "answer": doc["answers"]["text"],
        "background": doc["context"]
    }
    return new_doc

def transfer_superglue_axb(doc, i=0):
    nli_map = {
        0: "entailment",
        1: "not entailment",
    }
    premise = doc["sentence1"]
    hypothesis = doc["sentence2"]
    label = doc["label"]
    new_doc = {
        "id": doc["idx"],
        "label": "NLI",
        "question": f"Tell me the logical relationship of two following sentences\n1. {premise}\n2. {hypothesis} ",
        "answer": nli_map[label],
        "choices": [ "entailment", "not entailment" ],
    }
    return new_doc

def transfer_superglue_axg(doc, i=0):
    nli_map = {
        0: "entailment",
        1: "not entailment",
    }
    premise = doc["premise"]
    hypothesis = doc["hypothesis"]
    label = doc["label"]
    if label not in nli_map:
        return {}
    new_doc = {
        "id": doc["idx"],
        "label": "NLI",
        "question": f"Tell me the logical relationship of two following sentences\n1. {premise}\n2. {hypothesis} ",
        "answer": nli_map[label],
        "choices": [ "entailment", "not entailment" ],
    }
    return new_doc

def transfer_superglue_cb(doc, i=0):
    nli_map = {
        0: "entailment",
        2: "neutral",
        1: "contradiction"
    }
    premise = doc["premise"]
    hypothesis = doc["hypothesis"]
    label = doc["label"]
    if label not in nli_map:
        return {}
    new_doc = {
        "id": doc["idx"],
        "label": "NLI",
        "question": f"Tell me the logical relationship of two following sentences\n1. {premise}\n2. {hypothesis} ",
        "answer": nli_map[label],
        "choices": [ "entailment", "neutral", "contradiction" ],
    }
    return new_doc

def transfer_superglue_boolq(doc, i=0):
    nli_map = {
        0: "false",
        1: "true",
    }
    question = doc["question"]
    label = doc["label"]
    if label not in nli_map:
        return {}
    new_doc = {
        "id": doc["idx"],
        "label": "NLI",
        "question": f"{question}, is it true? ",
        "answer": nli_map[label],
        "choices": ["true", "false"],
        "background": doc["passage"],
    }
    return new_doc

def transfer_superglue_copa(doc, i=0):
    choices = [
        doc["choice1"],
        doc["choice2"],
    ]
    label = doc["label"]
    premise = doc["premise"]
    question = doc["question"]
    if label not in [0,1]:
        return {}
    new_doc = {
        "id": doc["idx"],
        "label": "MUL",
        "question": f"{premise}, what is the {question}?",
        "choices": choices,
        "answer": choices[label],
    }
    return new_doc

def transfer_superglue_multirc(doc, i=0):
    nli_map = {
        0: "false",
        1: "true",
    }
    question = doc["question"]
    label = doc["label"]
    if label not in nli_map:
        return {}
    answer = doc["answer"]
    new_doc = {
        "id": i,
        "label": "NLI",
        "question": f"{question} Answer: {answer}, is it true? ",
        "answer": nli_map[label],
        "choices": ["true", "false"],
        "background": doc["paragraph"],
    }
    return new_doc

def transfer_superglue_record(doc, i):
    query = doc["query"]
    new_doc = {
        "id": i,
        "label": "QA",
        "question": f"{query}, what is the @placeholder refer to?",
        "answer": doc["answers"],
        "background": doc["passage"]
    }
    return new_doc

def transfer_superglue_wic(doc, i=0):
    nli_map = {
        0: "no",
        1: "yes",
    }
    word = doc["word"]
    sen1 = doc["sentence1"]
    sen2 = doc["sentence2"]
    label = doc["label"]
    if label not in nli_map:
        return {}
    new_doc = {
        "id": i,
        "label": "NLI",
        "question": f"Does the word {word} have the same meaning in these two sentences?\n1. {sen1} \n2. {sen2}",
        "answer": nli_map[label],
        "choices": ["yes", "no"],
    }
    return new_doc

def transfer_superglue_wsc(doc, i=0):
    nli_map = {
        0: "no",
        1: "yes",
    }
    text = doc["text"]
    text1 = doc["span1_text"]
    text2 = doc["span2_text"]
    label = doc["label"]
    if label not in nli_map:
        return {}
    new_doc = {
        "id": i,
        "label": "NLI",
        "question": f"Sentence: {text} In the previous sentence, does the pronoun {text2.lower()} refer to {text1}?",
        "answer": nli_map[label],
        "choices": ["yes", "no"],
    }
    return new_doc

def transfer_swagregular(doc, i=0):
    choices = [
        doc["ending0"],
        doc["ending1"],
        doc["ending2"],
        doc["ending3"],
    ]
    label = doc["label"]
    start = doc["startphrase"]
    if label not in [0,1]:
        return {}
    new_doc = {
        "id": i,
        "label": "MUL",
        "question": f"{start}, what is the appropriate continuation? ",
        "choices": choices,
        "answer": choices[label],
    }
    return new_doc

def transfer_trec(doc, i=0):
    choices = [
        "Abbreviation",
        "Entity",
        "Description",
        "Person",
        "Location",
        "Numeric",
    ]
    label = doc["coarse_label"]
    text = doc["text"]
    if label not in list(range(0,6)):
        return {}
    new_doc = {
        "id": i,
        "label": "MUL",
        "question": f"What category best describes: {text} ? ",
        "choices": choices,
        "answer": choices[label],
    }
    return new_doc

def transfer_xsum(doc, i):
    new_doc = {
        "id": doc["id"],
        "label": "SUM",
        "question": doc["document"],
        "answer": doc["summary"]
    }
    return new_doc


FUNC_DICT = {
    "ai2_arcARC-Challenge": transfer_ai2_arc,
    "ai2_arcARC-Easy": transfer_ai2_arc,
    "anli": transfer_anli,
    "billsum": transfer_billsum,
    "cnn_dailymail3.0.0": transfer_cnn_daily,
    "common_gen": transfer_common_gen,
    "commonsense_qa": transfer_ai2_arc,
    "emo": transfer_emo,
    "feverv1.0": transfer_fever,
    "feverv2.0": transfer_fever,
    "hotpot_qadistractor": transfer_hotpot,
    "hotpot_qafullwiki": transfer_hotpot,
    "imdb": transfer_imdb,
    "math_qa": transfer_math,
    "multi_nli": transfer_multi_nli,
    "openbookqaadditional": transfer_openbook,
    "openbookqamain": transfer_openbook,
    "quoref": transfer_quoref,
    "raceall": transfer_raceall,
    "racehigh": transfer_raceall,
    "racemiddle": transfer_raceall,
    "samsum": transfer_samsum,
    "sciq": transfer_sciq,
    "snli": transfer_snli,
    "squad_v2": transfer_squad_v2,
    "super_glueaxb": transfer_superglue_axb,
    "super_glueaxg": transfer_superglue_axg,
    "super_glueboolq": transfer_superglue_boolq,
    "super_gluecb": transfer_superglue_cb,
    "super_gluecopa": transfer_superglue_copa,
    "super_gluemultirc": transfer_superglue_multirc,
    "super_gluerecord": transfer_superglue_record,
    "super_gluerte": transfer_superglue_axg,
    "super_gluewic": transfer_superglue_wic,
    "super_gluewsc.fixed": transfer_superglue_wsc,
    "swagregular": transfer_swagregular,
    "trec": transfer_trec,
    "xsum": transfer_xsum,
}



def transfer_data(filename, limit=500):
    path = os.path.join("./data", f"{filename}.jsonl")
    processed_path = os.path.join("./processed_data", f"{filename}_processed.jsonl")
    docs = load_data(path)
    processed = []
    for i, doc in enumerate(docs):
        processed.append(FUNC_DICT[filename](doc, i))
    processed = [pro for pro in processed if pro]
    random.shuffle(processed)
    processed = processed[:limit]
    print(f"{len(processed)} docs processed")
    with jsonlines.open(processed_path, "w") as writer:
        for doc in processed:
            writer.write(doc)

if __name__=="__main__":
    finished_ls = [
        "ai2_arcARC-Challenge",
        "ai2_arcARC-Easy",
        "anli",
        "billsum",
        "cnn_dailymail3.0.0",
        "commonsense_qa",
        "common_gen",
        "emo",
        "feverv1.0",
        "feverv2.0",
        "hotpot_qafullwiki",
        "hotpot_qadistractor",
        "imdb",
        "math_qa",
        "multi_nli",
        "openbookqamain",
        "openbookqaadditional",
        "quoref",
        "raceall",
        "racehigh",
        "racemiddle",
        "samsum",
        "sciq",
        "snli",
        "squad_v2",
        "super_glueaxb",
        "super_glueaxg",
        "super_gluecb",
        "super_glueboolq",
        "super_gluecopa",
        "super_gluemultirc",
        "super_gluerecord",
        "super_gluerte",
        "super_gluewic",
        "super_gluewsc.fixed",
        "swagregular",
        "trec",

    ]
    file_ls = [
        "xsum"
    ]
    for file in file_ls:
        transfer_data(file)
