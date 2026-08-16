# 📝 Containerized Full-Stack To-Do Application

A production-ready **Full-Stack To-Do Management Application** built with **Python, MySQL, Docker, Docker Compose, Nginx, and GitHub Actions**.

The project demonstrates containerization, persistent database storage, secure configuration, health checks, CI/CD automation, Docker Hub integration, logging, and production-oriented deployment practices.

---

## 📌 Project Overview

This project contains:

- 🐍 Python Flask To-Do application
- 🗄️ MySQL database
- 🐳 Docker containers
- 🔀 Nginx reverse proxy
- 💾 Persistent MySQL volume
- 🌐 Custom Docker network
- 🔐 Environment-based configuration
- 👤 Non-root application container
- ❤️ Docker health checks
- 🚀 GitHub Actions CI/CD
- 📦 Docker Hub image publishing
- 🔍 Code quality and unit testing
- 🛡️ Dependency and image security scanning
- 📋 Application and container logging

---

## 🏗️ Architecture

```text
                         ┌──────────────────────┐
                         │       Browser        │
                         │   http://localhost   │
                         └──────────┬───────────┘
                                    │
                                    │ HTTP :80
                                    ▼
                         ┌──────────────────────┐
                         │    Nginx Container   │
                         │   Reverse Proxy      │
                         └──────────┬───────────┘
                                    │
                                    │ HTTP
                                    ▼
                         ┌──────────────────────┐
                         │   Flask App          │
                         │   Python + Gunicorn  │
                         │   Non-root User      │
                         └──────────┬───────────┘
                                    │
                                    │ MySQL :3306
                                    ▼
                         ┌──────────────────────┐
                         │    MySQL Container   │
                         │      MySQL 8.4       │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    Docker Volume     │
                         │     mysql_data       │
                         └──────────────────────┘


              ┌────────────────────────────────────┐
              │       Docker Network               │
              │        todo-network                │
              │                                    │
              │  Nginx → Flask → MySQL             │
              └────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript / Flask Templates |
| Backend | Python, Flask |
| WSGI Server | Gunicorn |
| Database | MySQL 8.4 |
| Reverse Proxy | Nginx |
| Containerization | Docker |
| Orchestration | Docker Compose |
| CI/CD | GitHub Actions |
| Image Registry | Docker Hub |
| Testing | Pytest |
| Code Quality | Flake8 |
| Database Driver | PyMySQL / SQLAlchemy |
| Operating System | Linux / WSL / Docker Desktop |

---

# 📁 Project Structure

```text
python-todo/
│
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   ├── database.py
│   └── templates/
│       └── index.html
│
├── tests/
│   └── test_app.py
│
├── init-db/
│   └── init.sql
│
├── nginx/
│   └── nginx.conf
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml
│
├── .dockerignore
├── .env
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── run.py
└── README.md
```

---

# 🚀 Application Features

The To-Do application supports:

- Create a task
- View tasks
- Update task status
- Delete tasks
- Store tasks in MySQL
- Persistent database storage
- Web-based interface
- REST-style backend routes
- Application health check
- Container health monitoring

---

# 🐳 Dockerization

## Application Container

The application uses a **multi-stage Dockerfile**.

Benefits:

- Smaller final image
- Reduced unnecessary dependencies
- Better security
- Faster deployment
- Separation between build and runtime environments

The application container also:

- Runs as a non-root user
- Uses Gunicorn
- Loads configuration from environment variables
- Includes a health check
- Uses a minimal Python base image

Example:

```dockerfile
FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /install /usr/local

COPY . .

RUN useradd -m appuser

USER appuser

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
```

---

# 🗄️ MySQL Database

The MySQL container uses:

```text
mysql:8.4
```

Database data is stored in a Docker named volume.

```yaml
volumes:
  mysql_data:
```

This ensures that database data survives container recreation.

Example:

```text
Container
   │
   ▼
MySQL
   │
   ▼
mysql_data volume
```

---

# 🔐 Environment Configuration

Sensitive configuration is stored using environment variables.

Example `.env`:

```env
MYSQL_ROOT_PASSWORD=your_root_password
MYSQL_DATABASE=todo_db
MYSQL_USER=todo_user
MYSQL_PASSWORD=your_database_password

DB_HOST=mysql
DB_PORT=3306

FLASK_ENV=production
```

> **Important:** Never commit `.env` containing real passwords to GitHub.

Add it to `.gitignore`:

```gitignore
.env
__pycache__/
*.pyc
```

Provide an example configuration through:

```text
.env.example
```

---

# 🌐 Docker Compose

Docker Compose manages the complete application stack.

Services:

```text
nginx
   │
   ▼
todo-app
   │
   ▼
todo-mysql
```

Start all services:

```bash
docker compose up -d
```

Check containers:

```bash
docker compose ps
```

View logs:

```bash
docker compose logs
```

View application logs:

```bash
docker compose logs todo-app
```

View MySQL logs:

```bash
docker compose logs todo-mysql
```

View Nginx logs:

```bash
docker compose logs todo-nginx
```

---

# ❤️ Health Checks

Health checks are configured for the application and database.

Example application health endpoint:

```text
GET /health
```

Expected response:

```text
SUCCESS
```

Check container health:

```bash
docker ps
```

Example:

```text
todo-app      Up (healthy)
todo-mysql    Up (healthy)
todo-nginx    Up
```

Health checks allow Docker Compose to understand whether services are ready to accept traffic.

---

# 🌐 Access the Application

After starting the containers:

```bash
docker compose up -d
```

Open:

```text
http://localhost
```

The request flow is:

```text
Browser
   ↓
Nginx :80
   ↓
Flask :5000
   ↓
MySQL :3306
```

---

# 🧪 Testing

Run unit tests locally:

```bash
pytest
```

Run tests with verbose output:

```bash
pytest -v
```

Example:

```text
================ test session starts ================
tests/test_app.py .....
================ 5 passed ===========================
```

---

# 🔎 Code Quality

Run Flake8:

```bash
flake8 .
```

Code quality checks are automatically executed through GitHub Actions.

---

# 🔄 CI/CD Pipeline

GitHub Actions automatically performs the following:

```text
Git Push
   │
   ▼
GitHub Actions
   │
   ├── Checkout Code
   │
   ├── Setup Python
   │
   ├── Install Dependencies
   │
   ├── Code Quality Check
   │
   ├── Run Unit Tests
   │
   ├── Build Docker Image
   │
   ├── Security Scan
   │
   ├── Login to Docker Hub
   │
   └── Push Docker Image
```

Pipeline file:

```text
.github/workflows/ci-cd.yml
```

---

# 🐳 Docker Hub

The application image is published to Docker Hub.

Example repository:

```text
username/todo-app
```

## Build Image

```bash
docker build -t username/todo-app:v1.0 .
```

## Tag Latest

```bash
docker tag username/todo-app:v1.0 username/todo-app:latest
```

## Login

```bash
docker login
```

## Push Version

```bash
docker push username/todo-app:v1.0
```

## Push Latest

```bash
docker push username/todo-app:latest
```

---

# 📦 Pull Image From Another Host

On another Docker-enabled machine:

```bash
docker pull username/todo-app:v1.0
```

Verify:

```bash
docker images
```

Run the image:

```bash
docker run -d \
  --name todo-app \
  -p 5000:5000 \
  username/todo-app:v1.0
```

Test:

```bash
curl http://localhost:5000/health
```

Expected:

```text
SUCCESS
```

---

# 🔒 Security

The project implements several security practices.

### Non-root Container

The Flask application does not run as root.

```dockerfile
USER appuser
```

### Environment Variables

Credentials are loaded from `.env` instead of being hard-coded into the application.

### Docker Secrets / GitHub Secrets

Docker Hub credentials should be stored securely in GitHub repository secrets.

Example:

```text
DOCKERHUB_USERNAME
DOCKERHUB_TOKEN
```

### Dependency Scanning

Python dependencies can be scanned for known vulnerabilities.

Example:

```bash
pip-audit
```

### Docker Image Scanning

The Docker image can be scanned using tools such as:

```bash
docker scout cves username/todo-app:v1.0
```

---

# 💾 Persistent Storage

MySQL uses a named Docker volume:

```text
mysql_data
```

List volumes:

```bash
docker volume ls
```

Inspect the volume:

```bash
docker volume inspect python-todo_mysql_data
```

Because database data is stored outside the container's writable layer, removing and recreating the MySQL container does not automatically remove the database data.

---

# 🗃️ Database Initialization

Initialization scripts are stored in:

```text
init-db/
```

Example:

```text
init-db/
└── init.sql
```

The script is mounted into MySQL:

```yaml
volumes:
  - ./init-db:/docker-entrypoint-initdb.d
```

MySQL executes initialization scripts when the database is initialized.

---

# 📋 Logging

View all Compose logs:

```bash
docker compose logs
```

Follow logs in real time:

```bash
docker compose logs -f
```

Application logs:

```bash
docker compose logs -f todo-app
```

Nginx logs:

```bash
docker compose logs -f todo-nginx
```

MySQL logs:

```bash
docker compose logs -f todo-mysql
```

Container-specific logs:

```bash
docker logs todo-app
```

---

# 🔍 Useful Docker Commands

### Check Running Containers

```bash
docker ps
```

### Check All Containers

```bash
docker ps -a
```

### Check Images

```bash
docker images
```

### Check Networks

```bash
docker network ls
```

### Inspect Network

```bash
docker network inspect python-todo_todo-network
```

### Check Volumes

```bash
docker volume ls
```

### Stop Application

```bash
docker compose down
```

### Stop and Remove Volumes

```bash
docker compose down -v
```

> ⚠️ `docker compose down -v` removes the database volume and therefore deletes the stored MySQL data.

### Rebuild Containers

```bash
docker compose build --no-cache
```

### Start Again

```bash
docker compose up -d
```

---

# 🔁 Complete Deployment

Clone the repository:

```bash
git clone https://github.com/USERNAME/python-todo.git
```

Enter the project:

```bash
cd python-todo
```

Create environment file:

```bash
cp .env.example .env
```

Edit the configuration:

```bash
nano .env
```

Build the images:

```bash
docker compose build
```

Start the application:

```bash
docker compose up -d
```

Check status:

```bash
docker compose ps
```

Test:

```bash
curl http://localhost/
```

Open in a browser:

```text
http://localhost
```

---

# 🧹 Cleanup

Stop containers:

```bash
docker compose down
```

Remove containers and volumes:

```bash
docker compose down -v
```

Remove unused Docker resources:

```bash
docker system prune
```

> Use `docker system prune` carefully because it can remove unused Docker resources.

---

# 📊 Monitoring

The project provides basic monitoring through:

- Docker health checks
- Container status
- Docker logs
- Application health endpoint
- MySQL health status

Optional monitoring can be added using:

```text
Prometheus
Grafana
Node Exporter
cAdvisor
```

Possible monitoring architecture:

```text
                    ┌──────────────┐
                    │   Grafana    │
                    └──────▲───────┘
                           │
                    ┌──────┴───────┐
                    │  Prometheus  │
                    └──────▲───────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
          Flask App      MySQL       Docker
```

---

# 🎯 Project Requirements Checklist

- [x] Python To-Do application
- [x] MySQL database
- [x] Dockerized application
- [x] Multi-stage Dockerfile
- [x] Non-root application user
- [x] Environment-based configuration
- [x] Application health check
- [x] MySQL health check
- [x] Persistent MySQL volume
- [x] Database initialization scripts
- [x] Docker Compose
- [x] Nginx reverse proxy
- [x] Custom Docker network
- [x] Unit tests
- [x] Code quality checks
- [x] GitHub Actions CI/CD
- [x] Docker Hub integration
- [x] Versioned Docker image tags
- [x] `latest` Docker image tag
- [x] Non-root execution
- [x] Dependency scanning
- [x] Image vulnerability scanning
- [x] Container logging
- [x] Health monitoring
- [x] Project documentation
- [ ] Optional Prometheus integration
- [ ] Optional Grafana integration

---

# 💡 What This Project Demonstrates

This project demonstrates practical DevOps and full-stack deployment concepts:

**Application Development**

```text
Python + Flask + MySQL
```

**Containerization**

```text
Docker + Dockerfile
```

**Container Orchestration**

```text
Docker Compose
```

**Networking**

```text
Nginx → Flask → MySQL
```

**Storage**

```text
Docker Named Volume
```

**Security**

```text
Non-root User
Environment Variables
Secrets
Vulnerability Scanning
```

**CI/CD**

```text
GitHub
   ↓
GitHub Actions
   ↓
Test
   ↓
Build
   ↓
Scan
   ↓
Docker Hub
```

---

# 🏆 Project Outcome

The final system provides a containerized To-Do application that can be developed locally, tested automatically, built into a Docker image, published to Docker Hub, and deployed on another Docker-enabled host.

The architecture separates the **web proxy, application, and database layers**, while Docker networking provides service-to-service communication and persistent storage protects the database from container recreation.

---

## 👨‍💻 Author

**Aravind S**

### Project

**Containerized Full-Stack To-Do Application**

### Technologies

```text
Python | Flask | MySQL | Docker | Docker Compose
Nginx | GitHub Actions | Docker Hub | Linux
```