# Ko-Arena-Hard-Auto
[한국어](README.md) / English<br>

[Leaderboard](https://qwopqwop200.github.io/ko-arena-hard-auto/leaderboard.html) / [Dataset](https://huggingface.co/datasets/qwopqwop/ko-arena-hard-auto-v0.1)

Ko-Arena-Hard-Auto is an automated evaluation tool for benchmarking Korean language models.<br>
It uses 500 challenging questions collected by Arena-Hard-Auto-v0.1 ([Paper](https://arxiv.org/abs/2406.11939)), translated into Korean.<br>
It uses gemini-2.0-flash, gpt-4o-mini, deepseek-chat-v3-0324 as judges and compares the model's responses against a baseline model (default: claude-3.7-sonnet).<br>

For more details, please refer to the [arena-hard-auto code](https://github.com/lmarena/arena-hard-auto).

## Key Differences from the Original Implementation
This fork includes the following major changes:

1.  **Dataset and Prompts**: Uses the [ko-arena-hard-auto-v0.1](https://huggingface.co/datasets/qwopqwop/ko-arena-hard-auto-v0.1) dataset and different [system prompts](https://github.com/qwopqwop200/ko-arena-hard-auto/blob/main/config/judge_config.yaml#L23) for judging.
2.  **Judge Models**: Uses gemini-2.0-flash, gpt-4o-mini, deepseek-chat-v3-0324 and ensembles their judgments. This is intended to mitigate self-preference bias.
3.  **Baseline Model**: Uses claude-3.7-sonnet.

## Table of Contents
- [Installation](#installation)
- [Evaluation](#evaluation)
- [References](#references)

# Installation
```bash
git clone https://github.com/qwopqwop200/ko-arena-hard-auto
cd ko-arena-hard-auto # Assuming the cloned directory name, adjust if different
pip install -r requirements.txt
pip install -r requirements-optional.txt  # Optional (e.g., anthropic sdk)
```
*Note: The original README had `cd arena-hard`, but the repo name is `ko-arena-hard-auto`. I've adjusted the `cd` command accordingly. Please verify the actual directory name after cloning.*

## Evaluation

### Step 1. Configure Model Endpoints
Enter your API endpoints in `config/api_config.yaml`. Supports OpenAI-compatible API servers. You can specify the number of concurrent API requests using `parallel` (default: 1).

Inference models like o1, o3-mini are not automatically supported currently and require additional code modifications.
```yaml
# example
gpt-3.5-turbo-0125:
    model_name: gpt-3.5-turbo-0125
    endpoints: null
    api_type: openai
    parallel: 8

[YOUR-MODEL-NAME]:
    model_name: [YOUR-MODEL-NAME]
    endpoints:
        - api_base: [YOUR-ENDPOINT-URL]
          api_key: [YOUR-API-KEY]
    api_type: openai
    parallel: 8
```

### Step 2. Generate Model Answers

Add your model name(s) to the `model_list` in `config/gen_answer_config.yaml`.
```yaml
bench_name: ko-arena-hard-v0.1
temperature: 0.0
max_tokens: 4096
num_choices: 1

model_list:
  - [YOUR-MODEL-NAME]
```

To generate answers, run the following command:
```console
python gen_answer.py
```
A caching feature is implemented. Answers for the same question will not be generated if they already exist.

### Step 3. Generate Judgments

Add your model name(s) to the `model_list` in `config/judge_config.yaml`.
```yaml
...
# Add models to evaluate below
model_list:
  - gpt-3.5-turbo-0125
  - [YOUR-MODEL-NAME]
```

Run the command to generate judgments:
```console
python gen_judgment.py
```
Judgment caching is also implemented. Judgments will not be generated if they already exist or if one of the model answers is missing.

### Step 4. Generate Ensemble Judgments
Generate ensemble judgments from the individual judge models.
```console
python gen_ensemble_judgment.py
```

### Step 5. Save Results
Save the model evaluation results to a file.
```console
python show_result.py
```

### Step 6. Arena Hard UI
You can use the UI code to review individual judgment results.
```console
python qa_browser.py --share
```

## References
```
@article{li2024crowdsourced,
  title={From Crowdsourced Data to High-Quality Benchmarks: Arena-Hard and BenchBuilder Pipeline},
  author={Li, Tianle and Chiang, Wei-Lin and Frick, Evan and Dunlap, Lisa and Wu, Tianhao and Zhu, Banghua and Gonzalez, Joseph E and Stoica, Ion},
  journal={arXiv preprint arXiv:2406.11939},
  year={2024}
}
@misc{arenahard2024,
    title = {From Live Data to High-Quality Benchmarks: The Arena-Hard Pipeline},
    url = {https://lmsys.org/blog/2024-04-19-arena-hard/},
    author = {Tianle Li*, Wei-Lin Chiang*, Evan Frick, Lisa Dunlap, Banghua Zhu, Joseph E. Gonzalez, Ion Stoica},
    month = {April},
    year = {2024}
}
```