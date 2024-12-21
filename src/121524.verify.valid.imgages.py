import os
from PIL import Image
from pathlib import Path

# /cl/home2/shintaro/text_simplification_for_image_generation/wit_images_2k
project_root = Path(
    '/cl/home2/shintaro/text_simplification_for_image_generation')


def check_images_in_directory(directory):
  supported_extensions = ('.png', '.jpg', '.jpeg')
  files = [
      f for f in os.listdir(directory)
      if f.lower().endswith(supported_extensions)
  ]
  results = {}

  for i, file in enumerate(files):
    file_path = os.path.join(directory, file)
    try:
      with Image.open(file_path) as img:
        img.verify()  # ファイルが有効な画像かどうかを確認
      results[file] = "Valid"
    except Exception as e:
      results[file] = f"Invalid ({str(e)})"
      # そのファイルを削除
      os.remove(file_path)
  return results


# 使用例
directory_path = project_root / 'wit_images_2k'
results = check_images_in_directory(directory_path)

overall_count = len(results)
invalid_count = 0
for file, status in results.items():
  if status != "Valid":
    print(f"{file}: {status}")
    invalid_count += 1

print()
print(f"Overall: {overall_count}")
print(f"Invalid: {invalid_count}")
print(f'Valid: {overall_count - invalid_count}')
