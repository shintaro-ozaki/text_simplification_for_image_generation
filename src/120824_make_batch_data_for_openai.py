import csv
import json
from pathlib import Path
"""
{"custom_id": "request-1", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "gpt-3.5-turbo-0125", "messages": [{"role": "system", "content": "You are a helpful assistant."},{"role": "user", "content": "Hello world!"}],"max_tokens": 1000}}
{"custom_id": "request-2", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "gpt-3.5-turbo-0125", "messages": [{"role": "system", "content": "You are an unhelpful assistant."},{"role": "user", "content": "Hello world!"}],"max_tokens": 1000}}
"""

from hf_model import *
import argparse
import json
from dotenv import load_dotenv
from pathlib import Path
import os
import torch

torch.manual_seed(0)
load_dotenv()
project_root = Path(
    '/cl/home2/shintaro/text_simplification_for_image_generation')


def load_jsonl(file_path):
  with open(file_path, 'r') as f:
    return [json.loads(l) for l in f]


def save_jsonl(data, file_path):
  with open(file_path, 'w') as f:
    for d in data:
      f.write(json.dumps(d) + '\n')


def make_prompt_for_summarization(caption_reference_description, entity,
                                  abstracts):
  prompt = f"""
Please summarize the following text and make the optimal prompt for the image generation.
Please make the prompt as simple as possible, not hitting the 100 tokens limit.
Begin the output with SummaryStart: and write the summary of the text.

Caption: {caption_reference_description}

Complement:
"""
  for e, a in zip(entity, abstracts):
    prompt += f"* {e}: {a}\n"
  prompt += """
SummaryStart:
"""
  return prompt


if __name__ == "__main__":
  model_name = 'gpt-4o-mini'
  wit_path = project_root / 'data' / 'wit' / 'en.wit.2k.prompt.jsonl'
  output_path = project_root / 'data' / 'wit' / 'en.wit.2k.batch.input.jsonl'
  wit_data = load_jsonl(wit_path)
  openai_datalist = []

  for i, line in enumerate(wit_data):
    print(f'Processing {i} / {len(wit_data)}')
    caption_reference_description = line['caption_reference_description']
    abstracts = line['entity_abstract']
    entity_in_caption = line['entity_in_caption']
    prompt_for_summary = make_prompt_for_summarization(
        caption_reference_description, entity_in_caption, abstracts)
    max_tokens = 300

    openai_data = {
        "custom_id": f"request-{i}",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": model_name,
            "messages": [{
                "role":
                    "system",
                "content":
                    "You are a summary expert, please respond appropriately to the prompt entered below. "
            }, {
                "role": "user",
                "content": prompt_for_summary
            }],
            "max_tokens": max_tokens
        }
    }
    openai_datalist.append(openai_data)
  save_jsonl(openai_datalist, output_path)
  print(f'Saved to {output_path}')
