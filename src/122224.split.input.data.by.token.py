"""
witのinputをclipのtokenizerで分割してトークン数を測りそれによってデータを分割する
"""

from pathlib import Path
import json
from t5_tokenize import *
from clip_tokenize import *

project_root = Path('/cl/home2/shintaro/text_simplification_for_image_generation')


def load_jsonl(file):
  with open(file, "r") as f:
    return [json.loads(line) for line in f]


def save_jsonl(data, file):
  with open(file, "w") as f:
    for line in data:
      f.write(json.dumps(line, ensure_ascii=False) + "\n")


def split_data_by_token(data, t5_tokeninzer, clip_tokenizer):
  output_list = []
  for i, line in enumerate(data):
    text = line["caption_reference_description"]
    clip_count, clip_decoded_text = clip_tokenized_words(clip_tokenizer, text)
    if clip_count > 77:
      over_clip_text = text[len(clip_decoded_text):]
      t5_count, t5_decoded_text = t5_tokenized_words(t5_tokeninzer, over_clip_text)
      print(f"t5: {t5_count}")
      if t5_count > 256:
        print("t5 over 256")
    else:
      pass
      output_list.append(clip_count)

  # 平均, max, minを出力
  print(f"max: {max(output_list)}")
  print(f"min: {min(output_list)}")
  print(f"average: {sum(output_list) / len(output_list)}")


if __name__ == "__main__":
  t5_tokeninzer = initialize_t5_tokenizer("google-t5/t5-11b")
  clip_tokenizer = initialize_clip_tokenizer("openai/clip-vit-large-patch14")

  wit_data = load_jsonl(project_root / "data/wit/en.wit.2k.prompt.jsonl")

  split_data_by_token(wit_data, t5_tokeninzer, clip_tokenizer)
