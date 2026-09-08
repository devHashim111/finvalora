Finvalora

Finvalora is a backend-focused cryptocurrency trading platform designed to simulate the architecture and core workflows of a modern crypto exchange.



The project combines a traditional REST API with a dedicated realtime service. The REST layer handles persistent application state and business operations, while the realtime layer is responsible for low-latency market and event streaming.



The system is designed around two complementary backend services:



Django + Django REST Framework for authentication, users, wallets, trading operations, persistent data, and REST APIs.

FastAPI for asynchronous realtime communication, WebSocket connections, and event streaming through Redis.



Finvalora is intended primarily as a backend engineering project and experimental trading platform. It can be used to explore exchange-style application architecture, asynchronous processing, WebSockets, background jobs, trading models, and API-driven frontend integration.

Features

Authentication

Finvalora provides the foundation for authenticated trading workflows, including:



User registration

User login

JWT-based authentication

Authenticated API access

User-associated wallet management



Authentication is handled by the Django REST Framework service.

Wallet Management

Wallets are associated with users and provide the balance layer required by the trading system.



The wallet subsystem is responsible for tracking balances that can be used when creating and executing trades.



Wallet provisioning is intended to occur automatically as part of user registration so that a newly created account can immediately participate in the trading workflow.

Trading

The trading subsystem models the core entities required for a cryptocurrency exchange.



The platform supports the concept of:



Exchanges

Assets

Trading pairs

Wallets

Portfolios

Positions

Orders

Trades

Transactions

Candles

Order-book snapshots

Watchlists

Alerts

Indicator snapshots

Fee schedules



Orders can represent common exchange-style operations such as market and limit orders.



Database-level validation and application-level business logic are used to maintain consistency between orders, trades, wallets, and balances.

Market Data

Finvalora includes a realtime market-data pipeline designed to provide continuously updated information to connected clients.



Market-related data can include:



Asset prices

OHLC candle information

Trading-pair information

Order-book snapshots

Technical indicator information

Other exchange events



Background workers can collect and process market information before publishing events to Redis.

Realtime WebSockets

The FastAPI service provides WebSocket endpoints for clients that need realtime updates.



Instead of requiring every client to repeatedly poll the REST API, connected clients can subscribe to a WebSocket connection and receive events as they become available.



This architecture keeps the long-lived asynchronous connections separate from the traditional Django request/response lifecycle.

Background Processing

Celery is used for tasks that should run independently of normal HTTP requests.



Typical background responsibilities include:



Periodic market-data processing

Scheduled data updates

Publishing events

Data aggregation

Other asynchronous application tasks



Celery Beat is used for scheduled jobs, while Celery workers execute the queued tasks.



Redis acts as the message broker and event transport between background workers and the realtime service.

API Documentation

The Django REST Framework API is documented using drf-spectacular.



This provides an OpenAPI schema that can be used with:



Swagger UI

OpenAPI-compatible clients

API testing tools

Frontend API integration

Automatic API client generation

Architecture

Finvalora separates persistent application logic from realtime communication.

                         ┌─────────────────────┐
                         │      Frontend       │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┴────────────────┐
                    │                                │
                    │ REST / HTTP                    │ WebSocket
                    ▼                                ▼
          ┌─────────────────────┐          ┌─────────────────────┐
          │ Django + DRF        │          │ FastAPI             │
          │                     │          │ realtime/            │
          │ Authentication      │          │                     │
          │ Users               │          │ WebSocket clients   │
          │ Wallets             │          │ Realtime events     │
          │ Trading             │          │ Async streaming     │
          │ Persistent logic    │          │                     │
          └──────────┬──────────┘          └──────────┬──────────┘
                     │                                │
                     │                                │
                     ▼                                ▲
              ┌───────────────┐              ┌───────────────┐
              │   Database    │              │     Redis     │
              │    SQLite     │              │               │
              │               │              │ Pub/Sub       │
              │ Persistent    │              │ Broker        │
              │ application   │              │ Event bus     │
              │ state         │              │               │
              └───────────────┘              └───────┬───────┘
                                                     ▲
                                                     │
                                              ┌──────┴───────┐
                                              │ Celery       │
                                              │              │
                                              │ Workers      │
                                              │ Beat         │
                                              │ Background   │
                                              │ processing   │
                                              └──────────────┘


Service Responsibilities

Django REST Framework

Django is the primary application service.



It is responsible for:



User management

Authentication

JWT token handling

Wallet creation and management

Trading models

Order management

Transaction handling

Persistent application state

Business rules

REST API endpoints

OpenAPI schema generation



Django is therefore the main source of truth for persistent application data.

FastAPI

FastAPI is responsible for the realtime side of the application.



Its primary responsibilities are:



WebSocket connections

Async client communication

Realtime market updates

Redis event consumption

Broadcasting events to connected clients

Streaming rapidly changing data without tying up Django request workers



FastAPI is not intended to duplicate the entire Django API. Instead, it acts as a specialized realtime gateway.

Redis

Redis provides the communication layer between asynchronous producers and consumers.



It can be used for:



Celery message brokering

Pub/Sub channels

Realtime event propagation

Communication between background processing and the FastAPI service



The important architectural concept is that Django/Celery does not need to maintain direct WebSocket connections.



Instead:

Market Data
    ↓
Celery Task
    ↓
Redis
    ↓
FastAPI
    ↓
WebSocket Clients


Celery

Celery handles work that does not need to run directly inside an HTTP request.



Celery Beat schedules recurring operations, while Celery workers execute those operations.



This allows market-data and other periodic processes to continue independently of user requests.

Data Flow

User Registration

The basic registration flow is:

Client
  │
  │ POST /signup
  ▼
Django REST API
  │
  ├── Create user
  │
  └── Provision wallet
          │
          ▼
       Database


Once registration is complete, the user can authenticate and access authenticated API operations.

Authentication

A typical authentication flow is:

Client
  │
  │ Login credentials
  ▼
Django REST API
  │
  ├── Validate credentials
  │
  └── Issue JWT
  │
  ▼
Client


The resulting JWT can then be used to authenticate subsequent API requests.

Order Placement

A simplified order flow is:

Client
   │
   │ Create order
   ▼
Django REST API
   │
   ├── Authenticate user
   ├── Validate trading pair
   ├── Validate order
   ├── Validate wallet/balance
   └── Create order
           │
           ▼
       Database


Depending on the order type and trading workflow, execution can result in trades and corresponding balance or transaction updates.

Realtime Market Data

Market data is processed independently of WebSocket clients:

Market Source
     │
     ▼
Celery / Background Task
     │
     ├── Fetch or process market data
     │
     ├── Aggregate/update data
     │
     └── Publish event
             │
             ▼
           Redis
             │
             ▼
          FastAPI
             │
             ▼
        WebSocket Clients


This decouples market-data processing from client connections.

Trading Domain

Finvalora models a number of concepts commonly found in exchange platforms.

Exchange

Represents a trading venue or market source.

Asset

Represents an individual cryptocurrency or other tradable asset.



Examples conceptually include base and quote assets used in a trading pair.

Trading Pair

Represents a market such as:

BTC/USDT
ETH/USDT
BTC/USDC


A trading pair defines which asset is traded against another asset.

Wallet

Represents user-held balances.



Wallet information is used when validating whether a user can place or execute a trade.

Portfolio

Represents the user's broader financial position across assets and trading activity.

Position

Represents an exposure or holding associated with a particular asset or trading activity.

Order

Represents an instruction submitted by a user to buy or sell an asset.



The trading system can model order types such as:



Market

Limit

Trade

Represents an executed transaction resulting from order execution.



A trade is different from an order: an order is an instruction, while a trade represents execution.

Transaction

Represents a balance-affecting financial event associated with the trading system.

Candle

Represents OHLC-style market data over a time interval.



A candle can contain:

Open
High
Low
Close
Volume
Timestamp


Order Book Snapshot

Represents the state of buy and sell orders at a particular point in time.

Watchlist

Allows users to track selected trading pairs or assets.

Alert

Represents a user-defined condition that can trigger an event.

Indicator Snapshot

Stores calculated technical indicator information.



Possible indicators include concepts such as:



RSI

EMA

MACD

Fee Schedule

Represents trading fee configuration used when calculating transaction or execution costs.

Background Processing Pipeline

The background architecture can be visualized as:

                    Celery Beat
                         │
                         │ scheduled task
                         ▼
                 Celery Worker
                         │
              ┌──────────┴──────────┐
              │                     │
              ▼                     ▼
        Market Processing      Database Update
              │
              ▼
            Redis
              │
              ▼
           FastAPI
              │
              ▼
        WebSocket Clients


This design allows scheduled processing to continue without depending on active users.



It also prevents WebSocket connections from becoming responsible for data acquisition themselves.

API Layer

Finvalora exposes two communication styles.

REST API

The REST API is the primary interface for operations involving persistent state.



Examples of REST responsibilities include:

Authentication
Users
Wallets
Assets
Trading pairs
Orders
Trades
Transactions
Portfolio information
Watchlists
Alerts


The exact endpoints depend on the Django application configuration.

WebSocket API

The WebSocket layer is intended for continuously changing information.



Examples include:

Market prices
Candle updates
Order-book updates
Trading events
Application events


The realtime service is implemented using FastAPI and Python's asynchronous execution model.

API Documentation

The REST API uses drf-spectacular to generate an OpenAPI specification.



This allows the API to be explored and tested through Swagger UI and also makes the API consumable by tooling capable of reading OpenAPI schemas.



A development environment can typically expose the generated API schema and documentation through Django URL configuration.

Project Structure

A conceptual project layout is:

Finvalora/
│
├── manage.py
├── requirements.txt
├── README.md
│
├── <django_project>/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── <django_apps>/
│   ├── authentication/
│   ├── wallets/
│   ├── trading/
│   ├── portfolio/
│   └── ...
│
├── realtime/
│   ├── ...
│   └── WebSocket / Redis integration
│
└── ...


The exact application names may vary as the project evolves.



The important separation is between the persistent Django application and the realtime FastAPI service.

Requirements

The current project stack is based on:

ComponentTechnology

Language

Python 3.12

Main backend

Django 5.1

REST API

Django REST Framework

Realtime API

FastAPI

Realtime transport

WebSockets

Database

SQLite

Message broker

Redis

Background jobs

Celery

Scheduler

Celery Beat

API documentation

drf-spectacular

Deployment target

Vercel

The versions above reflect the project's current README configuration. Update this section whenever the project moves to a different runtime or framework version.

Local Development

1. Clone the repository

git clone <repository-url>
cd Finvalora


2. Create a virtual environment

Linux/macOS:

python3.12 -m venv venv
source venv/bin/activate


Windows:

py -3.12 -m venv venv
venv\Scripts\activate


3. Install dependencies

pip install -r requirements.txt


4. Configure environment variables

Create the appropriate environment configuration for your development environment.



Typical configuration may include values for:

DJANGO_SECRET_KEY
DEBUG
DATABASE_URL
REDIS_URL
CELERY_BROKER_URL


Do not commit secrets or production credentials to source control.

5. Run database migrations

python manage.py migrate


6. Create a superuser

python manage.py createsuperuser


7. Start Django

python manage.py runserver


The Django API will then be available on the development server.

8. Start Redis

Redis must be running for Celery and realtime event communication.



For a local Redis installation, start the Redis service using the appropriate command for your operating system.

9. Start Celery Worker

From the project root:

celery -A <django_project> worker --loglevel=info


Replace <django_project> with the Django project module used by the repository.

10. Start Celery Beat

celery -A <django_project> beat --loglevel=info


11. Start FastAPI

Run the realtime application with an ASGI server such as Uvicorn:

uvicorn realtime.<module>:app --reload


Replace <module> with the actual FastAPI module containing the application instance.

Development Workflow

A typical development environment requires several processes running simultaneously:

Terminal 1
└── Django

Terminal 2
└── Redis

Terminal 3
└── Celery Worker

Terminal 4
└── Celery Beat

Terminal 5
└── FastAPI / WebSockets


This separation mirrors the production architecture and makes it easier to identify which service is responsible for a given problem.

Testing

Django functionality should be tested independently from realtime functionality.



Recommended test areas include:

Authentication
Wallet creation
Wallet balance updates
Order validation
Order creation
Trade execution
Transaction creation
Market-data processing
Celery tasks
Redis event publishing
WebSocket connections
WebSocket event delivery


When adding a trading feature, tests should cover both the normal workflow and invalid states, especially around wallet balances and order validation.

Security

Authentication credentials, JWT signing keys, database credentials, and Redis credentials should never be committed to the repository.



For production deployments:



Use environment variables for secrets.

Disable Django debug mode.

Configure allowed hosts and trusted origins.

Use HTTPS.

Secure WebSocket connections using WSS.

Restrict Redis access to trusted services.

Use a production-grade database instead of SQLite where appropriate.



The development configuration is intentionally simpler than a production exchange deployment.

Deployment

The current project identifies Vercel Serverless as its deployment target.



Because Finvalora contains multiple backend responsibilities, deployment should account for the differences between:



Django HTTP requests

FastAPI ASGI/WebSocket connections

Celery workers

Celery Beat

Redis



In particular, persistent background workers and long-lived WebSocket connections may require deployment infrastructure capable of maintaining those processes continuously.



The deployment configuration should therefore be kept consistent with the execution model supported by the selected hosting environment.

Architectural Goals

Finvalora is not intended to be only a CRUD application.



The project is structured to explore several backend engineering concepts simultaneously:

Separation of concerns

Persistent application logic and realtime communication are handled by different services.

Asynchronous processing

Celery and FastAPI provide mechanisms for work that should not block normal HTTP requests.

Event-driven communication

Redis provides an event path between background processing and realtime clients.

Exchange-style domain modelling

The database models represent the major entities needed to simulate a cryptocurrency trading platform.

API-first development

OpenAPI documentation allows clients and frontend applications to integrate with the backend using a well-defined API contract.

Realtime architecture

WebSockets allow market information and other events to reach connected clients without relying exclusively on HTTP polling.

Current Scope

The current project focuses on the backend foundations of a cryptocurrency exchange simulation.



The primary areas are:

User authentication
        ↓
Wallets
        ↓
Trading models
        ↓
Orders
        ↓
Trades / Transactions
        ↓
Market data
        ↓
Background processing
        ↓
Redis events
        ↓
FastAPI WebSockets


Frontend functionality can be developed independently against the REST and WebSocket interfaces.

Future Improvements

Potential future development areas include:



More complete exchange matching-engine behavior

Advanced order types

Improved order-book handling

More complete portfolio accounting

Richer market-data aggregation

Historical candle storage

Additional technical indicators

User-configurable alerts

Improved transaction auditing

More comprehensive trading statistics

Dedicated production database

Scalable Redis infrastructure

Containerized development and deployment

Automated testing and CI/CD

Production monitoring and logging

Rate limiting and API security hardening



These features can be introduced incrementally without changing the fundamental separation between the Django application and realtime FastAPI service.

Disclaimer

Finvalora is an educational and experimental cryptocurrency trading backend.



It is not a real cryptocurrency exchange and should not be treated as a production financial system.



Any simulated balances, trades, market data, fees, or portfolio calculations are intended for development and testing purposes.

License



MIT License




