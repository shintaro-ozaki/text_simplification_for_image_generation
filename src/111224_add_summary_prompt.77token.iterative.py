from hf_model import *
import argparse
import json
from dotenv import load_dotenv
from pathlib import Path
import os
import torch
from loguru import logger
from clip_tokenize import *

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
      f.write(json.dumps(d, ensure_ascii=False) + '\n')


def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('--model', type=str, required=True)
  parser.add_argument('--quantize_type', type=str)
  parser.add_argument('--batch_size', type=int, default=8)
  parser.add_argument('--max_new_tokens', type=int, default=512)
  parser.add_argument('--iterative', type=int)
  return parser.parse_args()


def word_count(text):
  return len(text.split())


def make_prompt_for_caption_reference_description_and_entity_summary(
    caption_reference_description, summary):
  prompt = f"""{summary}"""
  return prompt

"""
  text = "This is an example sentence for tokenization."
  # CLIP-L
  tokenizer_name = "openai/clip-vit-large-patch14"
  tokenizer = initialize_clip_tokenizer(tokenizer_name)
  count_words = clip_tokenized_words(tokenizer, text)
  print(count_words)
"""

def make_prompt_for_summarization(caption_reference_description, entity,
                                  abstracts, clip_tokenizer):
  current_words = clip_tokenized_words(clip_tokenizer, caption_reference_description)
  for e, a in zip(entity, abstracts):
    current_words += clip_tokenized_words(clip_tokenizer, e)
    current_words += clip_tokenized_words(clip_tokenizer, a)

  prompt = f"""
The current tokens are {current_words} tokens.
Please generate a summary so that there are 77 tokens.
However, please do not delete proper nouns or other important information.
Please begin the output with SummaryStart: and write the summary of the text.

Caption: {caption_reference_description}

Complement:
"""
  for e, a in zip(entity, abstracts):
    prompt += f"* {e}: {a}\n"
  prompt += """
SummaryStart:
"""
  return prompt


def iterative_prompt(summary, current_words):
  prompt = f"""
Once summarized, but it exceeds 77 tokens, please summarize again so that it is within 77 tokens.
Currently, the number of tokens is {current_words} tokens.
However, please do not delete proper nouns or other important information.
Please begin the output with SummaryStart: and write the summary of the text.

Input: {summary}

SummaryStart:
"""
  return prompt


def summarize(model, tokenizer, prompts, kwargs, iterative, clip_tokenizer):
  input_ids = tokenizer(
      prompts,
      return_tensors="pt",
      truncation=True,
      padding=True,
  ).input_ids.to(device)
  output = model.generate(input_ids, temperature=0.0, **kwargs)
  summaries = tokenizer.batch_decode(output, skip_special_tokens=True)
  summary = summaries[0].split('SummaryStart:')[2].strip()
  length_of_words = clip_tokenized_words(clip_tokenizer, summary)

  for i in range(iterative):
    logger.info(f'Iteration {i} / {iterative}, 単語の数: {length_of_words}')
    if length_of_words > 77:
      prompt = iterative_prompt(summary, length_of_words)
      input_ids = tokenizer(
          [prompt],
          return_tensors="pt",
          truncation=True,
          padding=True,
      ).input_ids.to(device)
      output = model.generate(input_ids, temperature=0.0, **kwargs)
      summary = tokenizer.decode(output[0], skip_special_tokens=True)
      summary = summary.split('SummaryStart:')[2].strip()
      length_of_words = clip_tokenized_words(clip_tokenizer, summary)
    else:
      logger.info(f'{i}回目で終了 / {iterative}, 単語の数: {length_of_words}')
      break
  return summary


if __name__ == "__main__":
  args = parse_args()
  model_name = args.model
  quantize_type = args.quantize_type
  batch_size = args.batch_size
  max_new_tokens = args.max_new_tokens
  iterative = args.iterative
  device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
  logger.info(f'Device: {device}')
  hf_token = os.getenv('HUGGINGFACE_TOKEN')
  clip_tokenizer_name = "openai/clip-vit-large-patch14"
  clip_tokenizer = initialize_clip_tokenizer(clip_tokenizer_name)
  kwargs = {
      "max_new_tokens": max_new_tokens,
      "do_sample": False,
  }
  model_suffix = model_name.split('/')[-1]
  flash_attn = False
  model, tokenizer = initialize_model(model_name, quantize_type, device,
                                      hf_token, flash_attn)
  wit_path = project_root / 'data' / 'wit' / 'en.wit.2k.prompt.jsonl'
  output_path = project_root / 'data' / 'wit' / f'en.wit.2k.prompt.summary.{model_suffix}.{max_new_tokens}.iterative{iterative}.jsonl'
  logger.info(f'Output path: {output_path}')
  wit_data = load_jsonl(wit_path)
  datalist = []
  for i, line in enumerate(wit_data):
    logger.info(f'Iteration {i} / {len(wit_data)}')
    try:
      caption_reference_description = line['caption_reference_description']
      abstracts = line['entity_abstract']
      entity_in_caption = line['entity_in_caption']
      prompt_for_summary = make_prompt_for_summarization(
          caption_reference_description, entity_in_caption, abstracts, clip_tokenizer)
      summary = summarize(model, tokenizer, [prompt_for_summary], kwargs,
                          iterative, clip_tokenizer)
      logger.info(f'Filtered: {summary=}')
      prompt5 = make_prompt_for_caption_reference_description_and_entity_summary(
          line['caption_reference_description'], summary)
      line['summary5'] = summary
      line['prompt5'] = prompt5
      datalist.append(line)
    except Exception as e:
      logger.error(f'Error: {e} at line: {line}')
  save_jsonl(datalist, output_path)
  logger.info(f'Saved to {output_path}')
