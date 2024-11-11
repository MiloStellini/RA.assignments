import random
import matplotlib.pyplot as plt
import pandas as pd

n_values = range(50, 2501, 100)  # Different values of n (from 50 to 2500, in steps of 100)
m = 50              # Number of bins
beta = 0.8          # Beta-choice parameter
d = 5               # d-choice parameter
T = 50             # Number of trials for each n

methods = ["One-Choice", "Two-Choice", "Beta-Choice", "d-Choice"]

# Define methods for each choice strategy
def one_choice(X, m):    
    X[random.randint(0, m-1)] += 1       
    return X

def two_choice(X, m):
    r = random.sample(range(0, m), 2)
    if X[r[0]] < X[r[1]]:
        X[r[0]] += 1
    elif X[r[1]] < X[r[0]]:
        X[r[1]] += 1
    else:
        X[random.choice(r)] += 1
    return X

def beta_choice(X, m, beta):
    if random.random() <= beta:
        X = one_choice(X, m)
    else:
        X = two_choice(X, m)
    return X

def d_choice(X, m, d):
    r = random.sample(range(0, m), d)
    min_load = min([X[i] for i in r])
    min_ind = [j for j in r if X[j] == min_load]
    X[random.choice(min_ind)] += 1
    return X

# Simulation for each allocation method
def choice_methods(m, n, criteria, beta, d):
    X = [0] * m  # Initialize bin loads
    for i in range(n):
        if criteria == 0:
            X = one_choice(X, m)
        elif criteria == 1:
            X = two_choice(X, m)
        elif criteria == 2:
            X = beta_choice(X, m, beta)
        elif criteria == 3:
            X = d_choice(X, m, d)
    return X

# Track and plot the evolution of G_n for each method
Gn_results = {method: [] for method in methods}  # Store results for each method

for n in n_values:
    for k, method in enumerate(methods):
        G_sum = 0
        for t in range(T):  # Run T trials
            X = choice_methods(m, n, k, beta, d)
            G_sum += (max(X) - n / m)  # Calculate G_n for this trial
        G_avg = G_sum / T 
        Gn_results[method].append(G_avg)  # Store the result for this value of n

# Plot the results
plt.figure(figsize=(10, 6))
for method, Gn in Gn_results.items():
    plt.plot(n_values, Gn, label=method)

plt.xlabel("Number of balls (n)")
plt.ylabel("Average Gap (G_n)")
plt.title("Evolution of G_n with increasing n")
plt.legend()
plt.grid()
plt.show()

Gn_table = pd.DataFrame(Gn_results, index=n_values)

# Add n as a column to the DataFrame
Gn_table.index.name = 'n'
Gn_table.reset_index(inplace=True)

# Print the table to the console
print(Gn_table)

Gn_table.to_latex("Gn_evolution.tex", index=False)
