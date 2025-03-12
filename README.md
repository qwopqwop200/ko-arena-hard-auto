# Ko-Arena-Hard-Auto

Ko-Arena-Hard-Auto는 한국어를 벤치마킹하기위한 자동 평가 도구입니다. 
Arena-Hard-Auto-v0.1([논문](https://arxiv.org/abs/2406.11939))가 수집한 500개의 어려운 질문을 번역하여 사용합니다.
gemini-2.0-flash-lite-001와 gpt-4o-mini를 심사위원(judge)으로 사용하고 모델의 응답을 기준 모델(기본값: claude-3.7-sonnet)과 비교합니다.

특히, 인간의 선호도와높은 상관관계와 분리력을 가지고 있는 Arena-Hard-Auto를 기반으로 두기에 실제로 높은 상관관계를 가지고 있을것으로 예상됩니다. 

더 자세한 세부사항은 [arena-hard-auto 코드](https://github.com/lmarena/arena-hard-auto)를 참조하세요.

ko-arena-hard-auto 데이터는 huggingface에 공개되어 있습니다. [ko-arena-hard-auto-v0.1](https://huggingface.co/datasets/qwopqwop/ko-arena-hard-auto-v0.1)

## Content
- [리더보드](#리더보드)
- [설치](#설치)
- [평가](#평가)
- [참고문헌](#참고문헌)

# 리더보드
 [style control](https://lmsys.org/blog/2024-08-28-style-control/)를 사용한 리더보드 입니다.
단순히 gemini-2.0-flash-lite-001와 gpt-4o-mini의 평과결과를 단순 평균한 결과입니다.
gemini-2.0-flash-lite-001와 gpt-4o-mini는 자신의 답변을 선호하는 경향이 있기에 해석을 주의해야 합니다.

(업데이트: 2025/03/12)
```console
claude-3.7-sonnet                             | score:  50.00 | average #tokens: 1094
o1-medium                                     | score:  43.10 | average #tokens: 1487
o3-mini-high                                  | score:  42.80 | average #tokens: 1257
gemini-2.0-flash-001                          | score:  32.52 | average #tokens: 1901
claude-3.5-sonnet                             | score:  36.00 | average #tokens: 682
o3-mini-medium                                | score:  36.73 | average #tokens: 1221
gpt-4.5-preview                               | score:  38.26 | average #tokens: 1040
gemini-2.0-flash-lite-001(judge)              | score:  29.76 | average #tokens: 2196
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
gpt-4o-mini(judge)                            | score:  16.39 | average #tokens: 890
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

# 설치
```
git clone https://github.com/qwopqwop200/ko-arena-hard-auto
cd arena-hard
pip install -r requirements.txt
pip install -r requirements-optional.txt  # 선택사항 (e.g., anthropic sdk)
```
## 평가

### Step 1. 모델의 엔드포인트 설정
`config/api_config.yaml`에 API 엔드포인트를 입력하세요. OpenAI 호환 API 서버를 지원합니다. `parallel`을 지정하여 동시 API 요청 수를 지정할 수 있습니다(기본값: 1).

o1, o3-mini와 같은 추론 모델은 현재 자동으로 지원되지 않으며 추가적인 코드 작업이 필요합니다.
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

### Step 2. 모델 답변 생선

`config/gen_answer_config.yaml`에 모델 이름을 `model_list`에 추가하세요.
```yaml
bench_name: ko-arena-hard-v0.1
temperature: 0.0
max_tokens: 4096
num_choices: 1


model_list:
  - [YOUR-MODEL-NAME]
```

답변을 생성하려면 다음 명령어을 실행하세요.
```console
python gen_answer.py
```
캐싱 기능이 구현되어 있어, 동일한 질문에 대한 답변이 이미 있는 경우 답변을 생성하지 않습니다.

### Step 3. 판단(Judgment) 생성

`config/judge_config.yaml`에 모델 이름을 `model_list`에 추가하세요.
```yaml
...
# 평가할 모델을 아래에 추가하세요
model_list:
  - gpt-3.5-turbo-0125
  - [YOUR-MODEL-NAME]
```

Run the command to generate judgments:
```console
python gen_judgment.py
```
판단 캐싱도 구현되어 있습니다. 이미 생성된 판단이 있는 경우 또는 모델 답변 중 하나가 없는 경우 판단을 생성하지 않습니다.

### Step 4. 결과 보기
모델 승률을 출력합니다. 모델 순위를 csv 파일로 저장하려면 `--output`을 사용하세요. 기본적으로 --style-control을 사용합니다. 
이는 더 높은 인간의 선호도와 더 높은 상관관계를 가지고 있다고 알려져 있습니다.
```console
> python show_result.py --style-control --num-rounds 1000
```

### Step 5. Arena Hard UI
UI 코드를 사용하여 개별 판단 결과를 검토할 수 있습니다.
```console
> python qa_browser.py --share
```

## 참고문헌
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
