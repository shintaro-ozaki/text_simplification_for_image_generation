#!/bin/bash

# チェック対象のディレクトリ
dir=generated_images/pattern3/dreamlike-photoreal-2.0/Phi-3.5-mini-instruct.512

# ファイル番号の範囲
start=1
end=2652

# 存在しない番号を確認
for i in $(seq $start $end); do
  # ファイルの存在確認
  if ! [ -e "$dir/$i.png" ] && ! [ -e "$dir/$i.jpg" ] && ! [ -e "$dir/$i.jpeg" ]; then
    echo "$i"
  fi
done
