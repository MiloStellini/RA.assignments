import random
import matplotlib.pyplot as plt
import statistics as stat

# Parameters
m = 50               # Number of bins
beta = 0.5           # Beta-choice parameter
d = 3                # d-choice parameter
k = 1                # Number of questions allowed
T = 50              # Number of trials

# Range of n values for the study
n_values = range(50, 2501, 100)  # Different values of n
methods = ["One-Choice", "Two-Choice", "Beta-Choice", "d-Choice"]

# Helper functions for uncertainty queries
def is_above_median(X, i):
    return X[i] > stat.median(X)

def is_above_75(X, i):
    return X[i] > stat.quantiles(X, n=4)[2]

def is_above_25(X, i):
    return X[i] > stat.quantiles(X, n=4)[0]

# Allocation Methods with Uncertainty
def one_choice(m):          
    return random.randint(0, m - 1)

def two_choice(X, m):
    r = random.sample(range(0, m), 2)
    q1 = [is_above_median(X, r[j]) for j in range(2)]

    if q1[0] and not q1[1]:
        return r[1]
    elif q1[1] and not q1[0]:
        return r[0]
    elif k == 2 and not q1[0] and not q1[1]:
        q2 = [is_above_75(X, r[j]) for j in range(2)]
        if q2[0] and not q2[1]:
            return r[1]
        elif q2[1] and not q2[0]:
            return r[0]
        else:
            return random.choice(r)
    elif k == 2 and q1[0] and q1[1]:
        q2 = [is_above_25(X, r[j]) for j in range(2)]
        if q2[0] and not q2[1]:
            return r[1]
        elif q2[1] and not q2[0]:
            return r[0]
        else:
            return random.choice(r)
    else:
        return random.choice(r)

def beta_choice(X, m, beta):
    return one_choice(m) if random.random() <= beta else two_choice(X, m)

def d_choice(X, m, d):
    r = random.sample(range(0, m), d)
    below_median = [j for j in r if not is_above_median(X, j)]
    if below_median and k == 2:
        below_75th = [j for j in below_median if not is_above_75(X, j)]
        return random.choice(below_75th) if below_75th else random.choice(below_median)
    elif k == 2:
        below_25th = [j for j in r if not is_above_25(X, j)]
        return random.choice(below_25th) if below_25th else random.choice(r)
    else:
        return random.choice(below_median) if below_median else random.choice(r)

# Main simulation function for each method with varying n
def uncertain_methods(m, n, criteria, beta, d):
    X = [0] * m  # Initialize bin loads
    if criteria == 0:
        for _ in range(n):
            X[one_choice(m)] += 1
    elif criteria == 1:
        for _ in range(n):
            X[two_choice(X, m)] += 1
    elif criteria == 2:
        for _ in range(n):
            X[beta_choice(X, m, beta)] += 1
    elif criteria == 3:
        for _ in range(n):
            X[d_choice(X, m, d)] += 1
    else:
        raise ValueError("Invalid criteria method selected.")
    return X

# Collecting G_n results for each method and plotting
Gn_results = {method: [] for method in methods}

# Loop over n values
for n in n_values:
    for k, method in enumerate(methods):
        G_sum = 0
        for t in range(T):  # Run T trials
            X = uncertain_methods(m, n, k, beta, d)
            G_sum += max(X) - n / m
        G_avg = G_sum / T
        Gn_results[method].append(G_avg)

# Plotting the evolution of G_n with increasing n for each method
plt.figure(figsize=(10, 6))
for method, Gn in Gn_results.items():
    plt.plot(n_values, Gn, label=method)

plt.xlabel("Number of balls (n)")
plt.ylabel("Average Gap (G_n)")
plt.title("Evolution of G_n with increasing n")
plt.legend()
plt.grid()
plt.show()
