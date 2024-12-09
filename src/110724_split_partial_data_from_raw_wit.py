"""
witのrawデータを分割して、使用する分だけ取り出す
取り出したところからモデルの入力まで持っていく

WITは37046386 行
"""

from pathlib import Path
import json
import random

project_root = Path(
    '/cl/home2/shintaro/text_simplification_for_image_generation/')


def load_jsonl(file_path):
  with open(file_path, 'r') as f:
    return [json.loads(line) for line in f]


def save_jsonl(file_path, data):
  with open(file_path, 'w') as f:
    for line in data:
      f.write(json.dumps(line) + '\n')


def split_partial_data_from_raw_wit():
  raw_wit_path = project_root / 'data/wit/wit.raw.train.jsonl'
  raw_wit = load_jsonl(raw_wit_path)

  filtered_wit = []
  for i, line in enumerate(raw_wit):
    print(f'line: {i} / {len(raw_wit)}')
    # 英語だけを抽出
    if line["language"] == "en":
      # section_title, context_section_description がnullのものは除外
      if line["section_title"] is None or line[
          "context_section_description"] is None:
        continue
      filtered_wit.append(line)

  # filtered_witを分割する
  en_wit_all_file = project_root / 'data/wit/en.wit.all.jsonl'
  save_jsonl(en_wit_all_file, filtered_wit)
  # そこから3k行を取り出す
  random.seed(0)
  random.shuffle(filtered_wit)
  filtered_wit_2k = filtered_wit[:5000]
  en_wit_2k_file = project_root / 'data/wit/en.wit.2k.jsonl'
  save_jsonl(en_wit_2k_file, filtered_wit_2k)
  print(f'saved en all: {en_wit_all_file}')
  print(f'saved en 2k: {en_wit_2k_file}')


if __name__ == '__main__':
  split_partial_data_from_raw_wit()
