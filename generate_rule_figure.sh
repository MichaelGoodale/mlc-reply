#!/bin/bash

MODEL=${1:-"uniform.pt"} #"net-BIML-algebraic-top.pt"}
OUTPUT_STRING="rule_output_alt.csv"
LOG="rule_log.txt"

if test -f "$OUTPUT_STRING"; then
  echo "$OUTPUT_STRING already exists."
  read -p "Do you want to replace it: " -n 1 -r
  echo " "
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    [[ "$0" = "$BASH_SOURCE" ]] && exit 1 || return 1 # handle exits from shell or function but don't exit interactive shell
  else
    rm $OUTPUT_STRING
  fi
fi

for N in {1..10}; do
  FREQ=$(grep -Enr "\-> (\[u1\] ){$N}\$" data_algebraic/train/ | wc -l)
  uv run simple.py "$N" False
  uv run eval.py --max --episode_type few_shot_gold --fn_out_model "$MODEL" --verbose --max_length 15 >temp.txt
  uv run parse_partial.py temp.txt --n "$N" --frequency "$FREQ" --output $OUTPUT_STRING
  cat temp.txt >>$LOG
  rm temp.txt
done

uv run parse_output.py $OUTPUT_STRING
