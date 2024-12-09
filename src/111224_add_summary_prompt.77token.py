from hf_model import *
import argparse
import json
from dotenv import load_dotenv
from pathlib import Path
import os
import torch
from loguru import logger

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
  return parser.parse_args()


def make_prompt_for_caption_reference_description_and_entity_summary(
    caption_reference_description, summary):
  prompt = f"""{summary}"""
  return prompt


def make_prompt_for_summarization(caption_reference_description, entity,
                                  abstracts):
  # caption_reference_descriptionのトークン数+entityのトークン数+abstractsのトークン数
  current_tokens = len(
      tokenizer(caption_reference_description,
                return_tensors="pt").input_ids[0]) + sum([
                    len(tokenizer(e, return_tensors="pt").input_ids[0]) +
                    len(tokenizer(a, return_tensors="pt").input_ids[0])
                    for e, a in zip(entity, abstracts)
                ])
  prompt = f"""
The current tokens are {current_tokens} tokens.
Please generate a summary so that there are 70 tokens.
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


#batch_sizeごとに入力する
def summarize(model, tokenizer, prompts, kwargs):
  input_ids = tokenizer(
      prompts,
      return_tensors="pt",
      truncation=True,
      padding=True,
  ).input_ids.to(device)  # CUDAを使用するためにデバイスを指定
  output = model.generate(input_ids, temperature=0.0, **kwargs)
  summaries = tokenizer.batch_decode(output, skip_special_tokens=True)
  return summaries


if __name__ == "__main__":
  args = parse_args()
  model_name = args.model
  quantize_type = args.quantize_type
  batch_size = args.batch_size
  max_new_tokens = args.max_new_tokens
  device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
  logger.info(f'Device: {device}')
  hf_token = os.getenv('HUGGINGFACE_TOKEN')
  kwargs = {
      "max_new_tokens": max_new_tokens,
      "do_sample": False,
  }
  model_suffix = model_name.split('/')[-1]
  flash_attn = False
  model, tokenizer = initialize_model(model_name, quantize_type, device,
                                      hf_token, flash_attn)
  wit_path = project_root / 'data' / 'wit' / 'en.wit.2k.prompt.jsonl'
  output_path = project_root / 'data' / 'wit' / f'en.wit.2k.prompt.summary.{model_suffix}.{max_new_tokens}.jsonl'
  logger.info(f'Output path: {output_path}')
  wit_data = load_jsonl(wit_path)
  datalist = []
  for i in range(0, len(wit_data), batch_size):
    logger.info(f'{i+1}/{len(wit_data)}')
    try:
      batch = wit_data[i:i + batch_size]
      prompts = []
      for line in batch:
        caption_reference_description = line['caption_reference_description']
        abstracts = line['entity_abstract']
        entity_in_caption = line['entity_in_caption']
        prompt_for_summary = make_prompt_for_summarization(
            caption_reference_description, entity_in_caption, abstracts)
        prompts.append(prompt_for_summary)
      summaries = summarize(model, tokenizer, prompts, kwargs)
      for line, summary in zip(batch, summaries):
        #TODO:  summaryをフィルタリングする必要がある
        # logger.info(f'{summary=}')
        # Summary: 以降を取得
        summary = summary.split('SummaryStart:')[2].strip()
        logger.info(f'Filtered: {summary=}')
        prompt4 = make_prompt_for_caption_reference_description_and_entity_summary(
            line['caption_reference_description'], summary)
        line['summary4'] = summary
        line['prompt4'] = prompt4
        datalist.append(line)
    except Exception as e:
      logger.error(f'Error: {e}')
  save_jsonl(datalist, output_path)
  logger.info(f'Saved to {output_path}')
