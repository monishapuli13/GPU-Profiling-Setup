import time


def benchmark(fn, iterations):
    start = time.perf_counter()

    for _ in range(iterations):
        fn()

    end = time.perf_counter()

    elapsed = end - start

    return elapsed