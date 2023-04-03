import requests
import json
import sys
import io
import concurrent.futures
from typing import List
class api_model:
    def __init__(self, workers = 20):
        self.workers = workers
        
    def call_api_in_parallel(self, prompts: List[str], workers: int, timeout: int = 60) -> List[str]:
        def get_result_with_retry(prompt, retries=3, timeout=timeout):
            for attempt in range(retries):
                with concurrent.futures.ThreadPoolExecutor(max_workers=1) as timeout_executor:
                    future = timeout_executor.submit(self.get_api_result, prompt)
                    try:
                        return future.result(timeout)
                    except concurrent.futures.TimeoutError:
                        print(f"Timeout occurred while fetching results for prompt (attempt {attempt + 1})")
                    except Exception as e:
                        print(f"Error occurred while fetching results for prompt {e}")
                        break
            return None

        results = [None] * len(prompts)
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {executor.submit(get_result_with_retry, prompt): index for index, prompt in enumerate(prompts)}

            for future in concurrent.futures.as_completed(futures):
                index = futures[future]
                results[index] = future.result()

        return results

    def generate_text(self, batch):
        output = []
        for prompts in batch:
            result = self.call_api_in_parallel(prompts["text"], self.workers)
            output.extend(result)
        return output
    
    def get_api_result(self, prompt):
        pass

class ChatGPT(api_model):
    def __init__(self, workers = 20):
        self.url = ""
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
    

class ChatGLM:
    def __init__(self, workers = 20):
        self.url = ""
        self.seed = 2333
        self.temperature = 0.95
        self.max_tokens = 10
        self.workers = workers

    def get_api_result(self, prompt):
        url = self.url

        payload = json.dumps({
            "prompt": prompt,
            "seed": self.seed,
            "history": []
        })
        headers = {
            'Authorization': '',
            'Content-Type': 'application/json; charset=utf-8'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)


    def generate_text(self, batch):
        output = []
        for prompt in batch:
            result = self.get_api_result(prompt)
            output.append(result)
        return output


def get_model_api(model_name, workers = 20):
    if model_name == "ChatGLM":
        model = ChatGLM(workers)
        return model
    if model_name == "ChatGPT":
        model = ChatGPT(workers)
        return model