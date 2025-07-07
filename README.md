![CI](https://github.com/Kkasuga904/fastapi-docker-example/actions/workflows/ci.yml/badge.svg)

# 🚀 FastAPI Docker Example

A minimal example project with **FastAPI + Docker + GitHub Actions (CI/CD)**, ready for cloud-native deployment.

## ✅ Features

- ⚡ FastAPI — ultra-fast web framework
- 🐳 Docker — containerized for portability
- ✅ GitHub Actions — CI pipeline included
- 🧪 Pytest — test included
- 🖥️ curl / Swagger demo output

---

## 📦 Project Structure

```text
.
├── app/
│   └── main.py             # FastAPI app
├── test_main.py            # Simple test (Pytest)
├── Dockerfile              # Production-ready container
├── docker-compose.yml      # Local setup
├── .github/workflows/ci.yml# GitHub Actions CI
└── README.md
🐋 How to Run
bash
Copy
Edit
docker build -t fastapi-app .
docker run -d -p 8000:8000 fastapi-app
curl http://localhost:8000
Expected output:

json
Copy
Edit
{"message": "Hello, world"}
🧪 How to Test
bash
Copy
Edit
pytest test_main.py
🖼️ Screenshot


💡 Use Cases
This template is ideal for:

Portfolio Projects

Docker CI/CD practice

FastAPI microservices

Freelancer starter kits