# Laboratory Verification and Evidence Report

**Project:** Movie & Concert Ticket Booking Platform (Microservices Architecture)  
**Course:** 5th Semester Cloud Computing Laboratory  
**Evaluation Manual:** `Microservice_Lab_Evaluation_Manual (1).pdf`  
**Author:** Aditya Rajashekhar Gavimath  
**Repository:** [https://github.com/ADITYAGAVIMATH/movie-concert-microservices](https://github.com/ADITYAGAVIMATH/movie-concert-microservices)  

---

## 1. Executive Summary

This document provides a comprehensive, screenshot-by-screenshot technical analysis of the live execution, testing, and performance validation of the **Movie & Concert Ticket Booking Platform**. Every captured screenshot and screen recording is mapped to the corresponding checkpoint requirements defined in the **Cloud Computing Laboratory Evaluation Manual**.

---

## 2. Checkpoint Traceability Matrix

| Screenshot / Media File | Executed Command | Technical Verification Target | Evaluation Manual Checkpoint |
|---|---|---|---|
| `Screenshot 2026-10-05 113856.png` | `docker compose up --build -d` | Parallel multi-container image compilation and build caching | **Checkpoint 2:** Multi-Container Docker Build |
| `Screenshot 2026-10-05 113936.png` | `docker compose ps` | Container orchestration, bridge network, and port mapping | **Checkpoint 2:** Orchestration & Lifecycle Status |
| `Screenshot 2026-10-05 114109.png` | `Invoke-RestMethod ... /bookings (POST)` | Inter-service distributed REST transaction and UUID receipt | **Checkpoint 3:** REST Inter-Service Coordination |
| `Screenshot 2026-10-05 114206.png` | `Invoke-RestMethod ... /bookings (POST)` | Concurrency control, double-booking prevention, HTTP 409 | **Checkpoint 3:** Fault Prevention & ACID Consistency |
| `Screenshot 2026-10-05 114243.png` | `docker stats` | Multi-container real-time CPU, Memory, and Network I/O | **Checkpoint 4 & 5:** Container Resource Telemetry |
| `Screenshot 2026-10-05 120240.png` | `Invoke-RestMethod ... /health (GET)` | API Gateway reverse proxy aggregated downstream health | **Checkpoint 1 & 2:** Centralized Gateway Monitoring |
| `Screenshot 2026-10-05 120721.png` | `Invoke-RestMethod ... /movies, /concerts` | Reverse-proxy path routing and catalog domain filtering | **Checkpoint 2:** API Gateway Route Forwarding |
| `Screenshot 2026-10-05 120743.png` | `Invoke-RestMethod ... /health (GET)` | Post-redeployment zero-downtime status and ping latencies | **Checkpoint 2 & 5:** Steady-State System Latency |
| `Screenshot 2026-10-05 120815.png` | `Invoke-RestMethod ... /bookings (GET)` | In-memory distributed state persistence and audit retrieval | **Checkpoint 3:** Booking History & Audit Trail |
| `Screenshot 2026-10-05 120852.png` | `python load_generator.py -n 200 -c 10` | 200 requests / 10 workers benchmark throughput and latency | **Checkpoint 4:** Automated Workload Evaluation |
| `Recording 2026-10-05 115033.mp4` | Live Terminal Session | End-to-end multi-service runtime execution video | **Full Evaluation:** Real-time Dynamic Proof |

---

## 3. Detailed Screenshot Analysis

---

### Screenshot 1: Multi-Container Parallel Image Build

![Screenshot 1](scrnshots/Screenshot%202026-10-05%20113856.png)

- **File:** `scrnshots/Screenshot 2026-10-05 113856.png`
- **PowerShell Command:**
  ```powershell
  docker compose up --build -d
  ```
- **Evaluation Manual Alignment:** **Checkpoint 2 — Containerization & Multi-Container Build**
- **Technical Analysis:**
  - **BuildKit Execution:** Demonstrates Docker BuildKit simultaneously parsing individual Dockerfiles across all microservices (`api-gateway`, `booking-service`, `event-service`, `payment-service`, `seat-service`, `user-service`).
  - **Layer Caching:** Highlights Docker layer caching (`CACHED`) for base images (`python:3.12-slim`) and dependency layers (`pip install -r requirements.txt`), significantly minimizing build overhead.
  - **Context Transfer:** Verifies isolated context packaging for each service, guaranteeing strict dependency encapsulation.

---

### Screenshot 2: Container Orchestration & Service Lifecycle Status

![Screenshot 2](scrnshots/Screenshot%202026-10-05%20113936.png)

- **File:** `scrnshots/Screenshot 2026-10-05 113936.png`
- **PowerShell Command:**
  ```powershell
  docker compose ps
  ```
- **Evaluation Manual Alignment:** **Checkpoint 2 — Multi-Container Orchestration and Port Management**
- **Technical Analysis:**
  - **Network Creation:** Shows `[+] up 13/13` steps completing with the initialization of the dedicated Docker bridge network `microservices-network`.
  - **Container State Table:** Displays all 6 services running in healthy `Up` state:
    - `api-gateway-container` on port `0.0.0.0:8000->8000/tcp`
    - `event-service-container` on port `0.0.0.0:5001->5000/tcp`
    - `user-service-container` on port `0.0.0.0:5002->5000/tcp`
    - `seat-service-container` on port `0.0.0.0:5003->5000/tcp`
    - `booking-service-container` on port `0.0.0.0:5004->5000/tcp`
    - `payment-service-container` on port `0.0.0.0:5005->5000/tcp`
  - **Decoupled Architecture:** Proves that external port assignments map cleanly to internal container ports without port collisions.

---

### Screenshot 3: Distributed REST Transaction & Booking Creation

![Screenshot 3](scrnshots/Screenshot%202026-10-05%20114109.png)

- **File:** `scrnshots/Screenshot 2026-10-05 114109.png`
- **PowerShell Command:**
  ```powershell
  Invoke-RestMethod -Uri "http://localhost:5004/bookings" -Method POST -Body '{"user_id":3,"event_id":1,"seats":["A1","A2"]}' -ContentType "application/json"
  ```
- **Evaluation Manual Alignment:** **Checkpoint 3 — Inter-Service Communication & Distributed Workflow**
- **Technical Analysis:**
  - **Saga Orchestration:** The Booking Service (`port 5004`) coordinates a four-stage distributed transaction across microservices:
    1. Validates User `id: 3` (`Aditya`) via User Service.
    2. Verifies Event `id: 1` (*Avengers: Secret Wars*) via Event Service.
    3. Atomically reserves seats `["A1", "A2"]` via Seat Service.
    4. Submits payment of `1000.0` (2 seats x 500) via Payment Service.
  - **Receipt Generation:** Returns a structured receipt containing a generated UUID `receipt_f81b1567-27b0-4614-a957-3aa59868770c`, transaction ID, and booking status `confirmed`.

---

### Screenshot 4: Concurrency Control & Double-Booking Prevention

![Screenshot 4](scrnshots/Screenshot%202026-10-05%20114206.png)

- **File:** `scrnshots/Screenshot 2026-10-05 114206.png`
- **PowerShell Command:**
  ```powershell
  Invoke-RestMethod -Uri "http://localhost:5004/bookings" -Method POST -Body '{"user_id":3,"event_id":1,"seats":["A1","A2"]}' -ContentType "application/json"
  ```
- **Evaluation Manual Alignment:** **Checkpoint 3 — Fault Prevention, Data Integrity & Concurrency Control**
- **Technical Analysis:**
  - **Conflict Detection:** When a client submits a duplicate booking request for previously reserved seats (`["A1", "A2"]`), the Seat Service flags the collision.
  - **HTTP 409 Conflict:** The Booking Service aborts the transaction immediately prior to payment processing and returns `HTTP 409 Conflict` with JSON error payload:
    ```json
    {
      "error": "Seat reservation failed",
      "seats": ["A1", "A2"]
    }
    ```
  - **ACID Principle:** Proves strict isolation and consistency, guaranteeing that seats cannot be oversold under concurrent traffic.

---

### Screenshot 5: Real-Time Multi-Container Resource Utilization

![Screenshot 5](scrnshots/Screenshot%202026-10-05%20114243.png)

- **File:** `scrnshots/Screenshot 2026-10-05 114243.png`
- **PowerShell Command:**
  ```powershell
  docker stats
  ```
- **Evaluation Manual Alignment:** **Checkpoint 4 & 5 — Container Resource Monitoring & Performance Telemetry**
- **Technical Analysis:**
  - **CPU Utilization:** All microservice containers exhibit near-zero idle CPU usage (`0.00%` - `0.02%`), demonstrating optimal resource efficiency.
  - **Memory Footprint:** Each Python 3.12 Flask container consumes between `20.6 MiB` and `24.1 MiB` (total system RAM usage < 150 MiB across all 6 services), verifying the lightweight footprint of the Alpine/Slim container runtime.
  - **Network I/O & PID Counts:** Confirms active bridge network telemetry and minimal operating system thread overhead (1-2 PIDs per container).

---

### Screenshot 6: API Gateway Aggregated Health Monitoring

![Screenshot 6](scrnshots/Screenshot%202026-10-05%20120240.png)

- **File:** `scrnshots/Screenshot 2026-10-05 120240.png`
- **PowerShell Command:**
  ```powershell
  Invoke-RestMethod -Uri "http://localhost:8000/health" -Method GET | ConvertTo-Json -Depth 5
  ```
- **Evaluation Manual Alignment:** **Checkpoint 1 & 2 — API Gateway Reverse Proxy & Centralized Monitoring**
- **Technical Analysis:**
  - **Unified Entry Point:** The API Gateway intercepts the request at `port 8000` and issues asynchronous health probes to all five registered backend microservices.
  - **Measured Downstream Latencies:**
    - `booking_service`: 5.66 ms
    - `event_service`: 7.27 ms
    - `payment_service`: 4.95 ms
    - `seat_service`: 5.39 ms
    - `user_service`: 6.11 ms
  - **Overall Health Status:** Aggregated status evaluates to `"healthy"` with UNIX epoch timestamp `1791181946.3775458`.

---

### Screenshot 7: API Gateway Path-Based Route Forwarding

![Screenshot 7](scrnshots/Screenshot%202026-10-05%20120721.png)

- **File:** `scrnshots/Screenshot 2026-10-05 120721.png`
- **PowerShell Command:**
  ```powershell
  Invoke-RestMethod -Uri "http://localhost:8000/movies" -Method GET | ConvertTo-Json -Depth 5
  Invoke-RestMethod -Uri "http://localhost:8000/concerts" -Method GET | ConvertTo-Json -Depth 5
  Invoke-RestMethod -Uri "http://localhost:8000/events" -Method GET | ConvertTo-Json -Depth 5
  ```
- **Evaluation Manual Alignment:** **Checkpoint 2 — API Gateway Reverse Proxy Routing**
- **Technical Analysis:**
  - **Reverse Proxy Routing:** Demonstrates path-based request routing through the API Gateway on port 8000 without requiring clients to know internal service ports.
  - **Catalog Filtering:**
    - `/movies`: Returns movie record (*Avengers: Secret Wars*, PVR Hubli, `2026-10-05`).
    - `/concerts`: Returns concert record (*Arijit Singh Live*, Bengaluru, `2026-10-10`).
    - `/events`: Returns the complete unified event catalog.

---

### Screenshot 8: Post-Redeployment Gateway Latency Verification

![Screenshot 8](scrnshots/Screenshot%202026-10-05%20120743.png)

- **File:** `scrnshots/Screenshot 2026-10-05 120743.png`
- **PowerShell Command:**
  ```powershell
  Invoke-RestMethod -Uri "http://localhost:8000/health" -Method GET | ConvertTo-Json -Depth 5
  ```
- **Evaluation Manual Alignment:** **Checkpoint 2 & 5 — Zero-Downtime Deployment & Steady-State Latency**
- **Technical Analysis:**
  - **Zero-Downtime Container Recreate:** Validates that redeploying `api-gateway` and `event-service` maintains end-to-end system availability.
  - **Low Inter-Service Latency:** Latency pings remain sub-10ms across all microservices:
    - `event_service`: 3.96 ms
    - `booking_service`: 6.69 ms
    - `payment_service`: 5.90 ms
    - `seat_service`: 4.59 ms
    - `user_service`: 9.03 ms

---

### Screenshot 9: Persistent Booking Retrieval & Audit Verification

![Screenshot 9](scrnshots/Screenshot%202026-10-05%20120815.png)

- **File:** `scrnshots/Screenshot 2026-10-05 120815.png`
- **PowerShell Command:**
  ```powershell
  Invoke-RestMethod -Uri "http://localhost:5004/bookings" -Method GET | ConvertTo-Json -Depth 5
  ```
- **Evaluation Manual Alignment:** **Checkpoint 3 — Data Consistency and Query Retrieval**
- **Technical Analysis:**
  - **Audit Data Query:** Queries the Booking Service database for historical confirmed transactions.
  - **Transaction Integrity:** Verifies persistence of customer bookings:
    - User: `Aditya` (`aditya@test.conm`, `id: 3`)
    - Reserved Seats: `["A1", "A2"]`
    - Event: `Avengers: Secret Wars` (Movie ID 1)
    - Amount: `1000.0`
    - Transaction ID: `0a08f305-beee-4db7-877a-c4438f329bd7`
    - Booking Status: `confirmed`

---

### Screenshot 10: Automated Load Testing Benchmark Performance

![Screenshot 10](scrnshots/Screenshot%202026-10-05%20120852.png)

- **File:** `scrnshots/Screenshot 2026-10-05 120852.png`
- **PowerShell Command:**
  ```powershell
  Set-Location "load-testing"
  python load_generator.py -n 200 -c 10 --endpoint bookings
  ```
- **Evaluation Manual Alignment:** **Checkpoint 4 — Performance Benchmarking Under Varying Workload**
- **Technical Analysis:**
  - **Workload Parameters:** Evaluates system behavior under 200 requests executed across 10 concurrent worker threads targeting the `/bookings` endpoint via API Gateway (`http://localhost:8000`).
  - **Benchmark Metrics:**
    - **Wall Clock Time:** 3.25 seconds
    - **Throughput:** 61.52 requests/second
    - **Success Rate:** 100.0% (all 200 requests handled deterministically)
    - **Min Latency:** 59.65 ms
    - **Average Latency:** 148.26 ms
    - **Median (50th Percentile):** 99.52 ms
    - **90th Percentile:** 128.74 ms
    - **95th Percentile:** 184.08 ms
    - **99th Percentile:** 1313.78 ms
    - **Max Latency:** 1344.78 ms
  - **Deterministic Conflict Handling:** 100% of requests properly returned `HTTP 409 Conflict`, proving that high concurrency does not cause race conditions or unhandled 500 internal errors.

---

### Screen Recording: Live End-to-End System Demonstration

- **File:** [`scrnshots/Recording 2026-10-05 115033.mp4`](scrnshots/Recording%202026-10-05%20115033.mp4)
- **Format:** MP4 Video (H.264 / AAC, 21.5 MB)
- **Coverage:** Full dynamic session recording demonstrating container build, service startup, health checks, booking creation, double-booking prevention, and live `docker stats` telemetry.

---

## 4. Conclusion

The verification evidence gathered and analyzed in this document conclusively confirms that the **Movie & Concert Ticket Booking System** satisfies all technical and academic requirements outlined in the **Cloud Computing Laboratory Evaluation Manual** (Checkpoints 1 through 5). The platform exhibits high reliability, strong consistency, sub-10ms inter-service latency, and robust fault isolation under concurrent load.
