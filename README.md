# Flask Blog Application

A Flask-based blog application deployed on Kubernetes (minikube) with PostgreSQL database, CI/CD pipeline via GitHub Actions, and Docker containerization.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-black?logo=flask)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue?logo=docker)
![Kubernetes](https://img.shields.io/badge/Kubernetes-minikube-326ce5?logo=kubernetes)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-orange?logo=githubactions)

---

## Overview

This is a full-stack blog application that allows users to create, read, update, and delete blog posts. The application follows a modular architecture with separate routes for API and web interfaces, uses SQLAlchemy ORM for database operations, and is containerized for easy deployment on Kubernetes.

### Features

- **CRUD Operations**: Create, read, update, and delete blog posts
- **RESTful API**: JSON-based API endpoints for blog operations
- **PostgreSQL Database**: Persistent storage with SQLAlchemy ORM
- **Docker Containerized**: Multi-stage Docker build with gunicorn WSGI server
- **Kubernetes Deployment**: Production-ready manifests for minikube
- **CI/CD Pipeline**: GitHub Actions for automated build and deployment
- **Health Checks**: Liveness and readiness probes for container health monitoring
- **Secrets Management**: Kubernetes secrets for sensitive configuration

---

## Project Structure

```
flask-blog/
├── app/                          # Flask application package
│   ├── __init__.py              # App factory and extensions
│   ├── config.py                # Configuration classes
│   ├── models/
│   │   ├── __init__.py
│   │   └── blog_post.py         # BlogPost model
│   └── routes/
│       ├── api/                  # API routes
│       │   ├── __init__.py
│       │   ├── create.py
│       │   └── read.py
│       └── web/                  # Web routes
│           ├── __init__.py
│           ├── create.py
│           ├── read.py
│           ├── update.py
│           └── delete.py
├── k8s/                          # Kubernetes manifests
│   ├── postgres.yaml             # PostgreSQL deployment + service
│   ├── flask-blog-deployment.yaml
│   └── flask-blog-service.yaml
├── tests/                        # Unit tests
│   ├── __init__.py
│   ├── conftest.py
│   └── test_models.py
├── .github/workflows/
│   └── ci.yml                    # CI/CD pipeline
├── Dockerfile                    # Docker build configuration
├── docker-entrypoint.sh          # Container startup script
├── wsgi.py                       # WSGI entry point
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| **Framework** | Flask 3.0.0 |
| **Database** | PostgreSQL 15 |
| **ORM** | SQLAlchemy 2.0 |
| **Migrations** | Flask-Migrate 4.0.5 |
| **WSGI Server** | gunicorn 21.2.0 |
| **Container** | Docker (Python 3.11-slim) |
| **Orchestration** | Kubernetes (minikube) |
| **CI/CD** | GitHub Actions |

---

## Prerequisites

- Python 3.11
- Docker Desktop (with Kubernetes enabled or minikube)
- minikube
- kubectl
- Git

---

## Local Development

### 1. Clone the Repository

```bash
git clone <repository-url>
cd flask-blog
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables

Create a `.env` file in the project root:

```env
FLASK_ENV=development
SECRET_KEY=dev-secret-key
DATABASE_URL=postgresql://postgres:KES92@pk@localhost:5432/flask_blog_dev
```

### 4. Run Locally

```bash
python app.py
```

The app will be available at `http://localhost:5000`

### 5. Run Tests

```bash
pytest tests/ -v
```

---

## Deployment to minikube

### Step 1: Start minikube

```bash
minikube start
```

### Step 2: Create Kubernetes Secret

Create a secret to store sensitive data:

**PowerShell:**
```powershell
kubectl create secret generic flask-blog-secrets `
  --from-literal=DATABASE_URL="postgresql://postgres:KES92%40pk@postgres:5432/flask_blog_dev" `
  --from-literal=SECRET_KEY="dev-secret-key-change-in-prod"
```

**Linux/Mac:**
```bash
kubectl create secret generic flask-blog-secrets \
  --from-literal=DATABASE_URL="postgresql://postgres:KES92%40pk@postgres:5432/flask_blog_dev" \
  --from-literal=SECRET_KEY="dev-secret-key-change-in-prod"
```

**Note:** The `%40` is the URL-encoded form of `@` in the password (`KES92@pk`).

### Step 3: Apply Kubernetes Manifests

```bash
kubectl apply -f k8s/postgres.yaml
kubectl apply -f k8s/flask-blog-deployment.yaml
kubectl apply -f k8s/flask-blog-service.yaml
```

### Step 4: Verify Pods are Running

```bash
kubectl get pods
```

You should see:
```
NAME                          READY   STATUS    RESTARTS   AGE
flask-blog-xxxxxxxxx-xxxxx    1/1     Running   0          1m
postgres-xxxxxxxxx-xxxxx      1/1     Running   0          1m
```

### Step 5: Access the Application

```bash
minikube service flask-blog --url
```

This will output a URL like `http://192.168.49.2:30XXX` - open it in your browser.

---

## Kubernetes Configuration

### Deployments

| Deployment | Replicas | Image | Port |
|------------|----------|-------|------|
| flask-blog | 2 | manches300/flask-blog:latest | 5000 |
| postgres | 1 | postgres:15 | 5432 |

### Services

| Service | Type | Port | Target Port |
|---------|------|------|-------------|
| flask-blog | NodePort | 80 | 5000 |
| postgres | ClusterIP | 5432 | 5432 |

### Environment Variables

The Flask app uses these environment variables:

| Variable | Source | Description |
|----------|--------|-------------|
| `FLASK_ENV` | Direct env | Application environment (production) |
| `DATABASE_URL` | Secret | PostgreSQL connection string |
| `SECRET_KEY` | Secret | Flask secret key for sessions |

### Health Checks

- **Liveness Probe**: HTTP GET `/` on port 5000 (initial delay: 30s, period: 10s)
- **Readiness Probe**: HTTP GET `/` on port 5000 (initial delay: 5s, period: 5s)

---

## CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/ci.yml`) performs:

1. **Test Job** (Ubuntu runner):
   - Installs Python dependencies
   - Runs pytest test suite

2. **Build and Deploy Job** (Self-hosted runner):
   - Logs into Docker Hub
   - Builds and pushes Docker image
   - Applies Kubernetes manifests
   - Restarts deployment

### Setting Up Self-Hosted Runner

1. Go to GitHub Repository → Settings → Actions → Runners
2. Click "New self-hosted runner"
3. Select Windows and x64
4. Download and configure the runner on your machine
5. Run the runner (`.\run.cmd`)
6. Ensure `docker` and `kubectl` are in PATH

### Required Secrets

Add these to GitHub Repository → Settings → Secrets and variables → Actions:

| Name | Description |
|------|-------------|
| `DOCKERHUB_USERNAME` | Your Docker Hub username (e.g., `manches300`) |
| `DOCKERHUB_PASSWORD` | Your Docker Hub password or access token |

---

## Useful Commands

### View Logs

```bash
# Flask app logs
kubectl logs -l app=flask-blog

# PostgreSQL logs
kubectl logs -l app=postgres

# Follow logs in real-time
kubectl logs -l app=flask-blog -f

# Previous instance logs (after crash)
kubectl logs -l app=flask-blog --previous
```

### Check Database

```bash
# Get postgres pod name
kubectl get pods -l app=postgres

# Connect to database
kubectl exec -it <postgres-pod-name> -- psql -U postgres -d flask_blog_dev

# List tables
kubectl exec -it <postgres-pod-name> -- psql -U postgres -d flask_blog_dev -c "\dt"

# Query data
kubectl exec -it <postgres-pod-name> -- psql -U postgres -d flask_blog_dev -c "SELECT * FROM blog_posts;"
```

### Scale Application

```bash
# Scale to 5 replicas
kubectl scale deployment flask-blog --replicas=5

# Check pods
kubectl get pods -l app=flask-blog
```

### Restart Deployment

```bash
kubectl rollout restart deployment flask-blog
```

### Access Service

```bash
minikube service flask-blog --url
```

### Delete Pods

```bash
# Delete specific pod
kubectl delete pod <pod-name>

# Delete all flask-blog pods (deployment will recreate)
kubectl delete pods -l app=flask-blog

# Force delete immediately
kubectl delete pod <pod-name> --force --grace-period=0
```

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/posts` | GET | Get all blog posts |
| `/posts/<id>` | GET | Get single blog post |
| `/posts/create` | POST/GET | Create new blog post |
| `/posts/<id>/update` | POST/GET | Update blog post |
| `/posts/<id>/delete` | POST | Delete blog post |

---

## Troubleshooting

### Pods in CrashLoopBackOff

```bash
# Check logs
kubectl logs -l app=flask-blog

# Check previous instance logs
kubectl logs -l app=flask-blog --previous

# Describe pod for events
kubectl describe pod -l app=flask-blog
```

### Database Connection Errors (localhost instead of postgres)

1. Verify secret exists and has data:
   ```bash
   kubectl get secret flask-blog-secrets
   ```
   Should show `DATA   2`

2. If secret is empty (DATA   0), recreate it:
   ```bash
   kubectl delete secret flask-blog-secrets
   kubectl create secret generic flask-blog-secrets \
     --from-literal=DATABASE_URL="postgresql://postgres:KES92%40pk@postgres:5432/flask_blog_dev" \
     --from-literal=SECRET_KEY="dev-secret-key-change-in-prod"
   ```

3. Restart pods:
   ```bash
   kubectl delete pods -l app=flask-blog
   ```

### ImagePullBackOff Errors

1. Verify image exists on Docker Hub: https://hub.docker.com/r/manches300/flask-blog
2. Check image name in deployment YAML
3. Ensure Docker Hub credentials are correct

### exec format error (Windows line endings)

The Dockerfile handles this automatically:
```dockerfile
RUN printf '%s\n' '#!/bin/bash' ... > docker-entrypoint.sh
```

If you still get this error, rebuild with `--no-cache`:
```bash
docker build --no-cache -t manches300/flask-blog:latest .
docker push manches300/flask-blog:latest
kubectl rollout restart deployment flask-blog
```

### YAML Parsing Errors

Common issues:
- Indentation must be consistent (2 spaces)
- No trailing spaces after `:`
- `periodSeconds: 10` needs a space after colon

---

## Security Considerations

- **Secrets**: Sensitive data stored in Kubernetes secrets, not in YAML files
- **Password Encoding**: Special characters in passwords are URL-encoded (`@` → `%40`)
- **No Hardcoded Credentials**: Database credentials loaded from environment/secrets
- **Production Config**: No fallback to localhost in production

---

## Future Improvements

- [ ] Add HTTPS/TLS termination with Ingress
- [ ] Implement user authentication (Flask-Login)
- [ ] Add horizontal pod autoscaling (HPA)
- [ ] Set up monitoring with Prometheus/Grafana
- [ ] Add persistent volume for PostgreSQL data
- [ ] Implement database backups
- [ ] Add rate limiting
- [ ] Container security scanning with Trivy

---

## License

MIT

---

## Author

Developed and deployed by [Your Name]

For issues or questions, please open an issue on the repository.
