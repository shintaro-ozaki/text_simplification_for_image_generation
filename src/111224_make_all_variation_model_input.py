from wikiapi import *
import json
from pathlib import Path
from urllib.parse import quote

project_root = Path(
    '/cl/home2/shintaro/text_simplification_for_image_generation')


def load_jsonl(file_path):
  with open(file_path, 'r') as f:
    return [json.loads(l) for l in f]


def save_jsonl(data, file_path):
  with open(file_path, 'w') as f:
    for d in data:
      f.write(json.dumps(d) + '\n')


logging.basicConfig(
    format="| %(asctime)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level="INFO",
    stream=sys.stdout,
)
logger: logging.Logger = logging.getLogger(__name__)


def make_prompt_for_only_caption_reference_description(
    caption_reference_description):
  prompt = f"""
Please generate an image using the following information.

Caption: {caption_reference_description}
"""
  return prompt


def make_prompt_for_caption_reference_description_and_entity(
    caption_reference_description, entity, abstract):
  prompt = f"""
Please generate an image using the following information.

Caption: {caption_reference_description}

Complement:
"""
  for e, a in zip(entity, abstract):
    prompt += f"* {e}: {a}\n"
  return prompt


def make_prompt_for_caption_reference_description_and_entity_summary(summary):
  prompt = f"""
Please generate an image using the following information.

Caption: {summary}
"""
  return prompt


def get_abstract_of_entities(entities):
  """caption内に存在するentityのabstractを取得する"""
  abstracts = []
  entities = [entity for entity in entities if entity != ' ']
  for entity in entities:
    # entity = entity.replace(' ', '_')
    entitiy = quote(entity)
    pageid = get_pageid_from_title(entity)
    if pageid is None:
      continue
    sections, entities = get_full_page_content(pageid)
    wikitext = get_page_wikitext(pageid)
    wiki_text_entities = extract_hyperlinked_entities(wikitext)
    combined_entities = list(set(entities + wiki_text_entities))
    # sectionsの中からabstractを取得
    abstract = sections.get('abstract', '')
    abstracts.append(abstract)
  return abstracts


def make_all_variation_model_input(wit_data, output_path):
  """
  * caption_reference_description
  * caption_reference_description+entity
  * (caption_reference_description+entity) -> summary
  """
  datalist = []
  for i, line in enumerate(wit_data):
    logger.info(f'{i+1}/{len(wit_data)}')
    try:
      caption_reference_description = line['caption_reference_description']
      title = quote(line['page_title'])
      pageid = get_pageid_from_title(title)
      if pageid is None:
        continue
      sections, entities = get_full_page_content(pageid)
      wikitext = get_page_wikitext(pageid)
      wiki_text_entities = extract_hyperlinked_entities(wikitext)
      combined_entities = list(set(entities + wiki_text_entities))

      entity_in_caption: list[str] = [
          entity for entity in combined_entities
          if entity in caption_reference_description
      ]
      abstracts: list[str] = get_abstract_of_entities(entity_in_caption)

      if len(entity_in_caption) == 0 or len(abstracts) == 0:
        continue

      line['pageid'] = pageid
      line['entity_abstract'] = abstracts
      line['entity_in_caption'] = entity_in_caption

      prompt1 = make_prompt_for_only_caption_reference_description(
          caption_reference_description)
      prompt2 = make_prompt_for_caption_reference_description_and_entity(
          caption_reference_description, entity_in_caption, abstracts)
      line['prompt1'] = prompt1
      line['prompt2'] = prompt2
      datalist.append(line)
    except Exception as e:
      # raise e
      logger.info(e)
      continue
  save_jsonl(datalist, output_path)


if __name__ == "__main__":
  wit_path = project_root / 'data' / 'wit' / 'en.wit.2k.jsonl'
  output_path = project_root / 'data' / 'wit' / 'en.wit.2k.prompt.updated.jsonl'
  wit_data = load_jsonl(wit_path)
  make_all_variation_model_input(wit_data, output_path)
