# benchmark.py

import os
import torch
import torch.nn as nn
import time
from metrics import get_memory_usage
from torch.profiler import profile
from throughput import benchmark
from report import save_report

class SimpleNet(nn.Module):
    def __init__(self):
        super().__init__()

        self.layers = nn.Sequential(
            nn.Linear(1024, 2048),
            nn.ReLU(),
            nn.Linear(2048, 1024)
        )

    def forward(self, x):
        return self.layers(x)


device = "cuda" if torch.cuda.is_available() else "cpu"

model = SimpleNet().to(device)


def train_step():
    x = torch.randn(256, 1024).to(device)

    output = model(x)

    loss = output.mean()

    loss.backward()


os.makedirs("traces", exist_ok=True)
iterations = 100
batch_size = 256

start = time.perf_counter()

with profile(
    activities=[
        torch.profiler.ProfilerActivity.CPU
    ]
) as prof:

    for _ in range(iterations):
        train_step()

elapsed = time.perf_counter() - start

samples_per_second = (iterations * batch_size) / elapsed
print(
    prof.key_averages().table(
        sort_by="cpu_time_total",
        row_limit=10
    )
)

print(f"\nElapsed Time: {elapsed:.2f}s")
print(f"Throughput: {samples_per_second:.2f} samples/sec")

try:
    prof.export_chrome_trace("traces/trace.json")
    print("Trace saved to traces/trace.json")
except RuntimeError as e:
    print(f"Profiler trace already exists: {e}")

print(get_memory_usage())
memory = get_memory_usage()["rss_mb"]

save_report(
    elapsed,
    samples_per_second,
    memory
)