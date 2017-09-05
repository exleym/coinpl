API Documentation
=================
This project aims to be a loosely-coupled relationship between server-side
business logic and client-side UX / UI to allow each component to be written
in a suitable language. Consequently, the server side application must
expose a thorough yet simple and well-documented API for the client-side
application to consume. This section seeks to document that web API.


API Key Points
--------------
This API is meant to be a simple and effective means of controlling the
`coinpl` server-side application from a decouped client (currently
thinking Angular for a first stab at it). That means there are two
types of endpoints to expose first:

1.  CRUD Resource Managment Endpoints
2.  Dataset Access Endpoints

Later, we will want to build in endpoints for managing most parts
of a backtest or trading system running on a local machine, with the
dockerized toolkit running as a virtual server locally and exposing its
tools. If more power is needed, we can worry about scaling later.

3.  Research tools to expose

    a.  Get realtime prices and import / adapt to other datasets (kaggle has one)
    b.  Implement abstract classes to provide backtesting tools.
        These tools should be easily extended into mock or real
        trading systems by switching a few toggles and coding in
        a few extra parameters
    c.  taking a system live shouldn't be trivial to do, to avoid
        accidents -- this should include requiring any scripts that
        generate trades to have a version id and username encoded
        in the docstring in a specific format, and save a hidden
        file documenting the timestamp, machine name, etc. If the
        version changes, the class will prompt you for re-approval,
        and if the module / class detect that the file doesn't
        exist for their version, they will prompt you. This file
        should also store a hmac signature to prove it was created
        by the same CoinbaseAuth user that generated the trades.

At some point, we will also have no choice but to implement event-management
endpoints, but we're currently a long way from there.


Resource Management
-------------------
We need to be able to perform CRUD operations on all existing resources
seamlessly, which means implementing a full suite of resource management
endpoints. These exist for all resources in the form of the following request
types:


Resource Creation
^^^^^^^^^^^^^^^^^
Resources are created via a POST request to the API endpoint, along with
a JSON object containing (at a minimum) the required fields to initialize
the object.

The URL for the resource creation endpoints follows this pattern::

   <BASE_URL>/api/v1.0/<resource_name>

Where <resource_name> is the name of the collection. For example, to create
a news Currency, one must POST to `currencies`.

The POST request should come in the following form::

    import requests
    url = '/api/v1.0/currencies'
    data = {
        "symbol": "ETH",
        "name": "Ethereum",
        "min_size": 0.001,
        "ipo_date": "2014-1-1",
        "currency_limit": 100000
    }
    rv = request.post(url, data=data, content_type='application/json')

The POST request will return a Response object with a status code and an
attribute `data`.


Resource Retrieval
^^^^^^^^^^^^^^^^^^
Resources can be retrieved from the server using a variety of GET requests to
different endpoints. The basic profile of the resource retrieval endpoint set
is detailed below. For resource-specific endpoints like filtering a resource
by non-primary-key fields, see the Swagger docs.

GET Endpoints:
-   get_resource_by_id(resource_id): request a single resource from the API
    by its primary key id.
-   get_resources(): request an array of all available resource objects. Note,
    this only works on resources with reasonably small set size. Large sets
    like Intraday Price will not be available through this endpoint.


Resource Alteration
^^^^^^^^^^^^^^^^^^^
Some resources can and should be altered from time to time, and if they should,
we expose a PUT endpoint that allows clients to alter an existing resource.
There are two standard ways to implement this type of endpoint: 1) force the
user to PUT the entire object to be altered (retrieve the object, make an
alteration, and put the object back to the API) and 2) allow the user to PUT
just the values that should be changed.

NOTE: Unsure which of these we should use

A Python implementation of the full-object PUT is shown here in an interactive
session::

    >>> import requests, json
    >>> url = '/api/v1.0/currency/1'
    >>> currency = request.get(url).data
    >>> print(currency)
    {
        "symbol": "ETH",
        "name": "Ethereum",
        "min_size": 0.001,
        "ipo_date": "2014-1-1",
        "currency_limit": 100000
    }
    >>> currency["currency_limit"] = 9000
    >>> currency["name"] = "OprahCoin"
    >>> request.put(url, currency, content_type='application/json')
    >>> currency = request.get(url).data
    >>> print(currency)
    {
        "symbol": "ETH",
        "name": "OprahCoin",
        "min_size": 0.001,
        "ipo_date": "2014-1-1",
        "currency_limit": 9000
    }

Where the object is requested, altered, and finally put back to the API, before
the correct persisting of the change server-side is verified by the user.


Resource Deletion
^^^^^^^^^^^^^^^^^
Deleting a resource is a very simple process, if the user is authorized to
make the deletion. Most DELETE requests will require some elevated privilege if
they are not targeted at resources belonging to the user themself. Additionally,
some DELETE requests do not actually delete the resource in question, but rather
move it to a state in which it can no-longer be retrieved by non-administrative
users. These cases only exist to maintain auditability of the system.


-   GET: read from resource table, either getting a single resource by <id> or
    retrieving all resources of that type.
-   PUT: update a resource by sending a JSON package with terms to alter.
-   DELETE: destroy a resource by sending a DELETE request with resource <id>.

For a more thorough documentation of the API endpoints and how to use them,
see the Swagger Docs for this project.

Note: look into the idea of embedding Swagger doc and Sphinx doc into the
same project documentation site. Perhaps this should all just be served as
a static page as part of the actual web-app?

