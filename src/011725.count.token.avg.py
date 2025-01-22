# CLIPのtokenizerを用いてトークン数の平均を計算する

from pathlib import Path
import json
from clip_tokenize import *

def load_jsonl(file):
  with open(file, 'r') as f:
    return [json.loads(line) for line in f]


project_root = Path('/cl/home2/shintaro/text_simplification_for_image_generation')
clip_tokenizer_name = "openai/clip-vit-large-patch14"

tokenizer = initialize_clip_tokenizer(clip_tokenizer_name)

model_list = [
  "Qwen/Qwen2.5-72B-Instruct",
  "microsoft/Phi-3.5-mini-instruct",
  "meta-llama/Llama-3.1-8B-Instruct",
  "meta-llama/Llama-3.1-70B-Instruct",
  "meta-llama/Llama-3.3-70B-Instruct",
]
pattern_list = [3, 4, 5]

# pattern1
# /cl/home2/shintaro/text_simplification_for_image_generation/data/wit/en.wit.2k.prompt.jsonl
pattern_1_2_data = load_jsonl(project_root / 'data/wit/en.wit.2k.prompt.jsonl')
pattern1_token_counts = []
pattern2_token_counts = []
for line in pattern_1_2_data:
  pattern1_prompt = line['prompt1']
  pattern2_prompt = line['prompt2']
  pattern1_token, _ = clip_tokenized_words(tokenizer, pattern1_prompt)
  pattern2_token, _ = clip_tokenized_words(tokenizer, pattern2_prompt)
  pattern1_token_counts.append(pattern1_token)
  pattern2_token_counts.append(pattern2_token)

# avg
pattern1_avg = sum(pattern1_token_counts) / len(pattern1_token_counts)
pattern2_avg = sum(pattern2_token_counts) / len(pattern2_token_counts)

print(f'pattern1_avg: {pattern1_avg}')
print(f'pattern2_avg: {pattern2_avg}')

for pattern in pattern_list:
  # 3,4,5について
  pattern_tokens = []
  for model in model_list:
    model_suffix_name = model.split('/')[-1]
    # en.wit.2k.prompt.summary.Llama-3.1-8B-Instruct.180.jsonl
    if pattern == 3:
      file_name = f'en.wit.2k.prompt.summary.{model_suffix_name}.512.jsonl'
    elif pattern == 4:
      file_name = f'en.wit.2k.prompt.summary.{model_suffix_name}.180.jsonl'
    elif pattern == 5:
      file_name = f'en.wit.2k.prompt.summary.{model_suffix_name}.180.iterative3.jsonl' 
    else:
      raise ValueError('pattern is invalid')
    data = load_jsonl(project_root / 'data/wit' / file_name)
    token_counts = []
    for line in data:
      prompt = line[f'summary{pattern}']
      token, _ = clip_tokenized_words(tokenizer, prompt)
      token_counts.append(token)
    avg = sum(token_counts) / len(token_counts)
    pattern_tokens.append(avg)
  print(f'pattern{pattern}_avg: {sum(pattern_tokens) / len(pattern_tokens)}')
