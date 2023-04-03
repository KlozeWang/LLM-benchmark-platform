# LLM-benchmark

使用方法：

```
bash scripts/evaluate.sh ChatGPT task1.yaml task2.yaml dir1 dir2 ...
```

目前只支持ChatGPT端口调用，稍后会在群里发一个url，粘贴到evaluation/model_api.py 

```
class ChatGPT(api_model):
    def __init__(self, workers = 20):
        self.url = ""
```

然后即可使用。

tasks/test/Summ.yaml是一个测评SummEval文本摘要数据集的例子，可以直接运行。log和预测结果会被输出到相应文件夹。

具体的使用方法参考Evaluate Your Own Tasks.md。

若想在windows上使用，可以在git bash中运行代替bash。

这是一个可以很轻松的拓展任务评测的框架，只需要提供数据和相应的参数，就可以自动调用api生成评测结果，并且保存输出。你也可以在tasks/[your file]下轻松的建立新的task，重写评测手段（目前只实现了BLEU和ROUGE），或者重写其他任何东西。

你也可以在model-api中编辑自己的api，并且在--model参数中调用。这部分还待完善，可以先使用已经写好的openai api。