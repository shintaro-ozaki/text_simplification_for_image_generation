"""
T5のtokenizerを読み込んで、入力データをトークン化してトークン数を数える
google-t5/t5-11b
"""

from transformers import T5Tokenizer
from dotenv import load_dotenv
import os

load_dotenv()


def initialize_t5_tokenizer(tokenizer_name):
  tokenizer = T5Tokenizer.from_pretrained(tokenizer_name)
  return tokenizer


def tokenize_by_t5_tokenizer(tokenizer, text):
  tokens = tokenizer(
      text,
      max_length=512,
      truncation=True,
      return_tensors="pt",
  )
  return tokens


def t5_tokenized_words(tokenizer, text):
  tokens = tokenize_by_t5_tokenizer(tokenizer, text)
  decoded_text = tokenizer.decode(tokens["input_ids"][0], skip_special_tokens=True)
  count_words = len(decoded_text.split())
  return count_words, decoded_text


if __name__ == "__main__":
  text = "This is an example sentence for tokenization."
  # T5-11B
  tokenizer_name = "google-t5/t5-11b"
  tokenizer = initialize_t5_tokenizer(tokenizer_name)
  count_words = t5_tokenized_words(tokenizer, text)
  print(count_words)
