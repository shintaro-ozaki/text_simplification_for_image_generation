#!/bin/bash
#SBATCH -p lang_long
#SBATCH -c 16
#SBATCH -t 100:00:00
#SBATCH --account=lang
#SBATCH --job-name=delete-missing-file
#SBATCH -o logs/slurm-%x-%j.log

# 削除対象の番号が書かれた .txt ファイル
txt_file="scripts/missing_file.txt"

# 検索対象のディレクトリ
search_dir="generated_images"
ref_dir=wit_images_2k

# ファイルが存在するか確認
if [ ! -f "$txt_file" ]; then
    echo "Error: $txt_file が見つかりません。"
    exit 1
fi

# 削除処理
while read -r number; do
    # 空行をスキップ
    if [ -z "$number" ]; then
        continue
    fi

    # 該当する .png ファイルを検索して削除
    find "$search_dir" -type f -name "$number.png" -exec rm -v {} \;

    # ref_dirも削除
    find "$ref_dir" -type f -name "$number.png" -exec rm -v {} \;
    find "$ref_dir" -type f -name "$number.jpeg" -exec rm -v {} \;
    find "$ref_dir" -type f -name "$number.jpg" -exec rm -v {} \;
    
done < "$txt_file"
