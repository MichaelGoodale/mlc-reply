#!/bin/bash

STRING=${1:-"1 surround DAX after DAX thrice"}
MODEL=${2:-"net-BIML-algebraic-top.pt"}
OUTPUT_STRING="novel_rule_output.txt"
echo "Evaluating $STRING"
rm data_algebraic/val/*
python generate_novel_val_dataset.py -s "$STRING"
python eval.py --max --episode_type algebraic --fn_out_model "$MODEL" --verbose > $OUTPUT_STRING
python parse_generalizations.py $OUTPUT_STRING -s "$STRING"
