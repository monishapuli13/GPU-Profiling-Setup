import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("reports/results.csv")

plt.figure(figsize=(8, 5))
plt.plot(df.index, df["throughput"])

plt.title("Throughput Across Runs")
plt.xlabel("Run")
plt.ylabel("Samples / Second")

plt.tight_layout()

plt.savefig("reports/throughput.png")

print("Saved reports/throughput.png")