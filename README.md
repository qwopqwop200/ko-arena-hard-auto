# Arena-Hard-Auto

Arena-Hard-Auto-v0.1 ([See Paper](https://arxiv.org/abs/2406.11939)) is an automatic evaluation tool for instruction-tuned LLMs. It contains 500 challenging user queries sourced from Chatbot Arena. We prompt GPT-4-Turbo as judge to compare the models' responses against a baseline model (default: GPT-4-0314). Notably, Arena-Hard-Auto has the highest correlation and separability to Chatbot Arena among popular open-ended LLM benchmarks ([See Paper](https://arxiv.org/abs/2406.11939)). If you are curious to see how well your model might perform on Chatbot Arena, we recommend trying Arena-Hard-Auto.

Although both Arena-Hard-Auto and Chatbot Arena Category Hard ([See Blog](https://lmsys.org/blog/2024-05-17-category-hard/)) employ similar pipeline to select hard prompts, Arena-Hard-Auto employs automatic judge as a cheaper and faster approximator to human preference. Checkout [BenchBuilder](BenchBuilder) folder for code and resources on how we curate Arena-Hard-Auto. In the paper we also purposed metrics, such as model separability and agreement to human preference, for evaluating benchmarks' ability to rank models (See [Evaluate Benchmarks](#evaluate-benchmarks) for more information and code).

## Content
- [Install](#install-dependencies)
- [Evaluation](#evaluate)
- [Style Control: how to mitigate biases](#style-control)
- [Evaluate Benchmarks: how to evaluate benchmarks](#evaluate-benchmarks)
- [Citation](#citation)

# Leaderboard
The following leaderboard has [style control](https://lmsys.org/blog/2024-08-28-style-control/).

(Updated: 2025/03/12)
```console
claude-3.7-sonnet                             | score:  50.00 | average #tokens: 1094
o1-medium                                     | score:  43.10 | average #tokens: 1487
o3-mini-high                                  | score:  42.80 | average #tokens: 1257
gemini-2.0-flash-001                          | score:  32.52 | average #tokens: 1901
claude-3.5-sonnet                             | score:  36.00 | average #tokens: 682
o3-mini-medium                                | score:  36.73 | average #tokens: 1221
gpt-4.5-preview                               | score:  38.26 | average #tokens: 1040
gemini-2.0-flash-lite-001                     | score:  29.76 | average #tokens: 2196
o3-mini-low                                   | score:  33.41 | average #tokens: 1205
claude-3.5-haiku                              | score:  27.86 | average #tokens: 601
gpt-4o-2024-11-20                             | score:  28.06 | average #tokens: 1216
claude-3.5-sonnet-20240620                    | score:  23.70 | average #tokens: 628
minimax-01                                    | score:  20.02 | average #tokens: 370
grok-2-1212                                   | score:  19.20 | average #tokens: 898
deepseek-v3                                   | score:  22.60 | average #tokens: 1007
qwen-2.5-72b-instruct                         | score:  17.77 | average #tokens: 1097
nova-pro-v1                                   | score:  17.93 | average #tokens: 905
gemma-2-27b-it                                | score:  15.18 | average #tokens: 794
gpt-4-1106-preview                            | score:  15.41 | average #tokens: 846
mistral-large-2411                            | score:  16.68 | average #tokens: 906
gpt-4o-mini                                   | score:  16.39 | average #tokens: 890
qwen2.5-32b-instruct                          | score:  11.38 | average #tokens: 795
wizardlm-2-8x22b                              | score:  12.67 | average #tokens: 1028
command-r-plus-08-2024                        | score:  12.64 | average #tokens: 969
nova-lite-v1                                  | score:  12.16 | average #tokens: 994
hermes-3-llama-3.1-405b                       | score:  10.57 | average #tokens: 771
gemma-2-9b-it                                 | score:   9.48 | average #tokens: 751
mistral-small-24b-instruct-2501               | score:  11.15 | average #tokens: 998
hermes-3-llama-3.1-70b                        | score:   9.90 | average #tokens: 771
lfm-7b                                        | score:  11.21 | average #tokens: 1011
lfm-40b                                       | score:   8.49 | average #tokens: 863
llama-3.3-70b-instruct                        | score:   7.38 | average #tokens: 809
command-r-08-2024                             | score:   9.13 | average #tokens: 796
nova-micro-v1                                 | score:   8.71 | average #tokens: 927
lfm-3b                                        | score:   5.06 | average #tokens: 776
command-r7b-12-2024                           | score:   6.47 | average #tokens: 882
qwen-2.5-7b-instruct                          | score:   5.32 | average #tokens: 844
llama-3.1-nemotron-70b-instruct               | score:   4.32 | average #tokens: 1854
llama-3.1-405b-instruct                       | score:   2.45 | average #tokens: 1735
llama-3.1-70b-instruct                        | score:   1.56 | average #tokens: 1923
llama-3.1-8b-instruct                         | score:   0.42 | average #tokens: 5081                                                                                            
```

## Install Dependencies
```
git clone https://github.com/lm-sys/arena-hard.git
cd arena-hard
pip install -r requirements.txt
pip install -r requirements-optional.txt  # Optional dependencies (e.g., anthropic sdk)
```

## Download dataset
We have pre-generated many popular models answers and judgments. You can browse them with an online [demo](https://huggingface.co/spaces/lmsys/arena-hard-browser) or download them (with [`git-lfs`](https://git-lfs.com) installed) by
```console
> git clone https://huggingface.co/spaces/lmsys/arena-hard-browser
// copy answers/judgments to the data directory
> cp -r arena-hard-browser/data . 
```
Then run
```console
> python show_result.py
gpt-4-0125-preview             | score: 78.0  | 95% CI: (-1.8, 2.2)  | average #tokens: 619
claude-3-opus-20240229         | score: 60.4  | 95% CI: (-2.6, 2.1)  | average #tokens: 541
gpt-4-0314                     | score: 50.0  | 95% CI:  (0.0, 0.0)  | average #tokens: 423
claude-3-sonnet-20240229       | score: 46.8  | 95% CI: (-2.7, 2.3)  | average #tokens: 552
claude-3-haiku-20240307        | score: 41.5  | 95% CI: (-2.4, 2.5)  | average #tokens: 505
gpt-4-0613                     | score: 37.9  | 95% CI: (-2.1, 2.2)  | average #tokens: 354
mistral-large-2402             | score: 37.7  | 95% CI: (-2.9, 2.8)  | average #tokens: 400
Qwen1.5-72B-Chat               | score: 36.1  | 95% CI: (-2.1, 2.4)  | average #tokens: 474
command-r-plus                 | score: 33.1  | 95% CI: (-2.0, 1.9)  | average #tokens: 541
```
Running `show_result.py` will save generated battles into `data/arena_hard_battles.jsonl` and bootstrapping statistics into `data/bootstrapping_results.jsonl`. If you don't want to regenerate battles or bootstrapping statistics, simply toggle argument `--load-battles` or `--load-bootstrap`, respectively.

## Evaluate

### Step 1. Set up the endpoint config to your model

Fill in your API endpoint in `config/api_config.yaml`. We support OpenAI compatible API server. You can specify `parallel` to indicate the number of concurrent API requests (default: 1).
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
You may use inference engine such as [Latest TGI version](https://huggingface.co/docs/text-generation-inference/en/messages_api) or [vLLM](https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html) or [SGLang](https://github.com/sgl-project/sglang?tab=readme-ov-file#using-local-models) to host your model with an OpenAI compatible API server.

TGI Quick start
```
hf_pat=
model=
volume=/path/to/cache
port=1996

huggingface-cli download $model
sudo docker run --gpus 8 -e HUGGING_FACE_HUB_TOKEN=$hf_pat --shm-size 2000g -p $port:80 -v $volume:/data ghcr.io/huggingface/text-generation-inference:2.0.4 --model-id $model --max-input-length 8192 --max-batch-total-tokens 8193 --max-batch-prefill-tokens 8193 --max-total-tokens 8193
```

### Step 2. Generate Model Answers

In `config/gen_answer_config.yaml`, add your model name in `model_list`.
```yaml
bench_name: ko-arena-hard-v0.1
temperature: 0.0
max_tokens: 4096
num_choices: 1


model_list:
  - [YOUR-MODEL-NAME]
```
Run the command to generate answers:
```console
python gen_answer.py
```
Caching feature is implemented. The code will skip generating an answer when there is already an existing answer/judgment to the same prompt. 

### Step 3. Generate Judgments

In `config/judge_config.yaml`, add your model name in `model_list`.
```yaml
...
# Add your model below for evaluation
model_list:
  - gpt-3.5-turbo-0125
  - [YOUR-MODEL-NAME]
```

Run the command to generate judgments:
```console
python gen_judgment.py
```
Judgment caching is also implemented. It will skip generating judgments that has already been generated or lacks one of the model answers.  

### Step 4. Show result
Output model win rates. To save a csv file of the model rankings, use `--output`
```console
> python show_result.py --style-control --num-rounds 1000
```

### Step 5. Arena Hard UI
You can review individual judgment results using our UI code.
```console
> python qa_browser.py --share
```

## Style Control
Following the newly introduced Style Control on Chatbot Arena, we release Style Control on Arena Hard Auto! We employ the same Style Control methods as proposed in the [blogpost](https://lmsys.org/blog/2024-08-28-style-control/). Please refer to the blogpost for methodology and technical background.
To control for style (token length and markdown elements), use `--style-control` when running `show_result.py`.

```console
> python show_result.py --style-control
```

## Evaluate Benchmarks
We outline two key properties that the benchmark aiming to approximate human preference should possess to provide meaningful comparisons between models:
1. Separability: the benchmark should separate models with high confidence.
2. Alignment with Human Preference: the benchmark should agree with human preference.

While previous works have focused on alignment, separability is also a crucial consideration when comparing models of similar quality (e.g., different checkpoints from the same training run). However, achieving high-confidence separability is challenging due to limitations in prompt design and inherent variances in LLM evaluations. Overly simplistic prompts fail to distinguish between models, while the randomness in human and LLM judgments leads to inconsistent predictions. As a result, it is often difficult to confidently determine if a model’s apparent performance reflects a genuine difference in capability or merely noisy observations, highlighting a need for methods to verify whether a benchmark can reliably separate similar models.

Statistical measures like Pearson (Pearson, 1895) and Spearman Correlations (Spearman, 1961), commonly used in benchmarks such as AlpacaEval (Li et al., 2023) to measure correlation to human preference ranking, may fail to adequately address model separability and ranking instability. In addition, these measures only provide a coarse signal of ranking correlation without quantifying the magnitude of performance differences between model pairs. To address these shortcomings, we develop three novel metrics: **Separability with Confidence**, **Agreement with Confidence**, and **Pair Rank Brier Score**.

**Separability with Confidence** quantifies the benchmark’s confidence by measuring its consistency in predicting the winner of a model pair across random seeds through bootstrapping. This is done by calculating the percentage of model pairs that have non-overlapping confidence intervals of their benchmark scores. A higher percentage indicates that the benchmark is more confident in distinguishing between the performance of different models, as the confidence intervals of their scores do not overlap.

For **Agreement with Confidence**, and **Pair Rank Brier Score**, please refer to section 3 of our [paper](https://arxiv.org/abs/2406.11939). The code for calculating these metrics can be found in this [colab notebook](https://colab.research.google.com/drive/1ar6XLWREN_dXEh404WNOxroFVUe_4njp). 

## Citation
The code in this repository is developed from the papers below. Please cite it if you find the repository helpful.
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
