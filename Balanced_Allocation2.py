import random
import matplotlib.pyplot as plt
import numpy as np

# Parameters
m = 50               # Number of bins
beta = 0.5           # Beta-choice parameter
d = 3                # d-choice parameter
T = 50              # Number of trials

# Range of n values for the study
n_values = range(50, 2501, 100)  # Increasing values of n
methods = ["One-Choice", "Two-Choice", "Beta-Choice", "d-Choice"]

# Allocation Methods
def one_choice(m):          
    return random.randint(0, m - 1)

def two_choice(X, m):
    r = random.sample(range(m), 2)
    return r[0] if X[r[0]] < X[r[1]] else (r[1] if X[r[1]] < X[r[0]] else random.choice(r))

def beta_choice(X, m, beta):
    return one_choice(m) if random.random() <= beta else two_choice(X, m)

def d_choice(X, m, d):
    r = random.sample(range(m), d)
    min_load = min(X[i] for i in r)
    min_ind = [j for j in r if X[j] == min_load]
    return random.choice(min_ind)

# Batch Allocation Simulation
def b_batching_methods(m, n, criteria, beta, d, b):
    X = [0] * m  # Bins loads
    for _ in range(int(n / b)):
        aux = [0] * m  # Temporary bin loads for each batch
        for _ in range(b):
            if criteria == 0:
                index = one_choice(m)
            elif criteria == 1:
                index = two_choice(X, m)
            elif criteria == 2:
                index = beta_choice(X, m, beta)
            elif criteria == 3:
                index = d_choice(X, m, d)
            else:
                raise ValueError("Invalid criteria method selected.")
            aux[index] += 1
        X = [x + y for x, y in zip(X, aux)]
    return X

# Store results for plotting
Gn_results = {method: [] for method in methods}

# Calculate Gn evolution for each method
for n in n_values:
    b = max(1, n//3)
    for k, method in enumerate(methods):
        G_sum = 0
        for t in range(T):  # Run T trials
            X = b_batching_methods(m, n, k, beta, d, b)
            G_sum += (max(X) - n / m)
        G_avg = G_sum / T
        Gn_results[method].append(G_avg)

# Plotting Gn evolution for each method with b proportional to n
plt.figure(figsize=(10, 6))
for method, Gn in Gn_results.items():
    plt.plot(n_values, Gn, label=method)

plt.xlabel("Number of balls (n)")
plt.ylabel("Average Gap (G_n)")
plt.title("Evolution of G_n with increasing n (b = n/3)")
plt.legend()
plt.grid()
plt.show()
