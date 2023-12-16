import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sys

sns.set_theme(style="whitegrid")
plt.figure(figsize=(12, 6), dpi=300)
df = pd.read_csv(sys.argv[1])
df = df.iloc[:, 1:]
df = df.groupby(["episode_number", "type", "n", "frequency"]).mean().reset_index()
df["Task"] = df["type"].apply(lambda x: "Generalize" if x == "generalize" else "Copy")
df["Percent correct per grammar"] = df["correct"]
df["Number of repeated arguments"] = df["n"]
ax = sns.barplot(
    data=df,
    x="Number of repeated arguments",
    y="Percent correct per grammar",
    hue="Task",
    errorbar="ci",
)
sns.move_legend(ax, "upper right")
ax2 = plt.twinx()
ax2.grid(False)
df["Frequency"] = np.log(df["frequency"] + 1)
sns.pointplot(
    data=df,
    x="Number of repeated arguments",
    y="Frequency",
    ax=ax2,
    color="black",
    linestyle="--",
    label="Frequency in the train set",
    markersize=1,
)
ax2.set_ylabel("Log frequency (where log(0)=0)")
ax2.set_ylim(0, 12)
plt.legend(loc="lower center")
plt.show()
