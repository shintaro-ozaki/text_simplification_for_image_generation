#!/bin/bash

# チェック対象のディレクトリ
dir="generated_images/pattern5/IF-I-L-v1.0/Qwen2.5-72B-Instruct.180.iterative3"

# ファイル番号の範囲
start=1
end=2653

# 存在しない番号を確認
for i in $(seq $start $end); do
  # ファイルの存在確認
  if ! [ -e "$dir/$i.png" ] && ! [ -e "$dir/$i.jpg" ] && ! [ -e "$dir/$i.jpeg" ]; then
    echo "$i"
  fi
done
