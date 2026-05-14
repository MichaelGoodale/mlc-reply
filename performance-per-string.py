import matplotlib.pyplot as plt
import seaborn as sns

d = {0: 0, 100: 0, "else": 0}
n = []
# bad-strings.txt generated using `./find_weird.sh > bad-strings.txt`
with open("bad-strings.txt") as f:
    for line in f:
        line = line.strip()
        if line.startswith("Acc"):
            x = float(line.split(": ")[1].split(" ")[0])
            n.append(x)
            if x == 0.0:
                d[0] += 1
            elif x == 100.0:
                d[100] += 1
            else:
                d["else"] += 1
print(d)
sns.histplot(n, bins=25)
plt.xlabel("Percent accurate per string")
plt.tight_layout()
plt.show()
# plt.savefig("hist.eps")
