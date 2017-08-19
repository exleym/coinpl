# coinpl
System for Cryptocurrency Trading Program

# Table of Contents  

1. [Summary](#summary)
2. [Testing](#testing)
3. [GDAX API](#gdax-api)
4. [Architecture](#architecture)

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
Unit testing for the `coinpl` application consists of several groups of
test suites. Each suite tests a specific component of the broader system.  
1.  SQLAlchemy Model Test Suite - test functionality and bahavior of models.
2.  API Test Suite - test the CRUD functionality for each resource.  
3.  PL System Test Suite - test the behavior of the P&L system.  
4.  Market Data Test Suite - test the behavior of the external data services.


#### SQLAlchemy Model Test Suite
> NOT YET IMPLEMENTED  

Ensure that the methods for each model - serialization, deserialization, or 
any specialty functionality (User class for example) work as expected. The 
following models are tested, with each test-case documented in detail:

*   `User` model:
    * test password setter  
    * test password as write-only property  
    * test validate password method  
*   `Cut` model:


#### API Test Suite  
The API test suite ensures that CRUD functionality for the application's 
resource-management API is performing as expected. Each resource implements 
the following tests to ensure core API functionality (`currency` resource 
is shown as an example): 

```python
import unittest

class TestModels(unittest.TestCase):
    API_BASE = '/api/v1.0/'

    def test_create_currency(self):
        """ create sample currencies and verify they have been persisted """
        pass

    def test_get_currency(self):
        """ create a currency object and ensure GET request works """
        pass

    def test_get_multiple_currencies(self):
        """ create several currency objects and ensure GET works for ALL """
        pass

    def test_missing_currency(self):
        """ attempt a GET request on missing data and ensure 404 error """
        pass
        
    def test_update_currency(self):
        """ create a currency object, use PUT to update terms, ensure change
            was persisted
        """
        pass
        
    def test_delete_currency(self):
        """ create a currency object and use DELETE to remove. ensure change
            was persisted 
        """
        pass
```

#### PL System Test Suite  
This set of tests ensures that the PL system is functioning correctly. It uses
mock pricing and trades data to simulate a short period of time, and ensure 
that all holdings, prices, nav and pl data are accurately calculated.  


# GDAX API
The [GDAX API](https://docs.gdax.com/?python#introduction) can provide 
real-time order book data and market data, account statistics, and a way to 
generate automatic trades.  

The GDAX API is exposed as a Python interface in the 
[coinpl.external.gdax](./coinpl/external/gdax) module. This module contains 
classes for data management, order management, and authentication.  


# Architecture  
This system is built to run as a collection of Docker images, with each image 
responsible for a specific piece of functionality. The images are managed as 
a group via the [`docker-compose.yml`](./docker-compose.yml) and 
[`Dockerfile`](./Dockerfile) text files that detail the behavior of the docker 
images, both individually and in their relation to one-another.  

#### Docker Images 
The docker images used in this system are:  
*   `coinpl_web_1`: Flask application providing API management of resources  
*   `coinpl_db_1`: Linux image running MySQL. DB initialized from SQLAlchemy 
    models.
*   `coinpl_mongo_1`: MongoDB image for persisting GDAX order books