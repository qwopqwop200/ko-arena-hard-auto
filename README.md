# Ko-Arena-Hard-Auto
한국어 / [English](README_EN.md)

[리더보드](https://qwopqwop200.github.io/ko-arena-hard-auto/leaderboard.html) / [데이터셋](https://huggingface.co/datasets/qwopqwop/ko-arena-hard-auto-v0.1)

Ko-Arena-Hard-Auto는 한국어를 벤치마킹하기위한 자동 평가 도구입니다.<br>
Arena-Hard-Auto-v0.1([논문](https://arxiv.org/abs/2406.11939))가 수집한 500개의 어려운 질문을 번역하여 사용합니다.<br>
gemini-2.0-flash, gpt-4o-mini, deepseek-chat-v3-0324를 judge(심사위원)으로 사용하고 모델의 응답을 baseline 모델(기본값: claude-3.7-sonnet)과 비교합니다.<br>

자세한 세부사항은 [arena-hard-auto 코드](https://github.com/lmarena/arena-hard-auto)를 참조하세요.

## 원래 구현과의 주요 차이점
이 포크는 다음과 같은 주요 변경 사항이 있습니다. 

1. 데이터셋 및 프롬프트: [ko-arena-hard-auto-v0.1](https://huggingface.co/datasets/qwopqwop/ko-arena-hard-auto-v0.1) 데이터셋과 심사할때 다른 [시스템 프롬프트](https://github.com/qwopqwop200/ko-arena-hard-auto/blob/main/config/judge_config.yaml#L23)를 사용합니다.
2. judge 모델: gemini-2.0-flash, gpt-4o-mini, deepseek-chat-v3-0324을 사용하고 앙상블 합니다. 이는 자기 선호도 편향을 완화하기 위한것 입니다.
3. baseline 모델: claude-3.7-sonnet을 사용합니다.

## 목차
- [설치](#설치)
- [평가](#평가)
- [참고문헌](#참고문헌)

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

### Step 5. 결과 저장
모델 평가 결과를 저장합니다.
```console
python show_result.py
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
