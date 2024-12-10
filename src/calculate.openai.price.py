from pathlib import Path
import json
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
project_root = Path('/cl/home2/shintaro/text_simplification_for_image_generation')

client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY"),
)

def execute(system_prompt, user_prompt):
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.0,
        top_p=0.0,
        seed=0,
        n=1,
        max_tokens=150,
    )
    assert response.choices[0].finish_reason == 'stop'
    return response

def load_jsonl(file):
    with open(file, "r") as f:
        return [json.loads(line) for line in f]

if __name__ == "__main__":
    # /cl/home2/shintaro/text_simplification_for_image_generation/data/wit/batch.format.wit2k.jsonl
    wit_file = project_root / 'data/wit/batch.format.wit2k.jsonl'
    print(f'Loading data....')
    data = load_jsonl(wit_file)
    data.sort(key=lambda x: len(x['body']['messages'][1]['content']), reverse=True)
    print(f'Loaded {len(data)} data')

    # avgのlengthを計算
    total_length = 0
    for d in data:
        total_length += len(d['body']['messages'][1]['content'])
    avg_length = total_length / len(data)
    print(f'avg_length: {avg_length}')

    fee = 0
    for i, d in enumerate(data):
        if i < 10:
            response = execute(d['body']['messages'][0]['content'], d['body']['messages'][1]['content'])
            completion_tokens = response.usage.completion_tokens
            prompt_tokens = response.usage.prompt_tokens
            fee = (0.00015 * prompt_tokens / 1000 + 0.0006 * completion_tokens / 1000)
            # batchなので半分にする
            fee = fee / 2
        else:
            break
    print(f'total: ${fee} / ￥{fee*150}')
    # total: $0.005307899999999999 / ￥0.7961849999999998 : 10件で
    # batch total : $0.0026539499999999996 / ￥0.3980924999999999 : 10件で
    # 10件で0.002ドル, 5000件で
