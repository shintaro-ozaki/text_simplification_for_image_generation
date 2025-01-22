from pathlib import Path
import json

project_root = Path('/cl/home2/shintaro/text_simplification_for_image_generation')


def load_jsonl(file_path):
  with open(file_path, 'r') as file:
    return [json.loads(line) for line in file]


def main():
  # /cl/home2/shintaro/text_simplification_for_image_generation/data/wit/en.wit.2k.prompt.jsonl
  # この中から、i行目のcaption_reference_descriptionを取得して、i.txtとして保存する。
  wit_data = load_jsonl(project_root / 'data/wit/en.wit.2k.prompt.jsonl')
  output_ref_dir = project_root / 'data/reference_caption'
  output_ref_dir.mkdir(exist_ok=True, parents=True)

  for i, data in enumerate(wit_data):
    print(f'Processing {i+1} / {len(wit_data)}')
    ref = data['caption_reference_description']
    with open(output_ref_dir / f'{i}.txt', 'w') as file:
      file.write(ref)
  print('Done')


if __name__ == '__main__':
  main()
