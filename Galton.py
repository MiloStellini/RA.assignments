import random
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, binom

class GaltonBoard:
    def __init__(self,n,N):
        self.nrows = n
        self.nballs = N
        self.board = np.zeros((n+1,n+1))
        self.result = np.fliplr(self.board).diagonal()


    def drop_ball(self):
        row, col = 0, 0

        while (row+col) < self.nrows:
            if random.random() < 0.5:
                row += 1
            else:
                col += 1
            
        self.board[row][col] += 1


    def simulation(self):
        for i in range(self.nballs):
            self.drop_ball()
        self.result = np.fliplr(self.board).diagonal()


    def normal_distribution(self):
        #Calculates N(n/2, n/4)
        mu = self.nrows / 2
        sigma = np.sqrt(self.nrows / 4)
        x = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 1000)
        return norm.pdf(x, mu, sigma)*self.nballs, x, mu, sigma


    def binomial_distribution(self):
        #Calculates B(n, 1/2)
        return binom.pmf(np.arange(self.nrows + 1), self.nrows, 0.5) * self.nballs


    def calculate_mse(self, distr1, distr2):
        distr1 = distr1 / np.sum(distr1)
        distr2 = distr2 / np.sum(distr2)
        mse = np.mean((distr1 - distr2) ** 2)
        return mse


    def plot_distributions(self):
        
        norm_pdf, x, mu, sigma = self.normal_distribution()
        binom_pmf = self.binomial_distribution()
        
        plt.subplot(1,2,1)
        plt.plot(x, norm_pdf, label=f'N({mu:.2f}, {sigma:.2f}^2)', color='red')
        plt.bar(range(self.nrows+1), self.result, color = 'blue')
        plt.xlabel("Slot number")
        plt.ylabel("Number of balls")
        plt.title(f"Galton Board : {self.nrows} Rows, {self.nballs} Balls")
        plt.grid(True)

        plt.subplot(1,2,2)
        plt.bar(range(self.nrows+1), binom_pmf, color='blue', label=f'Binomial distribution B({self.nrows}, 1/2)')
        plt.plot(x, norm_pdf, color='red', label=f'Normal distribution N({mu:.2f}, {sigma:.2f}^2)', linewidth=2)
        plt.xlabel("Slot number")
        plt.ylabel("Number of balls")
        plt.title(f'Binomial distribution B({self.nrows}, 1/2) vs Normal N({mu:.2f}, {sigma:.2f}^2)')
        plt.legend()
        plt.grid(True)

        plt.show()


    def error_emp_vs_binom(self, N_values, n_values):

        mse_errors = []

        for n in n_values:
            for N in N_values:
                self.nrows = n
                self.nballs = N
                self.__init__(n,N)
                self.simulation()
                empirical = self.result
                binomial = self.binomial_distribution()
                mse = self.calculate_mse(empirical, binomial)
                mse_errors.append((n, N, mse))
                
                #print(f"MSE for n={n}, N={N}: {mse}")

        mse_errors = np.array(mse_errors)

        plt.figure(figsize=(12, 6))
        for n in n_values:
            mse_n = mse_errors[mse_errors[:, 0] == n]
            plt.plot(mse_n[:, 1], mse_n[:, 2], label=f'MSE (n={n})')
        plt.xlabel('Number of Balls')
        plt.ylabel('Mean Squared Error (MSE)')
        plt.title('Error (MSE) evolution as N and n vary')
        plt.legend()
        plt.grid(True)
        plt.show()

    def error_binom_vs_norm(self,n_values, N):
        mse_values = []
    
        for n in n_values:
            mu = n / 2
            sigma = np.sqrt(n / 4)

            x_values = np.arange(n + 1)

            binomial_pmf = binom.pmf(x_values, n, 0.5) * N
            normal_pdf = norm.pdf(x_values, mu, sigma)*N

            mse = self.calculate_mse(binomial_pmf, normal_pdf)
            mse_values.append(mse)

        plt.figure(figsize=(10, 6))
        plt.plot(n_values, mse_values, marker='o', color='blue', label='MSE (Binomial vs Normal)')
        plt.xlabel('n (board dimension)')
        plt.ylabel('MSE')
        plt.title('Error (MSE) evolution Binomial vs Normal as n varies')
        plt.grid(True)
        plt.legend()
        plt.show()


n = 10     #Number of rows
N = 1000     #Number of balls
n_values = range(5,21,5)     #Values of n for error evolution
N_values = [5,10,20,40,60,80,100]  #Values of N for error evolution

board = GaltonBoard(n,N)
board.simulation()
board.plot_distributions()
board.error_emp_vs_binom(N_values, n_values)
board.error_binom_vs_norm(n_values, N)