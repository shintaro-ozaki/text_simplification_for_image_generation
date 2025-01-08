"""
openaiのbatch apiのフォーマットに変更する
"""
from pathlib import Path
import json

# フォーマットは下記のようになる
# {"custom_id": "request-1", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "gpt-4o-mini", "messages": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "What is 2+2?"}]}}

project_root = Path('/cl/home2/shintaro/text_simplification_for_image_generation')


def load_jsonl(file):
  with open(file, 'r') as f:
    return [json.loads(l) for l in f]


def save_jsonl(file, data):
  with open(file, 'w') as f:
    for d in data:
      f.write(json.dumps(d, ensure_ascii=False) + '\n')


SYSTEM_PROMPT = "You are a expert in summarization and you need to summarize the input text into 70 tokens without missing any information. Please start the summary with SummaryStart: and describe the summary of the text."


def make_prompt_for_summarization(caption_reference_description, entity, abstracts):
  prompt = f"""
Please generate a summary so that there are 180 tokens.
However, please do not delete proper nouns or other important information.
Please begin the output with SummaryStart: and write the summary of the text.
Please end the output with <SummaryEnd> as the last token.

Example:
SummaryStart: The summary of the text is as follows. The text is about the summary of the text. <SummaryEnd>

Caption: {caption_reference_description}

Complement:
"""
  for e, a in zip(entity, abstracts):
    prompt += f"* {e}: {a}\n"
  prompt += """
SummaryStart:
"""
  return prompt


def mak_batch_prompt_from_wit(data):
  output_datalist = []
  for i, line in enumerate(data):
    caption_reference_description = line['caption_reference_description']
    abstracts = line['entity_abstract']
    entity_in_caption = line['entity_in_caption']
    if len(abstracts) == 0 or len(entity_in_caption) == 0:
      continue
    user_prompt = make_prompt_for_summarization(caption_reference_description, entity_in_caption,
                                                abstracts)

    data_dict = {
        "custom_id": f"request-{i}",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model":
                "gpt-4o-mini",
            "messages": [{
                "role": "system",
                "content": SYSTEM_PROMPT
            }, {
                "role": "user",
                "content": user_prompt
            }]
        }
    }
    output_datalist.append(data_dict)
  return output_datalist


if __name__ == "__main__":
  wit_dir = project_root / 'data/wit'
  wit_file = wit_dir / 'en.wit.2k.prompt.jsonl'
  output_file = wit_dir / 'en.wit2k.batch.format.jsonl'
  data = load_jsonl(wit_file)
  responses = mak_batch_prompt_from_wit(data)
  save_jsonl(output_file, responses)
  print(f'Done! Saved to {output_file}')
