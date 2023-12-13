import os
import re
import pandas as pd
import argparse


parser = argparse.ArgumentParser(
    prog="parse_generalisations",
    description="Parses and processes results from a generalisation run",
)

parser.add_argument("filename")
parser.add_argument("--n", type=int)
parser.add_argument("--output", type=str)
parser.add_argument("--frequency", type=int)

args = parser.parse_args()
with open(args.filename) as f:
    evaluations = []
    state = None
    episode_number = None
    for line in f:
        line = line.strip()
        if m := re.match(r"Evaluation episode (\d+)", line):
            state = None
            episode_number = int(m.group(1))
        elif episode_number is None:
            # Ignore header
            continue
        elif line == "support items;":
            state = "support"
        elif line.startswith("retrieval items;"):
            state = "retrieval"
        elif line.startswith("generalization items;"):
            state = "generalize"
        elif state is not None:
            if state == "support":
                continue
            elif state in ["retrieval", "generalize"]:
                evaluations.append(
                    {
                        "episode_number": episode_number,
                        "n": args.n,
                        "frequency": args.frequency,
                        "type": state,
                        "correct": "target" not in line,
                    }
                )
df = pd.DataFrame(evaluations)
df.to_csv(args.output, mode="a", header=not os.path.exists(args.output))
