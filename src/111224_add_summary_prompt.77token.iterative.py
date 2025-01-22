from hf_model import *
import argparse
import json
from dotenv import load_dotenv
from pathlib import Path
import os
import torch
from loguru import logger
from t5_tokenize import *

torch.manual_seed(0)
from dotenv import load_dotenv
load_dotenv()
project_root = Path('/cl/home2/shintaro/text_simplification_for_image_generation')


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
  parser.add_argument('--iterative', type=int, required=True)
  return parser.parse_args()


def make_prompt_for_caption_reference_description_and_entity_summary(caption_reference_description,
                                                                     summary):
  prompt = f"""
Caption: {caption_reference_description}

Note: {summary}"""
  return prompt


def make_iterative_prompt_for_summarization(summary, t5_tokenizer):
  current_words, _ = t5_tokenized_words(t5_tokenizer, summary)
  prompt = f"""
The current tokens are still {current_words} tokens.
Please generate a summary so that there are 180 tokens.
However, please do not delete proper nouns or other important information.
Please begin the output with SummaryStart: and write the summary of the text.
Please end the output with <SummaryEnd> as the last token.

Example:
SummaryStart: The summary of the text is as follows. The text is about the summary of the text. <SummaryEnd>

Note: {summary}

SummaryStart:
"""
  return prompt


def make_prompt_for_summarization(caption_reference_description, entity, abstracts, t5_tokenizer):
  current_words, _ = t5_tokenized_words(t5_tokenizer, caption_reference_description)
  for e, a in zip(entity, abstracts):
    e_words, _ = t5_tokenized_words(t5_tokenizer, e)
    a_words, _ = t5_tokenized_words(t5_tokenizer, a)
  current_words += e_words + a_words

  prompt = f"""
The current tokens are {current_words} tokens.
Please generate a summary so that there are 180 tokens.
However, please do not delete proper nouns or other important information.
Please begin the output with SummaryStart: and write the summary of the text.
Please end the output with <SummaryEnd> as the last token.

Example:
SummaryStart: The summary of the text is as follows. The text is about the summary of the text. <SummaryEnd>

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
  t5_tokenizer_name = "google-t5/t5-11b"
  t5_tokenizer = initialize_t5_tokenizer(t5_tokenizer_name)
  kwargs = {
      "max_new_tokens": max_new_tokens,
      "do_sample": False,
  }
  model_suffix = model_name.split('/')[-1]
  flash_attn = False
  model, tokenizer = initialize_model(model_name, quantize_type, device, hf_token, flash_attn)
  wit_path = project_root / 'data' / 'wit' / 'en.wit.2k.prompt.jsonl'
  output_path = project_root / 'data' / 'wit' / f'en.wit.2k.prompt.summary.{model_suffix}.{max_new_tokens}.iterative{args.iterative}.jsonl'
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
        prompt_for_summary = make_prompt_for_summarization(caption_reference_description,
                                                           entity_in_caption, abstracts,
                                                           t5_tokenizer)
        prompts.append(prompt_for_summary)
      summaries = summarize(model, tokenizer, prompts, kwargs)
      for line, summary in zip(batch, summaries):
        summary = summary.split('SummaryStart:')[3].strip()
        summary = summary.split('<SummaryEnd>')[0].strip()
        logger.info(f'Filtered: {summary=}')
        # さらにsummaryが256トークン以上であれば、再度要約を行う (iterativeの回数だけ)
        for _ in range(args.iterative):
          current_words, _ = t5_tokenized_words(t5_tokenizer, summary)
          if current_words <= 180:
            break
          prompt = make_iterative_prompt_for_summarization(summary, t5_tokenizer)
          summary = summarize(model, tokenizer, prompt, kwargs)
          summary = summary.split('SummaryStart:')[3].strip()
          summary = summary.split('<SummaryEnd>')[0].strip()
        prompt5 = make_prompt_for_caption_reference_description_and_entity_summary(
            line['caption_reference_description'], summary)
        line['summary5'] = summary
        line['prompt5'] = prompt5
        datalist.append(line)
    except Exception as e:
      logger.error(f'Error: {e}')
  save_jsonl(datalist, output_path)
  logger.info(f'Saved to {output_path}')
