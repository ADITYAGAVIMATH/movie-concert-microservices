# Movie & Concert Ticket Booking System

A containerized, microservices-based ticket booking platform designed for movies and live concert events. This project demonstrates microservice design principles, RESTful inter-service communication, containerization with Docker, multi-container orchestration with Docker Compose, and performance benchmarking under varying load conditions.

---

## Table of Contents

- [Project Overview](#project-overview)
- [System Architecture](#system-architecture)
- [Microservices Breakdown](#microservices-breakdown)
- [Repository Structure](#repository-structure)
- [Service Specifications](#service-specifications)
  - [Event Service](#event-service)
  - [User Service](#user-service)
  - [Seat Service](#seat-service)
  - [Booking Service](#booking-service)
  - [Payment Service](#payment-service)
- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Running Event Service](#running-event-service)
- [Running User Service](#running-user-service)
- [Running Seat Service](#running-seat-service)
- [Running Booking Service](#running-booking-service)
- [Running Payment Service](#running-payment-service)
- [Docker Network](#docker-network)
- [API Testing & Verification](#api-testing--verification)
- [Load Testing & Performance Evaluation](#load-testing--performance-evaluation)
- [Project Roadmap](#project-roadmap)
- [Academic Context](#academic-context)

---

## Project Overview

The Movie & Concert Ticket Booking System decouples traditional monolithic ticketing operations into autonomous, loosely-coupled microservices. Each service encapsulates a distinct business domain with its own code, dependencies, and deployment lifecycle.

### Key Objectives

- **Domain-Driven Isolation:** Independent microservices for Users, Events, Seats, Bookings, and Payments.
- **Containerization:** Each service packages its own runtime environment using Docker containers.
- **Standardized REST Communication:** Clear HTTP/JSON communication between services.
- **Scalability & Orchestration:** Services can be connected and managed using Docker Compose.
- **Service Independence:** Each microservice can be developed, tested, built, and deployed independently.
- **Performance Evaluation:** Load testing using Locust and custom Python load generators.

---

## System Architecture

```text
                           +------------------+
                           |      Client      |
                           |  Web / Mobile    |
                           +--------+---------+
                                    |
                                    | HTTP / REST
                                    v
                           +------------------+
                           |   API Gateway    |
                           |   Port 8000      |
                           +--------+---------+
                                    |
              +---------------------+----------------------+
              |                     |                      |
              v                     v                      v
       +--------------+      +--------------+      +--------------+
       | User Service |      | Event Service|      | Seat Service |
       |   Port 5002  |      |   Port 5001  |      |   Port 5003  |
       +--------------+      +--------------+      +------+-------+
                                                         |
                                                         v
                                                  +--------------+
                                                  |Booking Service|
                                                  |   Port 5004  |
                                                  +------+-------+
                                                         |
                                                         v
                                                  +--------------+
                                                  |Payment Service|
                                                  |   Port 5005  |
                                                  +--------------+
```

### Booking Service Communication Flow

```text
Client
  |
  v
Booking Service
  |
  +----> User Service
  |       Verify User
  |
  +----> Event Service
  |       Verify Event
  |
  +----> Seat Service
  |       Reserve Seats
  |
  +----> Payment Service
          Process Payment
  |
  v
Booking Confirmed
```

---

## Microservices Breakdown

| Service | Host Port | Container Port | Description | Status |
| :--- | :---: | :---: | :--- | :---: |
| API Gateway | 8000 | 8000 | Unified entry point and request routing | Planned |
| Event Service | 5001 | 5000 | Manages movie and concert event information | Active |
| User Service | 5002 | 5000 | Manages users and user profiles | Active |
| Seat Service | 5003 | 5000 | Manages seat availability, reservation and release | Active |
| Booking Service | 5004 | 5000 | Coordinates the complete booking workflow | Active |
| Payment Service | 5005 | 5000 | Processes payments and generates transactions | Active |

---

# Repository Structure

```text
movie-concert-microservices/
│
├── api-gateway/
│   └── API Gateway configuration and routing
│
├── architecture/
│   └── Architecture diagrams and design documents
│
├── docs/
│   └── Project documentation
│
├── load-testing/
│   ├── locustfile.py
│   └── load_generator.py
│
├── results/
│   └── Performance results and graphs
│
├── services/
│   │
│   ├── event-service/
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   │
│   ├── user-service/
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   │
│   ├── seat-service/
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   │
│   ├── booking-service/
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   │
│   └── payment-service/
│       ├── app.py
│       ├── requirements.txt
│       └── Dockerfile
│
├── .gitignore
└── README.md
```

---

# Service Specifications

## Event Service

The Event Service is responsible for managing movie and concert event information.

**Base URL:**

```text
http://localhost:5001
```

**Container Port:** `5000`

**Host Port:** `5001`

### Available Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| GET | `/` | Health check |
| GET | `/events` | Retrieve all events |
| GET | `/events/<id>` | Retrieve event by ID |

### 1. Health Check

```http
GET / HTTP/1.1
Host: localhost:5001
```

**Response:**

```json
{
    "service": "Event Service",
    "status": "running"
}
```

### 2. Get All Events

```http
GET /events HTTP/1.1
Host: localhost:5001
```

**Response:**

```json
[
    {
        "id": 1,
        "name": "Avengers: Secret Wars",
        "type": "movie",
        "venue": "PVR Hubli",
        "date": "2026-10-05"
    },
    {
        "id": 2,
        "name": "Arijit Singh Live",
        "type": "concert",
        "venue": "Bengaluru",
        "date": "2026-10-10"
    }
]
```

### 3. Get Event by ID

```http
GET /events/1 HTTP/1.1
Host: localhost:5001
```

**Response:**

```json
{
    "id": 1,
    "name": "Avengers: Secret Wars",
    "type": "movie",
    "venue": "PVR Hubli",
    "date": "2026-10-05"
}
```

**Error Response:**

```json
{
    "error": "Event not found"
}
```

---

# User Service

The User Service handles user registration and user profile management.

**Base URL:**

```text
http://localhost:5002
```

**Container Port:** `5000`

**Host Port:** `5002`

### Available Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| GET | `/` | Health check |
| GET | `/users` | Retrieve all users |
| GET | `/users/<id>` | Retrieve user by ID |
| POST | `/users` | Create a new user |

### 1. Health Check

```http
GET / HTTP/1.1
Host: localhost:5002
```

**Response:**

```json
{
    "service": "User Service",
    "status": "running"
}
```

### 2. Get All Users

```http
GET /users HTTP/1.1
Host: localhost:5002
```

**Response:**

```json
[
    {
        "id": 1,
        "name": "Manasa",
        "email": "manasa@example.com"
    },
    {
        "id": 2,
        "name": "Renuka",
        "email": "renuka@test.conm"
    },
    {
        "id": 3,
        "name": "Aditya",
        "email": "aditya@test.conm"
    }
]
```

### 3. Get User by ID

```http
GET /users/1 HTTP/1.1
Host: localhost:5002
```

**Response:**

```json
{
    "id": 1,
    "name": "Manasa",
    "email": "manasa@example.com"
}
```

### 4. Create New User

```http
POST /users HTTP/1.1
Host: localhost:5002
Content-Type: application/json

{
    "name": "Alex Mercer",
    "email": "alex@example.com"
}
```

**Response:**

```json
{
    "id": 4,
    "name": "Alex Mercer",
    "email": "alex@example.com"
}
```

### Invalid User

```http
GET /users/99 HTTP/1.1
Host: localhost:5002
```

**Response:**

```json
{
    "error": "User not found"
}
```

---

# Seat Service

The Seat Service manages seat availability, reservation, and release for events.

**Base URL:**

```text
http://localhost:5003
```

**Container Port:** `5000`

**Host Port:** `5003`

### Available Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| GET | `/` | Health check |
| GET | `/seats/<event_id>` | Get all seats for an event |
| GET | `/seats/<event_id>/available` | Get available seats |
| POST | `/seats/<event_id>/reserve` | Reserve seats |
| POST | `/seats/<event_id>/release` | Release seats |

### 1. Health Check

```http
GET / HTTP/1.1
Host: localhost:5003
```

**Response:**

```json
{
    "service": "Seat Service",
    "status": "running"
}
```

### 2. Get All Seats

```http
GET /seats/1 HTTP/1.1
Host: localhost:5003
```

**Response:**

```json
{
    "event_id": 1,
    "seats": {
        "A1": "available",
        "A2": "available",
        "A3": "available",
        "A4": "available",
        "A5": "available",
        "B1": "available",
        "B2": "available",
        "B3": "available",
        "B4": "available",
        "B5": "available"
    }
}
```

### 3. Get Available Seats

```http
GET /seats/1/available HTTP/1.1
Host: localhost:5003
```

**Response:**

```json
{
    "event_id": 1,
    "available_seats": [
        "A1",
        "A2",
        "A3",
        "A4",
        "A5",
        "B1",
        "B2",
        "B3",
        "B4",
        "B5"
    ]
}
```

### 4. Reserve Seats

```http
POST /seats/1/reserve HTTP/1.1
Host: localhost:5003
Content-Type: application/json

{
    "seats": [
        "A1",
        "A2"
    ]
}
```

**Response:**

```json
{
    "message": "Seats reserved successfully",
    "event_id": 1,
    "seats": [
        "A1",
        "A2"
    ]
}
```

### Seat Conflict

If a seat is already reserved:

```json
{
    "error": "Some seats are not available",
    "seats": [
        "A1"
    ]
}
```

### 5. Release Seats

```http
POST /seats/1/release HTTP/1.1
Host: localhost:5003
Content-Type: application/json

{
    "seats": [
        "A1",
        "A2"
    ]
}
```

**Response:**

```json
{
    "message": "Seats released successfully",
    "event_id": 1,
    "seats": [
        "A1",
        "A2"
    ]
}
```

---

# Booking Service

The Booking Service is the central orchestration service responsible for coordinating User, Event, Seat, and Payment services.

**Base URL:**

```text
http://localhost:5004
```

**Container Port:** `5000`

**Host Port:** `5004`

**Dependencies:**

```text
User Service
Event Service
Seat Service
Payment Service
```

## Booking Workflow

```text
                 +------------------+
                 | Booking Request  |
                 +--------+---------+
                          |
                          v
                 +------------------+
                 | Booking Service  |
                 +--------+---------+
                          |
          +---------------+---------------+
          |               |               |
          v               v               v
   User Service    Event Service    Seat Service
   Verify User     Verify Event     Reserve Seats
          |               |               |
          +---------------+---------------+
                          |
                          v
                  Payment Service
                  Process Payment
                          |
                          v
                  Booking Confirmed
```

### Available Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| GET | `/` | Health check |
| POST | `/bookings` | Create a booking |

### 1. Health Check

```http
GET / HTTP/1.1
Host: localhost:5004
```

**Response:**

```json
{
    "service": "Booking Service",
    "status": "running"
}
```

### 2. Create Booking

```http
POST /bookings HTTP/1.1
Host: localhost:5004
Content-Type: application/json

{
    "user_id": 2,
    "event_id": 1,
    "seats": [
        "A1",
        "A2"
    ]
}
```

### Booking Processing Steps

The Booking Service performs the following operations:

1. Verifies the user through the User Service.
2. Verifies the event through the Event Service.
3. Reserves seats through the Seat Service.
4. Calculates the ticket amount.
5. Sends the payment request to the Payment Service.
6. Releases seats if payment processing fails.
7. Creates the booking confirmation.

**Ticket Price:**

```text
₹500 per seat
```

### Successful Booking Response

```json
{
    "message": "Booking created successfully",
    "booking_id": "generated-uuid",
    "user": {
        "id": 2,
        "name": "Renuka",
        "email": "renuka@test.conm"
    },
    "event": {
        "id": 1,
        "name": "Avengers: Secret Wars",
        "type": "movie",
        "venue": "PVR Hubli",
        "date": "2026-10-05"
    },
    "seats": [
        "A1",
        "A2"
    ],
    "amount": 1000,
    "payment": {
        "message": "Payment successful",
        "transaction_id": "generated-uuid",
        "user_id": 2,
        "amount": 1000,
        "status": "completed"
    },
    "status": "confirmed"
}
```

### Seat Conflict Response

```json
{
    "error": "Seat reservation failed",
    "details": {
        "error": "Some seats are not available",
        "seats": [
            "A1"
        ]
    }
}
```

---

# Payment Service

The Payment Service processes payments and generates a unique transaction ID for each successful payment.

**Base URL:**

```text
http://localhost:5005
```

**Container Port:** `5000`

**Host Port:** `5005`

### Available Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| GET | `/` | Health check |
| POST | `/payments` | Process a payment |

### 1. Health Check

```http
GET / HTTP/1.1
Host: localhost:5005
```

**Response:**

```json
{
    "service": "Payment Service",
    "status": "running"
}
```

### 2. Process Payment

```http
POST /payments HTTP/1.1
Host: localhost:5005
Content-Type: application/json

{
    "user_id": 3,
    "amount": 500
}
```

**Response:**

```json
{
    "message": "Payment successful",
    "transaction_id": "generated-uuid",
    "user_id": 3,
    "amount": 500,
    "status": "completed"
}
```

### Invalid Amount

```json
{
    "error": "Amount must be greater than zero"
}
```

---

# Getting Started

## Prerequisites

Install the following software before running the project:

- Git
- Python 3.10+
- Docker
- Docker Desktop
- Docker Compose

---

# Running Event Service

Navigate to the service directory:

```bash
cd services/event-service
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the service:

```bash
python app.py
```

The service will run on:

```text
http://localhost:5000
```

### Docker

Build the image:

```bash
docker build -t event-service:v1 .
```

Run the container:

```bash
docker run -d -p 5001:5000 --name event-service-container event-service:v1
```

Check the container:

```bash
docker ps
```

---

# Running User Service

Navigate to the service directory:

```bash
cd services/user-service
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the service:

```bash
python app.py
```

### Docker

Build the image:

```bash
docker build -t user-service:v1 .
```

Run the container:

```bash
docker run -d -p 5002:5000 --name user-service-container user-service:v1
```

Check the container:

```bash
docker ps
```

---

# Running Seat Service

Navigate to the service directory:

```bash
cd services/seat-service
```

Build the Docker image:

```bash
docker build -t seat-service:v1 .
```

Run the container:

```bash
docker run -d \
    --name seat-service-container \
    -p 5003:5000 \
    seat-service:v1
```

Check the container:

```bash
docker ps
```

The Seat Service will be available at:

```text
http://localhost:5003
```

---

# Running Payment Service

Navigate to the service directory:

```bash
cd services/payment-service
```

Build the Docker image:

```bash
docker build -t payment-service:v1 .
```

Run the container:

```bash
docker run -d \
    --name payment-service-container \
    -p 5005:5000 \
    payment-service:v1
```

Check the container:

```bash
docker ps
```

The Payment Service will be available at:

```text
http://localhost:5005
```

---

# Running Booking Service

The Booking Service communicates with the other services using Docker container networking.

Create the Docker network:

```bash
docker network create microservices-network
```

Build the Booking Service image:

```bash
cd services/booking-service

docker build -t booking-service:v1 .
```

Run the Booking Service:

```bash
docker run -d \
    --name booking-service-container \
    --network microservices-network \
    -p 5004:5000 \
    booking-service:v1
```

The Booking Service uses the following internal service addresses:

```text
http://user-service-container:5000
http://event-service-container:5000
http://seat-service-container:5000
http://payment-service-container:5000
```

The Booking Service is available from the host at:

```text
http://localhost:5004
```

---

# Docker Network

The microservices communicate with each other through a dedicated Docker bridge network.

```bash
docker network create microservices-network
```

View available Docker networks:

```bash
docker network ls
```

Inspect the microservices network:

```bash
docker network inspect microservices-network
```

Expected services connected to the network:

```text
event-service-container
user-service-container
seat-service-container
booking-service-container
payment-service-container
```

---

# API Testing & Verification

The services can be tested using:

- cURL
- PowerShell
- Postman

---

# Event Service Testing

### Health Check

```powershell
Invoke-RestMethod http://localhost:5001/
```

### Get All Events

```powershell
Invoke-RestMethod http://localhost:5001/events
```

### Get Event by ID

```powershell
Invoke-RestMethod http://localhost:5001/events/1
```

### Invalid Event

```powershell
Invoke-RestMethod http://localhost:5001/events/99
```

---

# User Service Testing

### Health Check

```powershell
Invoke-RestMethod http://localhost:5002/
```

### Get All Users

```powershell
Invoke-RestMethod http://localhost:5002/users
```

### Get User by ID

```powershell
Invoke-RestMethod http://localhost:5002/users/1
```

### Create User

```powershell
$body = @{
    name = "Alex Mercer"
    email = "alex@example.com"
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://localhost:5002/users" `
    -Method Post `
    -Body $body `
    -ContentType "application/json"
```

---

# Seat Service Testing

### Health Check

```powershell
Invoke-RestMethod http://localhost:5003/
```

### Get All Seats

```powershell
Invoke-RestMethod http://localhost:5003/seats/1
```

### Get Available Seats

```powershell
Invoke-RestMethod http://localhost:5003/seats/1/available
```

### Reserve Seats

```powershell
$body = @{
    seats = @("A1", "A2")
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://localhost:5003/seats/1/reserve" `
    -Method Post `
    -Body $body `
    -ContentType "application/json"
```

### Release Seats

```powershell
$body = @{
    seats = @("A1", "A2")
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://localhost:5003/seats/1/release" `
    -Method Post `
    -Body $body `
    -ContentType "application/json"
```

---

# Booking Service Testing

### Health Check

```powershell
Invoke-RestMethod http://localhost:5004/
```

### Create Booking

```powershell
$body = @{
    user_id = 2
    event_id = 1
    seats = @("A1", "A2")
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://localhost:5004/bookings" `
    -Method Post `
    -Body $body `
    -ContentType "application/json"
```

The Booking Service automatically communicates with:

```text
User Service
Event Service
Seat Service
Payment Service
```

---

# Payment Service Testing

### Health Check

```powershell
Invoke-RestMethod http://localhost:5005/
```

### Process Payment

```powershell
$body = @{
    user_id = 3
    amount = 500
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://localhost:5005/payments" `
    -Method Post `
    -Body $body `
    -ContentType "application/json"
```

---

# Multi-Container Deployment

The final system is intended to be orchestrated using Docker Compose.

From the project root:

```bash
docker compose up --build -d
```

Check all running containers:

```bash
docker ps
```

Stop the complete application:

```bash
docker compose down
```

---

# Load Testing & Performance Evaluation

One of the major objectives of the project is evaluating the performance of the microservices architecture under different workloads.

## Testing Tools

### Locust

Locust is used to simulate multiple concurrent users and measure system performance.

The Locust scripts will be maintained inside:

```text
load-testing/
```

### Custom Python Load Generator

A custom Python load generator is used to generate high-volume requests and evaluate the performance of individual services and the complete system.

---

## Workloads

The system will be evaluated using different workloads:

```text
100 Users
1,000 Users
10,000 Users
```

---

## Performance Metrics

The following metrics will be collected:

### Throughput

Number of requests processed per second.

```text
Requests Per Second (RPS)
```

### Response Time

Response latency for service requests.

Important percentiles include:

```text
50th percentile
90th percentile
95th percentile
99th percentile
```

### Failure Rate

Percentage of failed requests under different loads.

### Resource Utilization

Container resource usage can be monitored using:

```bash
docker stats
```

Metrics include:

- CPU usage
- Memory usage
- Network usage
- Container resource consumption

---

# Project Roadmap

- [x] **Milestone 1:** Architecture & domain modeling
- [x] **Milestone 2:** Implement & containerize Event Service
- [x] **Milestone 3:** Implement & containerize User Service
- [x] **Milestone 4:** Implement & containerize Seat Service
- [x] **Milestone 5:** Implement & containerize Booking Service
- [x] **Milestone 5:** Implement & containerize Payment Service
- [ ] **Milestone 6:** Configure API Gateway
- [ ] **Milestone 6:** Complete Docker Compose configuration
- [ ] **Milestone 7:** Execute Locust load testing
- [ ] **Milestone 7:** Execute custom Python load testing
- [ ] **Milestone 7:** Generate performance graphs and benchmark report

---

# Current Service Status

| Service | Port | Docker | REST API | Status |
| :--- | :---: | :---: | :---: | :---: |
| Event Service | 5001 | Yes | Yes | Active |
| User Service | 5002 | Yes | Yes | Active |
| Seat Service | 5003 | Yes | Yes | Active |
| Booking Service | 5004 | Yes | Yes | Active |
| Payment Service | 5005 | Yes | Yes | Active |
| API Gateway | 8000 | Planned | Planned | Planned |

---

# Academic Context

**Course:** Cloud Computing Laboratory (CCLab) — Semester 5

**Institution:** KLE Technological University

**Project:** Movie & Concert Ticket Booking System

**Focus Areas:**

- Microservices Architecture
- RESTful APIs
- Docker Containerization
- Inter-Service Communication
- Service Discovery
- Docker Networking
- Docker Compose
- Load Testing
- Performance Benchmarking
- Distributed System Design

---

## Team Contributions

The project is developed collaboratively with individual microservices and system components implemented by different team members.

### Services Implemented

- **Event Service**
- **User Service**
- **Seat Service**
- **Booking Service**
- **Payment Service**

### Upcoming System Components

- API Gateway
- Docker Compose orchestration
- Locust performance testing
- Custom Python load generator
- Performance analysis and visualization
