#!/bin/bash

OUTPUT_STRING="all_data.csv"
LOG="rule_log.txt"

declare -a models=("replication.pt" "uniform.pt" "no-four_alt.pt" "few-four.pt")
declare -a datasets=("data_algebraic" "data_algebraic_uniform" "data_algebraic_alt" "data_algebraic_alt_dist")

for ((i = 0; i < 4; i++)); do
  echo ${models[i]}
  for N in {1..10}; do
    FREQ=$(grep -Enr "\-> (\[u1\] ){$N}\$" ${datasets[i]}/train/ | wc -l)
    uv run simple.py "$N" False
    uv run eval.py --max --episode_type few_shot_gold --fn_out_model "${models[i]}" --verbose --max_length 15 >temp.txt
    uv run parse_partial.py temp.txt --n "$N" --frequency "$FREQ" --output $OUTPUT_STRING --model ${models[i]}
    cat temp.txt >>$LOG
    rm temp.txt
  done
done
