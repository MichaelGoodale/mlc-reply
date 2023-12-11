import random
import sys

import argparse
from generate_datasets import sample_examples
from datasets import get_grammar_miniscan

words = [
    "dax",
    "lug",
    "wif",
    "zup",
    "fep",
    "blicket",
    "kiki",
    "tufa",
    "gazzer",
]
colours = ["RED", "YELLOW", "GREEN", "BLUE", "PURPLE", "PINK"]

parser = argparse.ArgumentParser(
    prog="String generation",
    description="Fills val directory with variants of gold grammar to test a string",
)

parser.add_argument("-r", "--random", type=int)
parser.add_argument("-s", "--string")
parser.add_argument("--n_times_per_triple", type=int, default=10)

args = parser.parse_args()

if args.random:
    random.seed(args.random)

    input_string, output_string = sample_examples(1, get_grammar_miniscan(), 10, 10)[0]
    while len(output_string.split(" ")) <= 3 or "DAX" not in input_string:
        input_string, output_string = sample_examples(
            1, get_grammar_miniscan(), 10, 10
        )[0]
elif args.string:
    random.seed(1337)
    input_string = args.string
    grammar = get_grammar_miniscan()
    output_string = grammar.apply(input_string)
else:
    print(
        "You need to provide either a specific string or a random seed using -s or -r respectively"
    )
    sys.exit()
print(f"{input_string} -> {output_string}")


def generate_example(n, rule_word, held_out_word, gen_color, file_count=0):
    possible_words = [w for w in words if w not in [rule_word, held_out_word]]
    random.shuffle(possible_words)
    possible_words = [held_out_word] + possible_words
    color = list(set(colours) - set([gen_color]))
    random.shuffle(color)
    color = [gen_color] + color
    color = {k: v for k, v in zip(possible_words, color)}
    replacements = [
        ("1", possible_words[1], color[possible_words[1]]),
        ("2", possible_words[2], color[possible_words[2]]),
        ("3", possible_words[3], color[possible_words[3]]),
        ("DAX", held_out_word, color[held_out_word]),
        ("thrice", rule_word, ""),
        ("surround", possible_words[5], ""),
        ("after", possible_words[4], ""),
    ]
    gen_input = input_string
    gen_output = output_string
    for a, b, c in replacements:
        gen_input = gen_input.replace(a, b)
        gen_output = gen_output.replace(a, c)
    s = f"""*SUPPORT*
IN: {possible_words[1]} OUT: {color[possible_words[1]]}
IN: {possible_words[2]} OUT: {color[possible_words[2]]}
IN: {possible_words[3]} OUT: {color[possible_words[3]]}
IN: {held_out_word} OUT: {color[held_out_word]}
IN: {possible_words[2]} {possible_words[4]} {possible_words[3]} OUT: {color[possible_words[3]]} {color[possible_words[2]]}
IN: {possible_words[1]} {possible_words[4]} {possible_words[2]} OUT: {color[possible_words[2]]} {color[possible_words[1]]}
IN: {possible_words[2]} {rule_word} OUT:{f' {color[possible_words[2]]}'*n}
IN: {possible_words[2]} {possible_words[5]} {possible_words[3]} OUT: {color[possible_words[2]]} {color[possible_words[3]]} {color[possible_words[2]]}
IN: {possible_words[1]} {rule_word} OUT:{f' {color[possible_words[1]]}'*n}
IN: {possible_words[3]} {possible_words[5]} {possible_words[1]} OUT: {color[possible_words[3]]} {color[possible_words[1]]} {color[possible_words[3]]}
IN: {possible_words[2]} {rule_word} {possible_words[4]} {possible_words[3]} OUT: {color[possible_words[3]]}{f' {color[possible_words[2]]}'*n}
IN: {possible_words[3]} {possible_words[4]} {possible_words[1]} {possible_words[5]} {possible_words[2]} OUT: {color[possible_words[1]]} {color[possible_words[2]]} {color[possible_words[1]]} {color[possible_words[3]]}
IN: {possible_words[2]} {possible_words[4]} {possible_words[3]} {rule_word} OUT:{f' {color[possible_words[3]]}'*n} {color[possible_words[2]]}
IN: {possible_words[3]} {possible_words[5]} {possible_words[1]} {possible_words[4]} {possible_words[2]} OUT: {color[possible_words[2]]} {color[possible_words[3]]} {color[possible_words[1]]} {color[possible_words[3]]}

*QUERY*
IN: {gen_input} OUT: {gen_output}

*GRAMMAR*
{possible_words[1]} -> {color[possible_words[1]]}
{possible_words[2]} -> {color[possible_words[2]]}
{possible_words[3]} -> {color[possible_words[3]]}
{held_out_word} -> {color[held_out_word]}
u1 {rule_word} ->{f' [u1]'*n}
u1 {possible_words[5]} u2 -> [u1] [u2] [u1]
x1 {possible_words[4]} x2 -> [x2] [x1]
u1 x1 -> [u1] [x1]"""
    with open(
        f"data_algebraic/val/{file_count}.txt",
        "w",
    ) as f:
        f.write(s)


possible_triplets = {}

for rule_word in words:
    for generalise_word in [w for w in words if w != rule_word]:
        for gen_color in colours:
            possible_triplets[(rule_word, generalise_word, gen_color)] = 0

file_count = 0
for i, (rule_word, held_out_word, held_out_color) in enumerate(
    [k for k, v in possible_triplets.items()]
):
    for _ in range(args.n_times_per_triple):
        generate_example(
            3,
            rule_word,
            held_out_word,
            held_out_color,
            file_count,
        )
        file_count += 1
