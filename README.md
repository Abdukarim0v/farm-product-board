🌾 Farm Product Board – DevOps Microservices Project
This repository contains a real-world DevOps-style microservices project built as part of a Level 6 DevOps assignment. The project demonstrates containerization, service orchestration, CI/CD, persistence, messaging, and rollback strategies using practical tools.

🚀 Project Overview
The system simulates a small agriculture trading platform where:

Farmers manage products

Markets place orders

Notifications are sent asynchronously

Product price changes are tracked

All services are Dockerized, orchestrated with Docker Compose, and validated through GitHub Actions CI.

🧩 Architecture
Services included:

Farm Product Board (Task 1)

Frontend (Nginx – static UI)

Backend (Flask REST API)

SQLite database (persistent volume)

Nginx reverse proxy (gateway)

Order Notification System (Task 2)

Orders API (Flask)

Redis (message queue)

Notifier Worker (Node.js)

Price Tracker Service (Task 3)

Flask REST API

SQLite persistence

CI/CD

GitHub Actions

Docker image builds

Rollback demonstration (tag + revert)

🛠 Tech Stack
Backend: Python (Flask)

Frontend: HTML + Nginx

Messaging: Redis

Worker: Node.js

Containers: Docker, Docker Compose

CI/CD: GitHub Actions

Database: SQLite (volumes)

▶️ How to Run the Project
All commands should be run from the deploy/ directory.

🔹 Task 1 – Farm Product Board
docker compose -f docker-compose.local.yml up -d --build
Access:

UI: http://localhost:8080

Health: GET /api/health

Products: GET /api/products, POST /api/products

🔹 Task 2 – Orders + Notifications
docker compose -f docker-compose.task2.yml up -d --build
Endpoints:

Health: http://localhost:6000/health

Create Order: POST http://localhost:6000/orders

Notifier logs:

docker logs deploy-notifier-1
🔹 Task 3 – Price Tracker
docker compose -f docker-compose.task3.yml up -d --build
Endpoints:

Health: http://localhost:7000/health

Price Changes: GET /price-changes, POST /price-changes

🔁 CI/CD and Rollback
GitHub Actions builds Docker images on each push

A stable release was tagged: v1.0-task3

A faulty commit was intentionally introduced

Rollback was performed using git revert

CI pipeline returned to green state

This demonstrates versioning and rollback in practice.

📸 Evidence (for submission)
Recommended screenshots:

GitHub Actions – green pipeline + rollback

docker ps showing all services running

Product API responses

Order queued + notifier logs

Price tracker API responses

✅ Learning Outcomes Covered
LO1: DevOps practices, containerization, automation

LO2: CI/CD pipelines, monitoring, rollback strategies

👤 Author
Abdukarimov
DevOps Assignment – 2025/2026

✅ This project is fully functional and ready for assessment.
