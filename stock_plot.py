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

# HELPER FUNCTIONS -------------------------------------------------------------

# --- bfAnnotate ---
# PURPOSE: Annotates a stock sim if bf = True
# FUNCTION: Float + [Listof Float] + Market + Figure + Float -> (Void)

def bfAnnotate2(xRange, yVals, M, fig, scale):
    for d in range(xRange):                 #only if BF is true
        for date in M.getTrends():
            # Annotations
            if (date.day == d % 365 and counter == 1):
                pylab.annotate(date.name, xy=(d, yVals[d]), textcoords = 'offset points',
                               xytext = (0,scale*yVals[d]), ha ='center', 
                               arrowprops=dict(arrowstyle="->", connectionstyle="arc"))
                counter += 1
                counter %= 2
            elif (date.day == d % 365 and counter == 0):
                pylab.annotate(date.name, xy=(d, yVals[d]), textcoords = 'offset points',
                               xytext = (0,-scale*yVals[d]), ha ='center', 
                               arrowprops=dict(arrowstyle="->", connectionstyle="arc"))
                counter += 1
                counter %= 2

# --- bfAnnotate2 ---
# PURPOSE: Annotates a stock sim if bf = True (ver. 2)
# FUNCTION: Float + [Listof Float] + Market + Figure + Float -> (Void)

def bfAnnotate(xRange, yVals, M, fig, scale):
    counter = 1                             #used for annotating
    for d in range(xRange):                 #only if BF is true
        for date in M.getTrends():
            # Annotations
            if (date.day == d % 365 and counter == 1):
                pylab.annotate(date.name, xy=(d, yVals[d]), textcoords = 'offset points',
                               xytext = (0,scale*yVals[d]), ha ='center', 
                               arrowprops=dict(arrowstyle="->", connectionstyle="arc"))
                counter += 1
                counter %= 2
            elif (date.day == d % 365 and counter == 0):
                pylab.annotate(date.name, xy=(d, yVals[d]), textcoords = 'offset points',
                               xytext = (0,-scale*yVals[d]), ha ='center', 
                               arrowprops=dict(arrowstyle="->", connectionstyle="arc"))
                counter += 1
                counter %= 2

# GLOBAL VARIABLES -------------------------------------------------------------

# Market Variables
v = volatility = 0.3 #To reduce typing
ctsMarketRate = rfrate = 0.04

# List of all trends as a [Listof Trend]
Trends = [Trend('Christmas', mdToNum(12,25), 0.05*v),
          Trend('Valentines Day', mdToNum(2,14), 0.005*v), 
          Trend('March Break', mdToNum(3,10), 0.001*v), 
          Trend('September $1^{st}$', mdToNum(9,1), -0.001*v), #; usually the lowest performing month
          Trend('Black Monday', mdToNum(10,19), -0.005*v)]

# VERY important variables for the stock simulations
market = Market(rfrate, Trends)
numDays = 1460
startPrice = 1000.0
mo = False
bf = False
scale = 0.04  #Annotating purposes
numStks = 15

# Used for the options 
months = 4.0
maturity = 365.0/12.0*months #(in days)
strike = startPrice*math.exp(maturity/365.0*rfrate)

# PLOTTING FUNCTONS ------------------------------------------------------------

# Note: S = current stock price
#       K = strike price
#       T = maturity time (in days)
#       r = risk-free interest rate
#       v = volatility

# --- plotStock ---
# PURPOSE: plots a stock simulation using runStockSim
# FUNCTION: String + Float + Nat + Float + Market + Boolean + Boolean + Figure -> (Void)

def plotStock(name, S, T, v, M, mo, bf, fig):
    history = runStockSim(name, S, T, v, M, mo, bf)
    ax = fig.add_subplot(111)
    titleP1 = 'Simulation of Stock ' + str(name) + '\n'
    titleP2 = '$t='+str(T)+'\,(days),\,\sigma='+str(v)+',\,r='+str(M.drift)
    titleP3 = ',\,S_{0}='+str(S)+',\,mo='+str(mo)+',\,bf='+str(bf)+'$'
    plotTitle = titleP1 + titleP2 + titleP3
    ax.set_title(plotTitle)
    ax.plot(history, label = 'Stock' + str(name))
    ax.set_xlabel('Time (days)')
    ax.set_ylabel('Price')
    #ax.grid(True)
    if bf: bfAnnotate(T, history, M, ax, scale)
    #print 'Final Price for Stock ' + name + ': ' + str(history[-1]) #Optional

# --- plotGreeks ---
# PURPOSE: uses Black-Scholes to generate a graph of put and call prices in 
#          relation to some variable; practical way to visualize the greeks
# FUNCTION: Float + Float + Float + Float + Float + String + Figure -> (Void)
# Variables are Market, Strike, Risk-Free-Rate, Volatility, Maturity in Days, Time-Remaining

def plotGreeks(S, K, T, r, v, var, fig):
    x = pylab.arange(0.9,1.1,0.001)
    putPrices = []
    callPrices = []
    if var == 'Market Price': 
        x = pylab.multiply(x,S)
        putPrices = x.copy()
        callPrices = x.copy()
        for i in range(len(x)): putPrices[i] = putPrice(x[i], K, T, r, v)
        for i in range(len(x)): callPrices[i] = callPrice(x[i], K, T, r, v)
    elif var == 'Strike Price' : 
        x = pylab.multiply(x,K)
        putPrices = x.copy()
        callPrices = x.copy()
        for i in range(len(x)): putPrices[i] = putPrice(S, x[i], T, r, v)
        for i in range(len(x)): callPrices[i] = callPrice(S, x[i], T, r, v)        
    elif var == 'Risk-free-rate' : 
        x = pylab.multiply(x,r)
        putPrices = x.copy()
        callPrices = x.copy()
        for i in range(len(x)): putPrices[i] = putPrice(S, K, T, x[i], v)
        for i in range(len(x)): callPrices[i] = callPrice(S, K, T, x[i], v)        
    elif var == 'Volatility' : 
        x = pylab.multiply(x,v)
        putPrices = x.copy()
        callPrices = x.copy()
        for i in range(len(x)): putPrices[i] = putPrice(S, K, T, r, x[i])
        for i in range(len(x)): callPrices[i] = callPrice(S, K, T, r, x[i])
    elif var == 'Maturity in Days' : 
        x = pylab.multiply(x,T)
        putPrices = x.copy()
        callPrices = x.copy()
        for i in range(len(x)): putPrices[i] = putPrice(S, K, x[i], r, v)
        for i in range(len(x)): callPrices[i] = callPrice(S, K, x[i], r, v)
    else : raise NameError('No such variable')
    ax = fig.add_subplot(111)
    titleP1 = 'European Options Simulation \n'
    titleP2 = '$t='+str(T*12/365)+'\,(months),\,\sigma='+str(v)+',\,r='+str(r)
    titleP3 = ',\,S_{0}='+str(S)+',\,K='+str(K)+'$'
    plotTitle = titleP1+titleP2+titleP3 
    ax.set_title(plotTitle)
    ax.plot(x, putPrices, label = 'Put Option')
    ax.plot(x, callPrices, label = 'Call Option')
    ax.set_xlabel(var)
    ax.set_ylabel('Option Prices')
    ax.legend(loc=9)
    #ax.grid(True)
    
# --- plotOptions ---
# PURPOSE: plots a stock simulation using runStockSim and uses data to plot
#          an option simulation
# FUNCTION: String + Float + Float + Nat + Float + Market + Boolean + Boolean + Figure -> (Void)

def plotOptions(name, S, K, T, v, M, mo, bf, fig):
    r = market.getDrift()    
    history = runStockSim(name, S, T, volatility, market, mo, bf)
    putPrices = history[:]
    callPrices = history[:]
    for i in range(len(history)): putPrices[i] = putPrice(history[i], K, T-i, r, v)
    for i in range(len(history)): callPrices[i] = callPrice(history[i], K, T-i, r, v)
    # Plot the stock
    ax1 = fig.add_subplot(211) #subplot feature
    ##ax1 = fig.add_subplot(111) #single plot feauture
    ln1 = ax1.plot(history, label = 'Stock ' + str(name), color='r')
    titleP1 = 'Simulation of Stock ' + str(name) + ' and European Options\n'
    titleP2 = '$t='+str(T)+'\,(days),\,\sigma='+str(v)+',\,r='+str(M.drift)
    titleP3 = ',\,S_{0}='+str(S)+',\,K='+str(K)+',\,mo='+str(mo)+',\,bf='+str(bf)+'$'
    plotTitle = titleP1 + titleP2 + titleP3    
    ax1.set_title(plotTitle)
    ax1.set_xlabel('Time (days)')
    ax1.set_ylabel('Stock Price')
    ax1.legend() #subplot feature
    #ax1.grid(True)
    if bf: bfAnnotate(T, history, M, ax1, scale)     #Optional, since it uses up space
    # Plot the options
    ax2 = fig.add_subplot(212) #subplot feature
    ##ax2 = ax1.twinx() #single plot feature
    ln2 = ax2.plot(putPrices, label = 'Put Option')
    ln3 = ax2.plot(callPrices, label = 'Call Option')
    ax2.set_xlabel('Time (days)')
    ax2.set_ylabel('Options Price')
    ax2.legend() #subplot feature
    ##lns = ln1+ln2+ln3 #single plot feature
    ##labs = [l.get_label() for l in lns] #single plot feature
    ##ax1.legend(lns, labs, mode='expand', ncol=3) #single plot feature
    
# --- plotMulti ---
# PURPOSE: plots a stock simulation of many stocks
# FUNCTION: Nat + Float + Nat + Float + Market + Boolean + Boolean + Figure -> (Void)

def plotMulti(numStks, S, T, v, M, mo, bf, fig):
    mean = 0
    avgVol = 0
    ax = fig.add_subplot(111)
    for i in range(numStks):
        v = random.gauss(0.0, volatility/2.0)
        avgVol += v
        history = runStockSim('Stock'+str(i), S, T, v, M, mo, bf)
        ax.plot(history)
        mean += history[-1]
    mean = mean/float(numStks)
    avgVol = avgVol/numStks
    EStk = NewStock('EStk', S, avgVol, T)
    ES_t = stockPrice(EStk, T, M)
    titleP1 = 'Simulation of '+str(numStks)+' Stocks\n'
    titleP2 = '$t='+str(T)+'\,(days),\,\sigma_{avg}='+str(avgVol)+',\,r='+str(M.drift)
    titleP3 = ',\,S_{0}='+str(S)+',\,E_{t}[S_{0}]='+str(ES_t)+',\,mo='+str(mo)+',\,bf='+str(bf)+'$'
    plotTitle = titleP1 + titleP2 + titleP3   
    ax.set_title(plotTitle)
    ax.axhline(mean, ls='--', color='red', 
               label='Average closing price \n= '+str(mean))
    ax.set_xlabel('Time (days)')
    ax.set_ylabel('Stock Price')
    ax.legend()

# PLOTTING DEMONSTRATIONS ------------------------------------------------------

# This is where we generate our plots
# Below are a couple tests

# Run a trial simulation using the 'rough' unitTestStock function:
#unitTestStock()
#pylab.show() # Show the results

# Run the Black-Scholes model on the price of an option:
#print putPrice(500.0, 1000.0, 365.0*4.0, r, volatility)

# Here are the actual plots that we want
# For the new plots, we initiate a new figure to work with per plot

# Plot the Black-Scholes model for comparing Put/Call Prices to the market price:
fig1 = pylab.figure()
plotGreeks(startPrice, strike, maturity, rfrate, volatility, 'Risk-free-rate', fig1)

# Plot the new Black-Scholes model of a stock simulation:
#fig2 = pylab.figure()
#plotStock('ABC', startPrice, numDays, volatility, market, mo, bf, fig2)

# Plot the above except now with options on a twin axis:
#fig3 = pylab.figure()
#plotOptions('ABC', startPrice, strike, numDays, volatility, market, mo, bf, fig3)

# Plot a multi-stock simulator:
#fig4 = pylab.figure()
#plotMulti(numStks, startPrice, numDays, volatility, market, mo, bf, fig4)