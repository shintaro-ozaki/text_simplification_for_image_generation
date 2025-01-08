"""
WITからデータセットを作成する
https://huggingface.co/datasets/google/wit

今回は英語だけで行う。
データセットのサイズを小さくする。

google/wit
"""

from datasets import load_dataset
import json
from pathlib import Path

project_root = Path('/cl/home2/shintaro/text_simplification_for_image_generation')


def load_wit_dataset():
  dataset = load_dataset("google/wit", "en", trust_remote_code=True)
  return dataset


def save_to_jsonl(dataset, save_path):
  with open(save_path, "w") as f:
    for data in dataset:
      f.write(json.dumps(data) + "\n")


def download_from_hf_to_jsonl():
  dataset = load_wit_dataset()
  save_to_jsonl(dataset["train"], project_root / "data/wit/wit.raw.train.jsonl")
  # WITはtrainしかない


if __name__ == "__main__":
  download_from_hf_to_jsonl()
