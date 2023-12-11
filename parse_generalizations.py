import re
import pandas as pd
import argparse


parser = argparse.ArgumentParser(
    prog="parse_generalisations",
    description="Parses and processes results from a generalisation run",
)

parser.add_argument("filename")
parser.add_argument("-s", "--string", default="1 surround DAX after DAX thrice")

args = parser.parse_args()
rule_string = args.string.split(" ")
with open(args.filename) as f:
    evaluations = []
    evaluation = {}
    episode_number = None
    state = None
    colour_count = 0
    for line in f:
        line = line.strip()
        if m := re.match(r"Evaluation episode (\d+)", line):
            episode_number = int(m.group(1))
            state = None
            if len(evaluation) > 0:
                evaluations.append(evaluation)
                evaluation = {}
            colour_count = 0
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
                if m := re.match(r"(\w+) -> ([A-Z]+)$", line):
                    evaluation[
                        f"colour_word_{colour_count + 1 if colour_count < 3 else 'h'}"
                    ] = m.group(1)
                    evaluation[
                        f"colour_{colour_count+ 1 if colour_count < 3 else 'h'}"
                    ] = m.group(2)
                    colour_count += 1
            elif state == "retrieval":
                continue
            elif state == "generalize":
                m = re.match(r" ".join([r"(\w+)" for w in rule_string]) + r" ->", line)

                for x in filter(
                    lambda x: x in rule_string, ["DAX", "surround", "after", "thrice"]
                ):
                    evaluation[x] = m.group(rule_string.index(x) + 1)

                if "target" in line:
                    evaluation["correct"] = False
                    string = line.split("->")[1].split("(")[0].strip()
                    for i in range(4):
                        string = string.replace(
                            evaluation[f"colour_{i + 1 if i < 3 else 'h'}"],
                            str(i + 1) if i != 3 else "h",
                        )
                    evaluation["generalization"] = string
                else:
                    evaluation["correct"] = True
                    string = line.split("->")[1].strip()
                    for i in range(4):
                        string = string.replace(
                            evaluation[f"colour_{i + 1 if i < 3 else 'h'}"],
                            str(i + 1) if i != 3 else "h",
                        )
                    evaluation["generalization"] = string
                episode_number = None
                state = None
evaluations.append(evaluation)
df = pd.DataFrame(evaluations)
print(df["generalization"].value_counts())
print(df.groupby(["colour_h"])["correct"].mean())
print(df.groupby(["colour_h"])["correct"].sem())
