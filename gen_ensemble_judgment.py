import os
import glob
import json
from tqdm import tqdm

def read_jsonl(file_path: str) -> list[dict]:
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():  # 빈 줄 무시
                data.append(json.loads(line))
    return data

def write_jsonl(file_path: str, data: list[dict]):
    with open(file_path, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(json.dumps(item) + "\n")

def get_data_index(data: dict, question_id: str) -> int: # get index of data by question_id
    for i, row in enumerate(data):
        if row['question_id'] == question_id:
            return i
    return None

def get_score(score: float) -> str:
    if score == 0:
        return 'A=B'
    elif 0 < score <= 1:
        return 'A>B'
    elif score > 1:
        return 'A>>B'
    elif -1 <= score < 0:
        return 'B>A'
    elif score < -1:
        return 'B>>A'
    else:
        raise ValueError('Invalid score')

if __name__ == "__main__":
    unique_model = None
    model_judgment_paths = glob.glob('./data/ko-arena-hard-v0.1/model_judgment/*')
    model_judgment_paths = [path for path in model_judgment_paths if 'ensemble' not in path]

    # get model list
    for model_judgment_path in model_judgment_paths:
        if unique_model is None:
            unique_model = set(
                os.path.basename(answer_name) for answer_name in glob.glob(f'{model_judgment_path}/*.jsonl')
            )
        else:
            unique_model = unique_model & set(
                os.path.basename(answer_name) for answer_name in glob.glob(f'{model_judgment_path}/*.jsonl')
            )

    score_dict = {
        "A=B": 0,
        "A>B": 1,
        "A>>B": 2,
        "B>A": -1,
        "B>>A": -2,
    }

    for model in tqdm(unique_model):
        model_result = []

        # load data
        judgment_datas = []
        for model_judgment_path in model_judgment_paths:
            judgment_datas.append(read_jsonl(model_judgment_path + f'/{model}'))

        # start ensemble judgment
        for i in range(len(judgment_datas[0])):
            # initialize result
            now_judgment = judgment_datas[0][i]
            question_id = now_judgment['question_id']
            result = {
                "question_id": question_id,
                "model": now_judgment['model'],
                "judge": 'ensemble',
                "games": []
            }

            # calculate score
            for game_index in range(len(now_judgment['games'])):
                total_score = 0
                num_error_answer = 0

                for data in judgment_datas:
                    data_row = data[get_data_index(data, question_id)]
                    score = data_row['games'][game_index]['score']

                    if score not in score_dict:
                        num_error_answer += 1
                        continue

                    total_score += score_dict[data_row['games'][game_index]['score']]
                result['games'].append(
                    {'score': get_score(total_score / (len(judgment_datas) - num_error_answer))}
                )
            model_result.append(result)
        # save result
        os.makedirs('./data/ko-arena-hard-v0.1/model_judgment/ensemble/', exist_ok=True)
        write_jsonl(f'./data/ko-arena-hard-v0.1/model_judgment/ensemble/{model}', model_result)