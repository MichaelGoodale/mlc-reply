import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sys

with open(sys.argv[1]) as f:
    data = []
    data_point = {}
    for i, l in enumerate(f):
        if i % 4 == 0:
            if data_point != {}:
                data.append(data_point)
                data_point = {}
            data_point["Number of repeated arguments"] = int(l)
        elif i % 4 == 1:
            data_point["freq"] = int(l)
        elif i % 4 == 2:
            data_point["Study Sequences (Copying)"] = float(l.split(": ")[1])
        elif i % 4 == 3:
            data_point["Query Sequences (Generalisations)"] = float(
                l.split(": ")[1].split(" ")[0]
            )
            data_point["novel_acc_sd"] = float(l.split("= ")[1].split(" ")[0])
data.append(data_point)

sns.set_theme()
plt.figure(figsize=(10, 6), dpi=300)
df = pd.DataFrame(data)
melted = pd.melt(
    df,
    id_vars=["Number of repeated arguments"],
    value_vars=["Study Sequences (Copying)", "Query Sequences (Generalisations)"],
    var_name="Task",
    value_name="Accuracy on task",
)
plt.ylim(-1, 101)
ax = sns.lineplot(
    data=melted, x="Number of repeated arguments", y="Accuracy on task", hue="Task"
)
sns.move_legend(ax, "upper right")
ax2 = plt.twinx()
ax2.grid(False)
df["freq"] = np.log(df["freq"] + 1)
sns.lineplot(
    data=df,
    x="Number of repeated arguments",
    y="freq",
    ax=ax2,
    color="black",
    linestyle="--",
    label="Frequency in the train set",
)
ax2.set_ylabel("Log frequency (where log(0)=0)")
plt.legend(loc="lower center")
plt.title("Generalisation only when pretrained to generalise")
plt.show()
