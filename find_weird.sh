#!/bin/bash

MODEL=${1:-"net-BIML-algebraic-top.pt"}

for N in {1..1000}
do
	echo "Seed number $N"
	rm data_algebraic/val/*
	python generate_novel_val_dataset.py -r "$N" --n_times_per_triple 3
	python eval.py  --max --episode_type algebraic --fn_out_model $MODEL 2>/dev/null | tail -1
done
