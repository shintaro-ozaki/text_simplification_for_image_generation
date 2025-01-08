#!/bin/bash

# missing_file.txt のパス
MISSING_FILE="scripts/missing_file.txt"

# ディレクトリのパス
TARGET_DIR="data/reference_caption"

# missing_file.txt が存在するか確認
if [[ ! -f "$MISSING_FILE" ]]; then
  echo "Error: $MISSING_FILE not found!"
  exit 1
fi

# missing_file.txt を1行ずつ読み込み
while IFS= read -r line; do
  # ファイルのパスを作成
  FILE_PATH="$TARGET_DIR/$line.txt"

  # ファイルが存在するか確認し、削除
  if [[ -f "$FILE_PATH" ]]; then
    rm "$FILE_PATH"
    echo "Deleted: $FILE_PATH"
  else
    echo "File not found: $FILE_PATH"
  fi
done <"$MISSING_FILE"
