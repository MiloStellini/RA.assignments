import randomhash # type: ignore
import math
import heapq
import numpy as np
import matplotlib.pyplot as plt

# Hash function
rfh = randomhash.RandomHashFamily()
def h(item):
    x = rfh.hashes(item)[0]
    return f'{x:032b}'

def synthetic_data(n,N,alpha):
    ranks = np.arange(1, n + 1)
    probabilities = 1 / np.power(ranks, alpha)
    probabilities /= probabilities.sum()

    data_stream = [str(x) for x in np.random.choice(ranks, size=N, p=probabilities)]

    return data_stream

# Rho function
def rho(item):
    return len(item) - len(item.lstrip('0')) + 1

alpha16 = 0.673
alpha32 = 0.697
alpha64 = 0.709
alpha_m = lambda m: (0.7213 / (1 + 1.079 / m)) if m >= 128 else None

def get_real_cardinality(file_path):

    try:
        with open(file_path, 'r') as file:
            num_lines = sum(1 for _ in file)
        return num_lines
    except FileNotFoundError:
        print(f"Error: file '{file_path}' not found.")
        return None

# HyperLogLog algorithm
def HyperLogLog(data,b):

    m = 2**b

    # Determina alpha
    if m == 16:
        alpha = alpha16
    elif m == 32:
        alpha = alpha32
    elif m == 64:
        alpha = alpha64
    else:
        alpha = alpha_m(m)

    M = [0]*m

    for v in data:
        x = h(v)

        j = int(x[:b], 2)
        w = x[b:]

        M[j] = max(M[j], rho(w))

    E = alpha*(m**2)*(sum(2**-M[j] for j in range(m)))**-1
    
    if E <= (5/2)*m:
        V = M.count(0)
        if V > 0:
            Estar = m*math.log(m/V)
        else:
            Estar = E
    elif E <= (1/30)*2**32:
        Estar = E
    elif E > (1/30)*2**32:
        Estar = -(2**32)*math.log(1-E/(2**32))        

    return Estar

def Recordinality(data,k):

    rhf = randomhash.RandomHashFamily(count=1)

    records = [float("-inf")] * k
    record_change = 0

    for element in data:
        hash = rhf.hashes(element)

        if hash[0] not in records and hash[0] > records[0]:
            _ = heapq.heapreplace(records, hash[0])
            record_change += 1

    estimate = (
        k * (1 + (1 / k)) ** (record_change - k + 1)
        - 1
    )

    return estimate

def read_file(filename):
    with open(filename, 'r') as file:
        data = file.read().splitlines()
    return data

file_path = "crusoe.txt"
data_file_path = "crusoe.dat"
    
try:
    data = read_file(file_path)
except FileNotFoundError:
    print(f"Error: file '{file_path}' not found.")
    exit()

n = 1000
N = 25000
syn_data = synthetic_data(n,N,0.3)

ntrials = 25

#cardinality = get_real_cardinality(data_file_path)
cardinality = n
print(f"Real cardinality: {cardinality}")

kk = [10,20,50,100,200,500,1000]
estimate_REC = np.zeros(len(kk))
i = 0
for k in kk:
    for _ in range(ntrials):
        estimate_REC[i] += Recordinality(syn_data,k)
    estimate_REC[i] = estimate_REC[i]/ntrials
    #print(f"Estimate cardinality REC: {estimate_REC[i]}")   
    #print(f"REC error: {abs(cardinality-estimate_REC[i])}")
    #print(f"REC error percentage: {abs(cardinality-estimate_REC[i])*100/cardinality} %")
    i += 1



bb = [4,5,6,7,8,9,10,11,12,13,14,15,16]
estimate_HLL = np.zeros(len(bb))
i = 0
for b in bb:
    for _ in range(ntrials):
        estimate_HLL[i] += HyperLogLog(syn_data,b)
    estimate_HLL[i] = estimate_HLL[i]/ntrials
    #print(f"Estimate cardinality HLL: {estimate_HLL[i]}")
    #print(f"HLL error: {abs(cardinality-estimate_HLL[i])}")
    #print(f"HLL error percentage: {abs(cardinality-estimate_HLL[i])*100/cardinality} %")
    i += 1

plt.figure(figsize=(8, 6))
plt.plot(kk, estimate_REC, marker='o', label='REC Estimate')
plt.axhline(y=cardinality, color='r', linestyle='--', label='True Cardinality')
plt.xlabel('Number of Elements (k)')
plt.ylabel('Estimated Cardinality')
plt.title('REC Performance at Different k')
plt.legend()
plt.grid()
plt.show()

plt.figure(figsize=(8, 6))
plt.plot(bb, estimate_HLL, marker='s', label='HLL Estimate')
plt.axhline(y=cardinality, color='r', linestyle='--', label='True Cardinality')
plt.xlabel('b')
plt.ylabel('Estimated Cardinality')
plt.title('HLL Performance at Different m = 2**b')
plt.legend()
plt.grid()
plt.show()


