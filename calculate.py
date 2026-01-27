import matplotlib.pyplot as plt

# L2 cache miss penalty in cycles 
L2_miss_cycles = 100  
CPU_frequency = 1e6  # CPU frequency in Hz (1 MHz as example)
# Task periods in ms (example, should match your tasks)
task_periods = {
    'pca': 20,
    'sphinx': 50,
    'disparity': 100
}

# Read results.txt 
results_file = "results.txt"

benchmarks = {}
with open(results_file) as f:
    current_benchmark = None
    for line in f:
        line = line.strip()
        if not line:
            continue
        # Detect benchmark name
        if line in ['pca', 'sphinx', 'disparity']:
            current_benchmark = line
            benchmarks[current_benchmark] = []
            continue
        # Read cache size and LL_misses
        parts = line.split()
        cache_size = int(parts[0])
        ll_misses = int(parts[1])
        benchmarks[current_benchmark].append((cache_size, ll_misses))

# Convert LL_misses to execution time (ms) 
def ll_misses_to_time(ll_misses, miss_cycles=L2_miss_cycles, cpu_freq=CPU_frequency):
    # time = cycles / frequency
    return (ll_misses * miss_cycles) / cpu_freq * 1000  # in ms

execution_times = {}
for benchmark, values in benchmarks.items():
    execution_times[benchmark] = [(cache, ll_misses_to_time(ll)) for cache, ll in values]

#  Compute CPU utilization 
utilizations = {}
for benchmark, times in execution_times.items():
    period = task_periods[benchmark]
    utilizations[benchmark] = [t / period for _, t in times]

#  Rate Monotonic Test 
def rate_monotonic_test(utilizations):
    n = len(utilizations)
    U_total = sum(utilizations)
    U_limit = n * (2**(1/n) - 1)
    return U_total, U_limit, U_total <= U_limit

# Compute RM for all benchmarks
for benchmark, U in utilizations.items():
    U_total, U_limit, schedulable = rate_monotonic_test(U)
    print(f"Benchmark {benchmark}:")
    print(f"  Total CPU Utilization: {U_total:.3f}")
    print(f"  RM Limit: {U_limit:.3f}")
    print(f"  Schedulable? {'Yes' if schedulable else 'No'}\n")

# Pareto Front (Cache size vs Execution time) 
plt.figure(figsize=(8,6))
for benchmark, times in execution_times.items():
    cache_sizes = [c for c, t in times]
    exec_times = [t for c, t in times]
    plt.scatter(cache_sizes, exec_times, label=benchmark)

plt.xlabel("Cache Size")
plt.ylabel("Execution Time (ms)")
plt.title("Pareto Front: Cache Size vs Execution Time")
plt.legend()
plt.grid(True)
plt.show()
