from evaluation.utils import print_rank_0
import requests
import json
import sys
import io
import time
import pdb
import concurrent.futures
from tqdm import tqdm
from typing import List
import threading


class api_model:
    def __init__(self, workers = 20):
        self.workers = workers

    def call_api_in_parallel(self, prompts, workers: int, timeout: int = 60) -> List[str]:

        def get_result_with_retry(prompt, retries=3, timeout=timeout):
            for attempt in range(retries):
                result = [None]
                timeout_event = threading.Event()

                def target():
                    try:
                        result[0] = self.get_api_result(prompt)
                    except Exception as e:
                        print(f"Error occurred while fetching results for prompt: {e}")
                        result[0] = None
                    finally:
                        timeout_event.set()

                worker = threading.Thread(target=target)
                worker.start()

                if not timeout_event.wait(timeout):
                    print(f"Timeout occurred while fetching results for prompt (attempt {attempt + 1})")
                else:
                    break

            return result[0]

        def worker_thread(prompt, index, results):
            results[index] = get_result_with_retry(prompt)

        threads = []
        results = [None] * len(prompts)

        for index, data in tqdm(enumerate(prompts)):
            prompt = data[0]["text"]
            t = threading.Thread(target=worker_thread, args=(prompt, index, results))
            t.start()
            threads.append(t)

            if len(threads) >= workers:
                threads[0].join()
                threads.pop(0)

        for t in threads:
            t.join()

        return results

    def generate_text(self, dataset):
        result = self.call_api_in_parallel(dataset, self.workers)
        return result
    
    def get_api_result(self, prompt):
        pass



class ChatGPT(api_model):
    def __init__(self, workers = 10):
        self.url = [] #yuhao提供的接口
        self.model = "gpt-3.5-turbo"
        self.workers = workers

    def get_api_result(self, prompt):
        url = self.url

        payload = json.dumps({
            "model": self.model,
            "messages": [
            {
                "role": "user",
                "content": prompt
                }
            ]
            })
        headers = {
            'Content-Type': 'application/json'
            }

        response = requests.request("POST", url, headers=headers, data=payload)

        return json.loads(response.text).get("choices")[0].get("message").get("content")
    



def get_model_api(model_name, workers = 20):
    if model_name == "ChatGPT":
        model = ChatGPT(workers)
        return model