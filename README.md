# coinpl
PL System for Coin Trading Program

# Table of Contents  

1. [Summary](#summary)
2. [Testing](#testing)
3. [GDAX API](#gdax-api)

# Summary
This system is a Bitcoin / Ethereum / Litecoin trading system built around 
the Coinbase / GDAX platform. It consists of several parts:

1.  Currency P&L System - keeps track of what you own and how your strategies
    are working.
2.  Market Data Management System - capture data from as many sources as 
    possible.
3.  Backtesting Framework - use historical data to simulate returns for a 
    hypothetical strategy and see how it works.
3.  Live Trading Framework - actually trade your ideas.
4.  Flask Web Application for Managing System 

Each part serves a role in the construction of a sytematic cryptocurrency 
trading algorith.

# Testing

# GDAX API
The [GDAX API](https://docs.gdax.com/?python#introduction) can provide 
real-time order book data and market data, account statistics, and a way to 
generate automatic trades.  

The GDAX API is exposed as a Python interface in the 
[coinpl.external.gdax](./coinpl/external/gdax) module. This module contains 
classes for data management, order management, and authentication. 