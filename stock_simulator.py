# Stock Market Simulation
# By William Kong
# December 1, 2011

# Based on Lecture 23 of the MIT Intro to Comp. Sci. and Prog. Series
# by Prof. Eric Grimson and Jogn Guttag

# Here is where I will be generating a stock market simulator with the assumption
# that the efficient market hypothesis holds true; this simulation will be a 
# modified version of a random walk

import math, pylab, random
from stock_classes import *
from stock_simulator import *

# SIMULATOR --------------------------------------------------------------------

import math, pylab, random
from stock_classes import *

# Here, we define a couple functions:

# --- unitTestStock ---
# PURPOSE: runs a simulation on randomly initiated stocks; this was a rough 
#          version of the simulator before the market class was introduced
# FUNCTION: (Void) -> (Void)

def unitTestStock():
    def runSim(stks, fig, mo):
        mean = 0.0
        for s in stks:
            for d in range(numDays):
                s.makeMove(bias, mo)
            s.showHistory(fig)
            mean += s.getPrice()
        mean = mean/float(numStks)
        pylab.axhline(mean)
    numStks = 1
    numDays = 365
    stks1 = []
    stks2 = []
    bias = 0.005
    mo = True
    for i in range(numStks):
        volatility = random.uniform(0,0.2)
        d1 = lambda: random.uniform(-volatility, volatility)
        d2 = lambda: random.gauss(0.0, volatility/2.0)
        stks1.append(Stock(100.0, d1))
        stks2.append(Stock(100.0, d2))
    runSim(stks1, 1, mo)
    pylab.grid(True)
    runSim(stks2, 2, mo)
    pylab.grid(True)

# ----------------- Here are my modifications ----------------------------------

# --- runStockSim ---
# PURPOSE: runs a stock simulation based on specified parameters; assumes the
#          stock is an Ito process; will run only a single stock for a specified
#          number of days
# FUNCTION: String + Float + Nat + Float + Market + Boolean + Boolean -> [Listof Float]

def runStockSim(name, startPrice, numDays, volatility, market, mo, bf):
    stock = NewStock(name, startPrice, volatility, numDays)
    for d in range(numDays):
        if bf:                                   #only if BF is true
            for date in market.getTrends():
                if date.day-7 == d % 365: 
                    stock.price *= (1 + date.factor)
        stock.makeMove(market.getDrift(), mo)
    return stock.history
