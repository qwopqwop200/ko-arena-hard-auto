# Ko-Arena-Hard-Auto

Ko-Arena-Hard-Auto는 한국어를 벤치마킹하기위한 자동 평가 도구입니다. 
Arena-Hard-Auto-v0.1([논문](https://arxiv.org/abs/2406.11939))가 수집한 500개의 어려운 질문을 번역하여 사용합니다.
gemini-2.0-flash와 gpt-4o-mini를 judge(심사위원)으로 사용하고 모델의 응답을 baseline 모델(기본값: claude-3.7-sonnet)과 비교합니다.

특히, 인간의 선호도와높은 상관관계와 분리력을 가지고 있는 Arena-Hard-Auto를 기반으로 두기에 실제로 높은 상관관계를 가지고 있을것으로 예상됩니다. 

더 자세한 세부사항은 [arena-hard-auto 코드](https://github.com/lmarena/arena-hard-auto)를 참조하세요.

ko-arena-hard-auto 데이터는 huggingface에 공개되어 있습니다. [ko-arena-hard-auto-v0.1](https://huggingface.co/datasets/qwopqwop/ko-arena-hard-auto-v0.1)<br>
리더보드 사이트: https://qwopqwop200.github.io/ko-arena-hard-auto/leaderboard.html

## 원래 구현과의 주요 차이점
이 포크는 다음과 같은 주요 변경 사항이 있습니다. 

1. 데이터셋 및 프롬프트: [ko-arena-hard-auto-v0.1](https://huggingface.co/datasets/qwopqwop/ko-arena-hard-auto-v0.1) 데이터셋과 심사할때 다른 [시스템 프롬프트](https://github.com/qwopqwop200/ko-arena-hard-auto/blob/main/config/judge_config.yaml#L23)를 사용합니다.
2. judge 모델: gemini-2.0-flash와 gpt-4o-mini을 사용하고 앙상블 합니다. 이는 자기 선호도 편향을 완화하기 위한것 입니다.
3. baseline 모델: claude-3.7-sonnet을 사용합니다.

## 목차
- [리더보드](#리더보드)
- [설치](#설치)
- [평가](#평가)
- [참고문헌](#참고문헌)

# 리더보드
 [style control](https://lmsys.org/blog/2024-08-28-style-control/)를 사용한 리더보드 입니다.
gemini-2.0-flash와 gpt-4o-mini는 자신의 답변을 선호하는 경향이 있기에 해석을 주의해야 합니다.

(업데이트: 2025/03/25)
```console
claude-3.7-sonnet              | score: 50.0  | 95% CI:  (0.0, 0.0)  | average #tokens: 1094
deepseek-chat-v3-0324          | score: 46.5  | 95% CI: (-2.3, 2.3)  | average #tokens: 1085
o1-high                        | score: 40.7  | 95% CI: (-2.2, 2.3)  | average #tokens: 1503
o3-mini-high                   | score: 39.7  | 95% CI: (-2.2, 2.2)  | average #tokens: 1257
o1-medium                      | score: 38.9  | 95% CI: (-2.4, 2.4)  | average #tokens: 1487
gpt-4.5-preview                | score: 38.0  | 95% CI: (-2.4, 2.2)  | average #tokens: 1040
o1-low                         | score: 35.1  | 95% CI: (-2.2, 2.3)  | average #tokens: 1513
claude-3.5-sonnet              | score: 34.8  | 95% CI: (-2.5, 2.7)  | average #tokens: 682
o3-mini-medium                 | score: 33.1  | 95% CI: (-2.2, 2.1)  | average #tokens: 1221
command-a                      | score: 31.8  | 95% CI: (-2.0, 2.1)  | average #tokens: 1083
o3-mini-low                    | score: 30.3  | 95% CI: (-2.0, 2.0)  | average #tokens: 1205
gpt-4o-2024-11-20              | score: 27.0  | 95% CI: (-1.8, 1.8)  | average #tokens: 1216
claude-3.5-haiku               | score: 26.7  | 95% CI: (-2.6, 2.6)  | average #tokens: 601
gemini-2.0-flash-001           | score: 25.5  | 95% CI: (-2.0, 1.9)  | average #tokens: 1901
gemma-3-27b-it                 | score: 24.4  | 95% CI: (-1.7, 1.8)  | average #tokens: 1654
gemini-2.0-flash-lite-001      | score: 22.9  | 95% CI: (-1.8, 1.9)  | average #tokens: 2196
claude-3.5-sonnet-20240620     | score: 21.8  | 95% CI: (-2.4, 2.1)  | average #tokens: 628
deepseek-v3                    | score: 21.6  | 95% CI: (-1.8, 1.8)  | average #tokens: 1007
jamba-1.6-large                | score: 15.8  | 95% CI: (-1.4, 1.6)  | average #tokens: 859
grok-2-1212                    | score: 15.7  | 95% CI: (-1.6, 1.7)  | average #tokens: 898
minimax-01                     | score: 15.2  | 95% CI: (-2.1, 2.2)  | average #tokens: 370
nova-pro-v1                    | score: 14.9  | 95% CI: (-1.5, 1.5)  | average #tokens: 905
qwen-2.5-72b-instruct          | score: 14.7  | 95% CI: (-1.3, 1.4)  | average #tokens: 1097
gpt-4o-mini                    | score: 14.1  | 95% CI: (-1.4, 1.6)  | average #tokens: 890
mistral-large-2411             | score: 13.4  | 95% CI: (-1.3, 1.5)  | average #tokens: 906
gpt-4-1106-preview             | score: 11.9  | 95% CI: (-1.4, 1.4)  | average #tokens: 846
gemma-2-27b-it                 | score: 11.8  | 95% CI: (-1.4, 1.3)  | average #tokens: 794
mistral-small-3.1-24b-instruct-2503 | score:  9.8  | 95% CI: (-1.1, 1.3)  | average #tokens: 961
command-r-plus-08-2024         | score:  9.4  | 95% CI: (-1.2, 1.1)  | average #tokens: 969
nova-lite-v1                   | score:  8.8  | 95% CI: (-1.0, 1.0)  | average #tokens: 994
wizardlm-2-8x22b               | score:  8.8  | 95% CI: (-1.0, 1.1)  | average #tokens: 1028
lfm-7b                         | score:  8.4  | 95% CI: (-0.9, 1.0)  | average #tokens: 1011
qwen2.5-32b-instruct           | score:  8.2  | 95% CI: (-1.1, 1.2)  | average #tokens: 795
mistral-small-24b-instruct-2501 | score:  7.8  | 95% CI: (-1.1, 1.2)  | average #tokens: 998
hermes-3-llama-3.1-405b        | score:  7.6  | 95% CI: (-1.0, 1.2)  | average #tokens: 771
hermes-3-llama-3.1-70b         | score:  7.1  | 95% CI: (-1.0, 1.1)  | average #tokens: 771
gemma-2-9b-it                  | score:  6.9  | 95% CI: (-1.0, 1.2)  | average #tokens: 751
command-r-08-2024              | score:  6.1  | 95% CI: (-1.0, 1.1)  | average #tokens: 796
nova-micro-v1                  | score:  6.0  | 95% CI: (-0.8, 0.8)  | average #tokens: 927
lfm-40b                        | score:  5.3  | 95% CI: (-0.8, 0.9)  | average #tokens: 863
llama-3.3-70b-instruct         | score:  4.9  | 95% CI: (-1.0, 1.0)  | average #tokens: 809
command-r7b-12-2024            | score:  4.6  | 95% CI: (-0.8, 0.8)  | average #tokens: 882
qwen-2.5-7b-instruct           | score:  3.2  | 95% CI: (-0.7, 0.9)  | average #tokens: 844
lfm-3b                         | score:  3.2  | 95% CI: (-0.6, 0.6)  | average #tokens: 776
olmo-2-0325-32b-instruct       | score:  3.0  | 95% CI: (-0.5, 0.6)  | average #tokens: 890
jamba-1.6-mini                 | score:  2.3  | 95% CI: (-0.5, 0.5)  | average #tokens: 920
llama-3.1-nemotron-70b-instruct | score:  2.1  | 95% CI: (-0.4, 0.4)  | average #tokens: 1854
llama-3.1-405b-instruct        | score:  0.8  | 95% CI: (-0.2, 0.2)  | average #tokens: 1735
llama-3.1-70b-instruct         | score:  0.5  | 95% CI: (-0.1, 0.1)  | average #tokens: 1923
llama-3.1-8b-instruct          | score:  0.1  | 95% CI: (-0.0, 0.0)  | average #tokens: 5081                                                                      
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


### step 4. 판단 앙상블 생성
모델들을 앙상블하여 판단을 생성합니다.
```console
python gen_ensemble_judgment.py
```

### Step 5. 결과 보기
모델 승률을 출력합니다. 모델 순위를 csv 파일로 저장하려면 `--output`을 사용하세요. 기본적으로 --style-control을 사용합니다. 
이는 더 높은 인간의 선호도와 더 높은 상관관계를 가지고 있다고 알려져 있습니다.
```console
python show_result.py --style-control --num-rounds 1000
```

### Step 6. Arena Hard UI
UI 코드를 사용하여 개별 판단 결과를 검토할 수 있습니다.
```console
python qa_browser.py --share
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
