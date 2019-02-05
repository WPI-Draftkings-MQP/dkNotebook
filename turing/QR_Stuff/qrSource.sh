#!/bin/bash
#SBATCH --job-name=DK_MQP_1
#SBATCH --output=jupyter.log
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=8gb
#SBATCH --time=24:00:00
#SBATCH --gres=gpu:1
date;hostname;pwd

source /home/svwoolf/toTuring/test_env/bin/activate

python qrTester.py DEFAULT
