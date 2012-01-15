# Stock Market Simulation
# By William Kong
# December 1, 2011

# Based on Lecture 23 of the MIT Intro to Comp. Sci. and Prog. Series
# by Prof. Eric Grimson and Jogn Guttag

# Here is where I will be generating a stock market simulator with the assumption
# that the efficient market hypothesis holds true; this simulation will be a 
# modified version of a random walk

# HELPER FUNCTIONS -------------------------------------------------------------

# The culmulative normal distribution function:
def phi(x):
    return 0.5*( 1.0 + math.erf(x/math.sqrt(2.0)) )

#--- mdToNum ---
# PURPOSE: calculates the number of days that have passed in the year based on an
#          inputed month and day (assume that it is not a leap year)
# FUNCTION: Nat Nat -> Nat

def mdToNum(months,days):
    montharr = [31,28,31,30,31,30,31,31,30,31,30,31] #Days in a month, chronologically
    total = 0
    if months == 1: return days
    else:
        for i in range(months-1):
            total += montharr[i]
        total += days
        return total
    
# --- stockPrice ---
# PURPOSE: uses Ito's Lemma to generate a stock price
# FUNCTION: Stock + Nat + Market -> Float
# Note that this is merely an estimation

def stockPrice(Stk, T, M):
    numLoop = 1000 # Adjust this number for accuracy
    stocMean = 0
    r = M.getDrift()
    v = Stk.volatility
    p = Stk.price
    detComp = (r - v**2/2)*T/365.0
    #for i in range(numLoop):  # Comment out if you do not wish for a Stochastic component
        #stocMean += v*(random.gauss(0,1))*math.sqrt(T)*T/365.0
    stocComp = stocMean / numLoop
    return p*math.exp(detComp + stocComp)
    
# --- putPrice ---
# PURPOSE: uses Black-Scholes to generate a put price
# FUNCTION: Float + Float + Float + Float +  Float + Float -> Float
# Note: S = current stock price
#       K = strike price
#       T = maturity time
#       r = risk-free interest rate
#       v = volatility
#       t = current time (in days)

def putPrice(S, K, T, r, v, t = 0.0):
    d1 = (math.log(S/K) + (r + (v**2.0)/2.0)*((T-t)/365.0)) / v*math.sqrt((T-t)/365.0)
    d2 = d1 - v*math.sqrt((T-t)/365.0)
    return max(0,-S*phi(-d1) + K*math.exp(-r*(T - t)/365.0)*phi(-d2)) #Avoid negative valued options

# --- callPrice ---
# PURPOSE: uses Black-Scholes to generate a call price; uses Call-Put parity
# FUNCTION: Float + Float + Float + Float + Float + Float -> Float
# Note: S = current stock price
#       K = strike price
#       T = maturity time
#       r = risk-free interest rate
#       v = volatility
#       t = current time (in days)

def callPrice(S, K, T, r, v, t = 0.0):
    p = putPrice(S, K, T, r, v, t = 0.0)
    return max(0,-K*math.exp(-r*(T-t)/365)+S+p) #Avoid negative valued options
        
# CLASSES ----------------------------------------------------------------------

import math, pylab, random

# Here, we define a couple classes:

# Below, we have
# mo = momentum (if true, then stocks that are rising are more likely to stay rising
#      and vice versa if the price is falling)
# bf = behavioural finance (if true, then the entirely stock market will be subjected
#      to drastic increases and decreases at certain intervals)

# --- Stock ---
# DESCRIPTION: describes the status of a stock that is randomly increasing or 
#              decreasing over time
# FIELDS: Nat(price), Function(distribution), [Listof Nat](history), Nat(lastChange)

class Stock(object):
    def __init__(self, price, distribution):
        self.price = price
        self.history = [price]
        self.distribution = distribution
        self.lastChange = 0
    def setPrice(self, price):
        self.price = price
        self.history.append(price)
    def getPrice(self):
        return self.price
    def makeMove(self, mktBias, mo):
        oldPrice = self.price
        baseRate = self.distribution() + mktBias
        self.price = self.price * (1.0 + baseRate)
        if mo:
            self.price = self.price + random.gauss(0.5,0.5) * self.lastChange
        if self.price < 0.01:
            self.price = 0.0
        self.history.append(self.price)
        self.lastChange = oldPrice - self.price
    def showHistory(self, figNum):
        pylab.figure(figNum)
        plot = pylab.plot(self.history, label = 'Test Stock')
        plot
        pylab.title('Closing Price, Test ' + str(figNum))
        pylab.xlabel('Day')
        pylab.ylabel('Price')
        
# -------------- Here are my modifications -------------------------------------

# --- NewStock ---
# DESCRIPTION: describes the status of a stock that is randomly increasing or 
#              decreasing over time; modified to make a better Black Scholes
#              simulation by assuming a gaussian distribution
# FIELDS: {Inherited from the Stock class minus a distribution but add in a 
#          volatility value}

class NewStock(Stock):
    def __init__(self, name, price, volatility, time):
        self.name = name
        self.price = price
        self.history = [price]
        self.volatility = volatility
        self.lastChange = 0
        self.duration = time
    def makeMove(self, drift, mo):
        oldPrice = self.price
        vol = self.volatility
        deltat = (1.0/365.0)
        detComp = (drift - vol**2/2)*deltat
        stocComp = vol*(random.gauss(0,1))*math.sqrt(deltat)
        deltas = math.exp(detComp + stocComp)
        self.price =  self.price*deltas
        if mo:
            self.price = self.price + random.gauss(0.5,0.5) * self.lastChange
        if self.price < 0.01:
            self.price = 0.0
        self.history.append(self.price)
        self.lastChange = oldPrice - self.price
    
# --- Market ---
# DESCRIPTION: describes the market in which the stock is running in; essentially
#              describing the environment in which the simulator is runnning in
# FIELDS: Float(drift), [Listof Tuples](trends)

class Market(object):
    def __init__(self, drift, trends):
        self.drift = drift
        self.trends = trends
    def getDrift(self):
        return self.drift
    def getTrends(self):
        return self.trends

# --- Derivative ---
# DESCRIPTION: describes the characteristics of a derivative
# FIELDS: Float(S), Float(K), Float(T), Float(r), Float(v)
# Note: S = current stock price
#       K = strike price
#       T = maturity time (in days)
#       r = risk-free interest rate
#       v = volatility

class Derivative(object):
    def __init__(self, S, K, T, r, v, t):
        self.stockPrice = S
        self.strikePrice = K
        self.maturity = T
        self.rfrate = r
        self.volatility = v
        self.curTime = t
    def setPrice(self):
        self.price = K
    def getPrice(self):
        return self.price()
    
class Trend(object):
    def __init__(self, name, day, factor):
        self.name = name
        self.day = day
        self.factor = factor
        
# ------------ WIP : Need more features ----------------------------------------

# ---PutOption ---
# DESCRIPTION: describes the characteristics of a put option
# FIELDS: Float(S), Float(K), Float(T), Float(r), Float(v), Float(t)

class PutOption(Derivative):
    pass
        
# ---CallOption ---
# DESCRIPTION: describes the characteristics of a call option
# FIELDS: Float(S), Float(K), Float(T), Float(r), Float(v), Float(t)

class CallOption(Derivative):
    pass 