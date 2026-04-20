# 📝 Flask Blog Application

A full-stack **CRUD blog application** built with Flask, containerized with Docker, and deployed automatically via a GitHub Actions CI/CD pipeline. Built as a DevOps learning project to demonstrate real-world software engineering practices.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python) ![Flask](https://img.shields.io/badge/Flask-3.0-black?logo=flask)  ![Docker](https://img.shields.io/badge/Docker-Containerized-blue?logo=docker) ![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-orange?logo=githubactions)

---

## 🖼️ Preview

The app allows users to create, read, update, and delete blog posts through a clean web interface. Each post includes a title, content, author name, and timestamp.

---

## ✨ Features

- **Create** new blog posts with title, content, and author
- **Read** all posts on the homepage or view a single post in full
- **Update** existing posts through an edit form
- **Delete** posts with a confirmation prompt
- **REST API** endpoints for all CRUD operations
- **Health check** endpoint at `/health`
- **Automated tests** covering all routes and API endpoints
- **Docker support** for one-command local setup
- **CI/CD pipeline** that builds, tests, and pushes to Docker Hub on every push to `main`

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11, Flask |
| Database | PostgreSQL 15 |
| ORM | Flask-SQLAlchemy |
| Containerization | Docker, Docker Compose |
| CI/CD | GitHub Actions |
| Testing | pytest |
| Production Server | Gunicorn |

---

## 📁 Project Structure

```
Blog_application/
├── app/                        # Application package
├── tests/                      # Unit tests
├── .github/
│   └── workflows/
│       └── ci-cd.yml           # GitHub Actions pipeline
├── app.py                      # Flask application entry point
├── docker-compose.yml          # Multi-service orchestration
├── Dockerfile                  # Container image definition
├── docker-entrypoint.sh        # Container startup script
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variable template
└── README.md
```

---

## ⚡ Quick Start

### Option 1: Docker (Recommended)

The easiest way — no need to install Python or PostgreSQL manually.

```bash
# Clone the repo
git clone https://github.com/manches3003/Blog_application.git
cd Blog_application

# Copy environment variables
cp .env.example .env

# Start the app (Flask + PostgreSQL)
docker-compose up --build

# Visit the app
open http://localhost:5000
```

To stop: `docker-compose down`

### Option 2: Run Locally

```bash
# Clone the repo
git clone https://github.com/manches3003/Blog_application.git
cd Blog_application

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/flask_blog_dev
export FLASK_ENV=development

# Run database migrations
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Start the app
python app.py
```

Visit `http://localhost:5000`

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/posts` | List all posts |
| `GET` | `/api/posts/<id>` | Get a single post |
| `POST` | `/api/posts` | Create a new post |
| `PUT` | `/api/posts/<id>` | Update an existing post |
| `DELETE` | `/api/posts/<id>` | Delete a post |
| `GET` | `/health` | Health check |

**Example — create a post:**
```bash
curl -X POST http://localhost:5000/api/posts \
  -H "Content-Type: application/json" \
  -d '{"title": "Hello World", "content": "My first post!", "author": "John"}'
```

---

## 🧪 Running Tests

Tests use an in-memory SQLite database — no PostgreSQL required.

```bash
pip install pytest
DATABASE_URL=sqlite:///:memory: pytest tests/ -v
```

---

## 🔄 CI/CD Pipeline

Every push to the `main` branch automatically triggers a three-stage GitHub Actions pipeline:

```
Push to main
     │
     ▼
┌────────────────┐
│ Build & Test   │  ← Install deps, run pytest, build Docker image
└───────┬────────┘
        │
        ▼
┌────────────────┐
│ Push Docker Hub│  ← Push image tagged :latest and :<git-sha>
└───────┬────────┘
        │
        ▼
┌────────────────┐
│ Security Scan  │  ← Check dependencies for vulnerabilities
└────────────────┘
```

### Setting up Docker Hub deployment

1. Create a free account at [hub.docker.com](https://hub.docker.com)
2. Generate an Access Token: **Account Settings → Security → New Access Token**
3. Add secrets to your GitHub repo: **Settings → Secrets → Actions**
   - `DOCKER_USERNAME` — your Docker Hub username
   - `DOCKER_PASSWORD` — your Access Token

---

## 🐳 DevOps Concepts Demonstrated

| Concept | Implementation |
|---------|---------------|
| Containerization | App packaged with all dependencies in Docker |
| Orchestration | Docker Compose manages Flask + PostgreSQL together |
| CI/CD | Automated build → test → deploy on every push |
| Infrastructure as Code | All config stored in version-controlled files |
| Health Checks | `/health` endpoint + Docker `HEALTHCHECK` directive |
| Environment Variables | Secrets kept out of code via `.env` files |
| Automated Testing | Tests run before every deployment |
| Image Versioning | Images tagged with `latest` and git commit SHA |
| Security Scanning | Dependency vulnerability detection with `safety` |

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
