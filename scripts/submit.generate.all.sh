#!/bin/bash
#SBATCH -p lang_long
#SBATCH -c 2
#SBATCH -t 100:00:00
#SBATCH --account=lang
#SBATCH --job-name=submit

# sbatch scripts/120924.deep.floyd.prompt.1.sh
# sbatch scripts/120924.deep.floyd.prompt.2.sh
# sbatch scripts/120924.dreamlike.prompt.1.sh
# sbatch scripts/120924.dreamlike.prompt.2.sh
# sbatch scripts/120924.stable.diffusion.prompt.1.sh
# sbatch scripts/120924.stable.diffusion.prompt.2.sh
# sbatch scripts/120924.flux.prompt.1.sh
# sbatch scripts/120924.flux.prompt.2.sh

# 監視するジョブIDのリスト
# job_ids=(221851 221854 221845 221849 222045 222043)

# # すべてのジョブが終了するまで待機
# while true; do
#     running_jobs=$(squeue -u $USER --noheader --format="%A" | grep -Ff <(printf "%s\n" "${job_ids[@]}") | wc -l)
#     if [ "$running_jobs" -eq 0 ]; then
#         echo "All jobs are finished. Submitting run.sh..."
#         break
#     fi
#     sleep 10 # 60秒ごとにチェック
#     echo "Waiting for $running_jobs jobs to finish..., current time is $(date)"
# done

# sbatch scripts/120924.deep.floyd.prompt.3.llama8b.sh
# sbatch scripts/120924.deep.floyd.prompt.3.llama70b.sh
# sbatch scripts/120924.deep.floyd.prompt.3.3.3.llama70b.sh
# sbatch scripts/120924.deep.floyd.prompt.3.phi.sh
# sbatch scripts/120924.deep.floyd.prompt.3.qwen.sh
# sbatch scripts/120924.deep.floyd.prompt.4.phi.sh
# sbatch scripts/120924.deep.floyd.prompt.4.qwen.sh
# sbatch scripts/120924.deep.floyd.prompt.4.llama8b.sh
# sbatch scripts/120924.deep.floyd.prompt.4.llama70b.sh
# sbatch scripts/120924.deep.floyd.prompt.4.3.3.llama70b.sh
# sbatch scripts/120924.deep.floyd.prompt.5.phi.sh
# sbatch scripts/120924.deep.floyd.prompt.5.qwen.sh
# sbatch scripts/120924.deep.floyd.prompt.5.llama8b.sh
# sbatch scripts/120924.deep.floyd.prompt.5.llama70b.sh
# sbatch scripts/120924.deep.floyd.prompt.5.3.3.llama70b.sh

# sbatch scripts/120924.dreamlike.prompt.3.phi.sh
# sbatch scripts/120924.dreamlike.prompt.3.qwen.sh
# sbatch scripts/120924.dreamlike.prompt.3.llama8b.sh
# sbatch scripts/120924.dreamlike.prompt.3.llama70b.sh
# sbatch scripts/120924.dreamlike.prompt.3.3.3.llama70b.sh
# sbatch scripts/120924.dreamlike.prompt.4.phi.sh
# sbatch scripts/120924.dreamlike.prompt.4.qwen.sh
# sbatch scripts/120924.dreamlike.prompt.4.llama8b.sh
# sbatch scripts/120924.dreamlike.prompt.4.llama70b.sh
# sbatch scripts/120924.dreamlike.prompt.4.3.3.llama70b.sh
# sbatch scripts/120924.dreamlike.prompt.5.phi.sh
# sbatch scripts/120924.dreamlike.prompt.5.qwen.sh
# sbatch scripts/120924.dreamlike.prompt.5.llama8b.sh
# sbatch scripts/120924.dreamlike.prompt.5.llama70b.sh
# sbatch scripts/120924.dreamlike.prompt.5.3.3.llama70b.sh

# sbatch scripts/120924.stable.diffusion.prompt.3.phi.sh
# sbatch scripts/120924.stable.diffusion.prompt.3.qwen.sh
# sbatch scripts/120924.stable.diffusion.prompt.3.llama8b.sh
# sbatch scripts/120924.stable.diffusion.prompt.3.llama70b.sh
# sbatch scripts/120924.stable.diffusion.prompt.3.3.3.llama70b.sh
# sbatch scripts/120924.stable.diffusion.prompt.4.phi.sh
# sbatch scripts/120924.stable.diffusion.prompt.4.qwen.sh
# sbatch scripts/120924.stable.diffusion.prompt.4.llama8b.sh
# sbatch scripts/120924.stable.diffusion.prompt.4.llama70b.sh
# sbatch scripts/120924.stable.diffusion.prompt.4.3.3.llama70b.sh
sbatch scripts/120924.stable.diffusion.prompt.5.phi.sh
sbatch scripts/120924.stable.diffusion.prompt.5.qwen.sh
sbatch scripts/120924.stable.diffusion.prompt.5.llama8b.sh
sbatch scripts/120924.stable.diffusion.prompt.5.llama70b.sh
sbatch scripts/120924.stable.diffusion.prompt.5.3.3.llama70b.sh

# sbatch scripts/120924.flux.prompt.3.phi.sh
# sbatch scripts/120924.flux.prompt.3.qwen.sh
# sbatch scripts/120924.flux.prompt.3.llama8b.sh
# sbatch scripts/120924.flux.prompt.3.llama70b.sh
# sbatch scripts/120924.flux.prompt.3.3.3.llama70b.sh
# sbatch scripts/120924.flux.prompt.4.phi.sh
# sbatch scripts/120924.flux.prompt.4.qwen.sh
# sbatch scripts/120924.flux.prompt.4.llama8b.sh
# sbatch scripts/120924.flux.prompt.4.llama70b.sh
# sbatch scripts/120924.flux.prompt.4.3.3.llama70b.sh
# sbatch scripts/120924.flux.prompt.5.phi.sh
# sbatch scripts/120924.flux.prompt.5.qwen.sh
# sbatch scripts/120924.flux.prompt.5.llama8b.sh
# sbatch scripts/120924.flux.prompt.5.llama70b.sh
# sbatch scripts/120924.flux.prompt.5.3.3.llama70b.sh

# sbatch scripts/121224.flux.prompt.3.openai.sh
# sbatch scripts/121224.dreamlike.prompt.3.openai.sh
# sbatch scripts/121224.stable.diffusion.prompt.3.openai.sh
# sbatch scripts/121224.deep.floyd.prompt3.openai.sh
