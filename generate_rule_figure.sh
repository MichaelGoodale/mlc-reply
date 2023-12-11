#!/bin/bash

OUTPUT_STRING="rule_output.txt"
MODEL=${1:-"net-BIML-algebraic-top.pt"}

if test -f "$OUTPUT_STRING"; then
    echo "$OUTPUT_STRING already exists."
	read -p "Do you want to replace it: " -n 1 -r
	echo  " "
	if [[ ! $REPLY =~ ^[Yy]$ ]]
	then
	    [[ "$0" = "$BASH_SOURCE" ]] && exit 1 || return 1 # handle exits from shell or function but don't exit interactive shell
	fi
fi

rm $OUTPUT_STRING
for N in {1..12}
do
	echo "$N" >> $OUTPUT_STRING
	grep -Enr "\-> (\[u1\] ){$N}\$" data_algebraic/train/ | wc -l >> $OUTPUT_STRING
	python simple.py  "$N" False
	python eval.py  --max --episode_type few_shot_gold --fn_out_model "$MODEL" --verbose --max_length 15 | tail -2 >> $OUTPUT_STRING
done

python parse_output.py $OUTPUT_STRING
