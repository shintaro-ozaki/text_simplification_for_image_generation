"""
英語のinfoboxに関するページを取得する。
"""
import logging
import sys
import argparse
import os
from pathlib import Path
import requests
import time
from datetime import datetime, timedelta
from urllib.parse import quote
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from bs4 import BeautifulSoup
from urllib.parse import quote
import re
from tqdm import tqdm

# 英語のWikipeidaのAPI URL
project_root = '/cl/home2/shintaro/llm_exp_wiki_multilingual_instruct'
WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"
########################################################
"""
英語のWikipediaページの情報を取得する。
取得にはテンプレート(例: "Template:Infobox artwork")を使用する。
テンプレートを使用しているページを取得し、各ページの情報を取得する。

Caution:
英語以外を使用する場合は、WIKIPEDIA_API_URLを変更する必要がある。
WIKIPEDIA_API_URL = f"https://{lang}.wikipedia.org/w/api.php"
"""


def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument("--infobox", type=str, required=True)
  return parser.parse_args()


logging.basicConfig(
    format="| %(asctime)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level="INFO",
    stream=sys.stdout,
)
logger: logging.Logger = logging.getLogger(__name__)


def save_to_json(data, file_name):
  """データをJSONファイルに保存する。"""
  os.makedirs(os.path.dirname(file_name), exist_ok=True)
  with open(file_name, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)


def save_to_jsonl(data, file_name):
  """データをJSONL形式のファイルに保存する。"""
  file_name.parent.mkdir(parents=True, exist_ok=True)
  with open(file_name, 'w', encoding='utf-8') as f:
    for line in data:
      f.write(json.dumps(line, ensure_ascii=False) + '\n')


def extract_entities(content, links, redirects):
  """コンテンツ内のリンクとリダイレクト情報を使用してエンティティを抽出する。"""
  entities = []
  for title, anchor_text in links.items():
    if anchor_text in content:
      redirected_title = redirects.get(title, title)
      entities.append(redirected_title)
  return entities


def _ensure_dict_structure(sections, current_section, current_subsection):
  """セクションの辞書構造を確保する。"""
  if current_section not in sections:
    sections[current_section] = {}
  if isinstance(sections[current_section], str):
    sections[current_section] = {'': sections[current_section]}
  if current_subsection and current_subsection not in sections[current_section]:
    sections[current_section][current_subsection] = {'': ''}


def extract_hyperlinked_entities(wikitext):
  """ウィキテキストからハイパーリンクされたエンティティを抽出する。"""
  pattern = r"\[\[(.*?)\]\]"
  entities = []
  for match in re.findall(pattern, wikitext):
    entities.extend(match.split('|'))
  return entities


def process_sections(content):
  """コンテンツをセクションごとに分割して整理する。"""
  sections = {}
  current_section = "abstract"
  current_subsection = None
  current_subsubsection = None
  sections[current_section] = ""

  for line in content.split('\n'):
    try:
      if line.startswith("===="):
        current_subsubsection = line.strip("=").strip()
        _ensure_dict_structure(sections, current_section, current_subsection)
        if current_subsubsection not in sections[current_section][
            current_subsection]:
          sections[current_section][current_subsection][
              current_subsubsection] = ""
        line = re.sub(r'===.*?===', '', line).replace('\n', '')
        sections[current_section][current_subsection][
            current_subsubsection] += line + '\n'

      elif line.startswith("==="):
        current_subsubsection = None
        current_subsection = line.strip("=").strip()
        _ensure_dict_structure(sections, current_section, current_subsection)
        if '' not in sections[current_section][current_subsection]:
          sections[current_section][current_subsection][''] = ""
        line = re.sub(r'===.*?===', '', line).replace('\n', '')
        sections[current_section][current_subsection][''] += line + '\n'

      elif line.startswith("=="):
        current_subsubsection = None
        current_subsection = None
        current_section = line.strip("=").strip()
        _ensure_dict_structure(sections, current_section, None)
        if '' not in sections[current_section]:
          sections[current_section][''] = ""
        line = re.sub(r'==.*?==', '', line).replace('\n', '')
        sections[current_section][''] += line + '\n'

      else:
        if isinstance(sections[current_section], dict):
          if current_subsection and isinstance(
              sections[current_section][current_subsection], dict):
            if current_subsubsection:
              sections[current_section][current_subsection][
                  current_subsubsection] += line + '\n'
            else:
              if '' not in sections[current_section][current_subsection]:
                sections[current_section][current_subsection][''] = ""
              sections[current_section][current_subsection][''] += line + '\n'
          else:
            if '' not in sections[current_section]:
              sections[current_section][''] = ""
            sections[current_section][''] += line + '\n'
        else:
          sections[current_section] += line + '\n'
    except Exception as e:
      logger.info(f"Error processing line: {e}")
      continue
  return sections


def get_redirects_for_links(links):
  """リンクのリダイレクト情報を取得する。"""
  session = requests.Session()
  redirects = {}
  for i in range(0, len(links), 20):
    chunk = links[i:i + 20]
    titles = "|".join([link['title'] for link in chunk])
    params = {
        "action": "query",
        "format": "json",
        "titles": titles,
        "redirects": 1
    }

    try:
      response = session.get(WIKIPEDIA_API_URL, params=params)
      if response.status_code != 200:
        print(f"Error: HTTP status code {response.status_code}")
        continue

      try:
        data = response.json()
        if 'query' in data:
          chunk_redirects = {
              redir['from']: redir['to']
              for redir in data['query'].get('redirects', [])
          }
          redirects.update(chunk_redirects)
      except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        print(f"Response content: {response.text}")
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(f"Error retrieving redirects: {e}")

  return redirects


def get_page_wikitext(page_id):
  """指定されたページIDのウィキテキストを取得する。"""
  session = requests.Session()
  params = {
      "action": "query",
      "prop": "revisions",
      "rvprop": "content",
      "rvslots": "*",
      "pageids": page_id,
      "format": "json"
  }
  # try:
  response = session.get(WIKIPEDIA_API_URL, params=params)
  data = response.json()
  page = data["query"]["pages"][str(page_id)]
  # print(page)
  wikitext = page["revisions"][0]["slots"]["main"]["*"]
  return wikitext
  # except (ConnectionError, Timeout, TooManyRedirects) as e:
  #   print(f"Error retrieving wikitext for page ID {page_id}: {e}")
  #   return ""


def extract_links_with_anchor_text(page_id):
  """指定されたページIDのリンクとアンカーテキストを抽出する。"""
  session = requests.Session()
  params = {
      "action": "query",
      "prop": "links",
      "pageids": page_id,
      "format": "json",
      "pllimit": "max"
  }

  try:
    response = session.get(WIKIPEDIA_API_URL, params=params)
    data = response.json()
    page = data["query"]["pages"][str(page_id)]
    links = page.get("links", [])
    return {
        link['title']: link.get('anchor_text', link['title']) for link in links
    }
  except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(f"Error retrieving links: {e}")
    return {}


def get_image_url_from_wikipedia(title):
  """Wikipediaページのタイトルから画像URLを取得する。"""
  if title == "_":
    return None
  page_url = f"https://en.wikipedia.org/wiki/{quote(title)}"
  try:
    response = requests.get(
        page_url, headers={"User-Agent": "Shintaro Ozaki (ee207060@gmail.com)"})
    soup = BeautifulSoup(response.content, "html.parser")

    # infoboxに画像がある場合は、table.infoboxを探す
    infobox_image = soup.find("table", class_="infobox")
    if infobox_image:
      img_tag = infobox_image.find("img")
      if img_tag:
        return "https:" + img_tag["src"]

    # infoboxに画像がない場合は、div.infoboxを探す
    infobox_div_image = soup.find("div", class_="infobox")
    if infobox_div_image:
      img_tag = infobox_div_image.find("img")
      if img_tag:
        return "https:" + img_tag["src"]

    # 画像がinfoboxにない場合は、ページ内の最初の画像を取得する
    figure_image = soup.find("figure", class_="mw-default-size")
    if figure_image:
      img_tag = figure_image.find("img")
      if img_tag:
        return "https:" + img_tag["src"]
    return None

  except Exception as e:
    logger.info(f"Error processing title '{title}': {e}")
    return None


def get_full_page_content(page_id):
  """指定されたページIDの全文を取得し、エンティティを抽出する。"""
  session = requests.Session()
  params = {
      "action": "query",
      "prop": "extracts|links",
      "pageids": page_id,
      "format": "json",
      "explaintext": True,
      "pllimit": "max"
  }
  try:
    response = session.get(WIKIPEDIA_API_URL, params=params)
    data = response.json()
    page = data["query"]["pages"][str(page_id)]
    content = page.get("extract", "")
    links = page.get("links", [])

    redirects = get_redirects_for_links(links)
    links_with_anchor = extract_links_with_anchor_text(page_id)
    entities = extract_entities(content, links_with_anchor, redirects)

    sections = process_sections(content)
    return sections, entities
  except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(f"Error retrieving content for page ID {page_id}: {e}")
    return {}, []


def get_page_url_from_page_id(page_id):
  """指定されたページIDのURLを取得する。"""
  session = requests.Session()
  params = {
      "action": "query",
      "prop": "info",
      "pageids": page_id,
      "inprop": "url",
      "format": "json"
  }
  try:
    response = session.get(WIKIPEDIA_API_URL, params=params)
    data = response.json()
    page = data["query"]["pages"][str(page_id)]
    return page["fullurl"]
  except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(f"Error retrieving URL for page ID {page_id}: {e}")
    return None


def get_embedded_pages(eititle, eilimit=20):
  """指定されたテンプレートを使用しているページを取得する。"""
  session = requests.Session()
  params = {
      "action": "query",
      "format": "json",
      "list": "embeddedin",
      "eititle": eititle,
      "eilimit": eilimit
  }
  ei_continue = {}
  pages: list[dict] = []
  while True:
    try:
      response = session.get(
          WIKIPEDIA_API_URL, params={
              **params,
              **ei_continue
          })
      data = response.json()
      for page in data.get("query", {}).get("embeddedin", []):
        title = page["title"]
        if "User:" not in title and "/sandbox" not in title:
          pages.append(page)
      if "continue" not in data:
        break
      ei_continue = data["continue"]
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      logger.info(f"Request error: {e}")
      break
  return pages


def get_pageid_from_title(title):
  """タイトルからページIDを取得する。"""
  session = requests.Session()
  params = {"action": "query", "format": "json", "titles": title}
  try:
    response = session.get(WIKIPEDIA_API_URL, params=params)
    data = response.json()
    page = data["query"]["pages"]
    page_id = list(page.keys())[0]
    return page_id
  except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(f"Error retrieving page ID for title {title}: {e}")
    return None


def get_infobox_page(infobox):
  articles_path = Path("data/articles")
  template_articles_path = articles_path / infobox.replace(
      "Template:", "").strip().replace(" ", "_")
  template_articles_path.mkdir(parents=True, exist_ok=True)
  embedded_pages = get_embedded_pages(infobox, eilimit=500)
  all_pages = embedded_pages
  logger.info(f"Total pages found: {len(embedded_pages)} about {infobox}")
  save_file_name = template_articles_path / f"en.{template_articles_path.name}.jsonl"
  logger.info(f"Save file is {project_root / save_file_name}")

  all_article_data = []
  for i, page in tqdm(enumerate(all_pages)):
    try:
      logger.info(f"Processing: {i+1}/{len(all_pages)}")
      page_id = page["pageid"]

      page_url = get_page_url_from_page_id(page_id)
      title = page["title"].replace('/', '_').replace(':', '_')
      image_url = get_image_url_from_wikipedia(title)

      sections, entities = get_full_page_content(page_id)
      wikitext = get_page_wikitext(page_id)
      wiki_text_entities = extract_hyperlinked_entities(wikitext)
      combined_entities = list(set(entities + wiki_text_entities))

      article_data = {
          "title": title,
          "pageid": page_id,
          "page_url": page_url,
          "image_url": image_url,
          "content": sections,
          "entities": combined_entities
      }
      all_article_data.append(article_data)
      logger.info(
          f"Saved article data for {title} in {project_root / save_file_name}")
      time.sleep(1)
    except Exception as e:
      logger.info(f"Error processing page: {e}")
      continue

  save_to_jsonl(all_article_data, save_file_name)
  logger.info("All articles data processing completed.")
  logger.info(f"Saved all articles data in {project_root / save_file_name}")


if __name__ == "__main__":
  args = parse_args()
  get_infobox_page(args.infobox)
