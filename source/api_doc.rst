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
    a.  Get realtime prices and import / adapt to other datasets
        (kaggle has one)
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

-   POST: create a new resource
-   GET: read from resource table, either getting a single resource by <id> or
    retrieving all resources of that type.
-   PUT: update a resource by sending a JSON package with terms to alter.
-   DELETE: destroy a resource by sending a DELETE request with resource <id>.


.. autoflask:: coinpl:create_app(env='prd')
   :blueprints: api_v1