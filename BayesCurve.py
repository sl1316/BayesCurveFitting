import csv
import os
import numpy as np
import math
import matplotlib.pyplot as plt
alpha = 0.005
beta = 11.1
M = 7
plt.figure(1, figsize= (10,10))

def readFile(stockName):
    fileDir = os.path.dirname(__file__)
    filename = os.path.join(fileDir, "stockData/" + stockName + ".csv")
    file = open(filename)
    reader = csv.reader(file)
    price = []
    for line in reader:
        price.append(float(line[0]))
    return np.asarray(price)

def stockPredictor(prices, stockName, subplot):
    #creat identity matrix(M*M)
    I = np.identity(M)
    X = [i for i in range(1, prices.shape[0] + 1)]
    #initialize phi
    PHI = []
    for x in X:
        PHI.append([math.pow(x, i) for i in range(M)])
    PHI = np.asarray(PHI)
    #calcuate the inverse matrix of S
    S_inverse = np.zeros((M, M))
    for phi in PHI[:-1]:
        value =  np.asmatrix(phi).T * np.asmatrix(phi)
        S_inverse += value
    S_inverse = alpha * I + beta * S_inverse
    #inverse S_inverse to get S
    S = np.linalg.inv(S_inverse)
    #calculate m(x)
    M_x = np.zeros(M)
    for i in range(PHI.shape[0] - 1):
        M_x += PHI[i] * prices[i]
    predictPrices = []
    for phi_test in PHI:
        M_x_test = beta * np.asmatrix(phi_test) * np.asmatrix(S) * np.asmatrix(M_x).T
        predictPrices.append(np.asarray(M_x_test)[0][0])
    dif = predictPrices - prices
    absDif = [abs(d) for d in dif]
    relativeError = 100 * sum(absDif) / sum(prices)
    absError = abs(predictPrices[-1] - prices[len(prices) - 1])
    plt.subplot(5,2,subplot)
    plt.plot(X, prices)
    plt.plot(X, predictPrices)
    plt.ylabel("price")
    plt.xlabel("day")
    plt.title(stockName)
    print "For stock %s:" %stockName
    print "Predict price is: %f" %predictPrices[-1]
    print "Real price is: %f" %prices[len(prices) - 1]
    print "Absolute Error: %f" %absError
    print "Relative Error: %f%%" %relativeError
    print "\n"
    return absError, relativeError

if __name__ == "__main__":
    stockList = ["AAPL", "AMZN", "BABA", "FB", "GOOG", "GRPO", "NFLX", "PYPL", "TSLA", "TWTR"]
    averageAbsError = 0
    averageRelativeError = 0
    figure = 1
    for stock in stockList:
        stockPrices = readFile(stockName = stock)
        absError, relativeError = stockPredictor(stockPrices, stock, figure)
        figure += 1
        averageAbsError += absError
        averageRelativeError += relativeError
    averageRelativeError /= len(stockList)
    averageAbsError /= len(stockList)
    print "The absolute mean error of ten stocks: %f" %averageAbsError
    print "The average relative error of ten stocks: %f\n" %averageRelativeError
    plt.tight_layout()
    plt.savefig('temp.png')
    plt.show()

