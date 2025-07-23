# NoteKeeper-App

A full-stack notes application built with Python microservices architecture, using FastAPI, Docker, and Azure MySQL. This project is a comprehensive demonstration of modern software development and DevOps practices, showcasing its full lifecycle from development to deployment.

## Architecture

```
┌─────────────┐       ┌──────────────┐
│   Frontend  │────▶│  API Gateway │
│  (Port 5000)│       │  (Port 8000) │
└─────────────┘       └──────┬───────┘
                              │
                      ┌──────┴───────┐
                      │              │
              ┌─────▼────┐    ┌────▼─────┐
              │   Auth   │    │  Notes   │
              │Service   │    │ Service  │
              │Port 8001 │    │Port 8002 │
              └─────┬────┘    └────┬─────┘
                    │              │
                    └─────┐ ┌─────┘
                          │ │
                      ┌────▼─▼────┐
                      │  Azure   │
                      │  MySQL   │
                      └───────────┘
```

## Features

- User authentication (signup/login)
- JWT token-based authorization
- Create, read, and delete notes
- Microservices architecture
- Docker containerization for local development
- Kubernetes deployment on Azure Kubernetes Service (AKS)
- Infrastructure as Code (IaC) with Terraform
- Configuration Management with Ansible
- CI/CD pipeline with GitHub Actions
- Cluster backup and recovery with Velero
- Azure MySQL database integration

## Prerequisites

- Docker and Docker Compose
- Python 3.9+
- Azure Account
- Node.js and npm (for frontend)

## Project Structure

```
microservices-python/
├── .github/
│   └── workflows/
│       └── ci-cd.yml              # GitHub Actions workflow
├── ansible/
│   └── my_aks_deployment/
│       ├── ansible.cfg
│       ├── inventory/
│       │   ├── hosts.ini
│       │   └── group_vars/
│       │       └── all.yml
│       ├── playbooks/
│       │   └── sites.yml
│       └── roles/
│           ├── cert-manager/
│           │   └── tasks/
│           │       └── main.yml
│           ├── common/
│           │   └── tasks/
│           │       └── main.yml
│           ├── csi-driver/
│           │   └── tasks/
│           │       └── main.yml
│           └── ingress/
│               ├── tasks/
│               │   └── main.yml
│               └── templates/
│                   └── ingress-nginx-values.yml.j2
├── api-gateway/
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── tests/
│       └── test_auth.py
├── auth-service/
│   ├── app.py
│   ├── database.py
│   ├── models.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── tests/
│       └── test_auth.py
├── notes-service/
│   ├── app.py
│   ├── database.py
│   ├── models.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── tests/
│       └── test_auth.py
├── frontend/
│   ├── templates/
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── notes.html
│   │   └── signup.html
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── helm-charts/
│   ├── .helmignore
│   ├── Chart.yaml
│   ├── cluster-issuer.yaml
│   ├── values.yaml
│   ├── certs/
│   ├── charts/
│   └── templates/
│       ├── apigateway-deployment.yml
│       ├── auth-deployment.yml
│       ├── configmap.yml
│       ├── frontend-deployment.yml
│       ├── ingress.yaml
│       └── noteservice-deployment.yml
├── kubernetes/
│   ├── apigateway-deployment.yml
│   ├── app-ingress.yml
│   ├── auth-deployment.yml
│   ├── configmap.yml
│   ├── frontend-deployment.yml
│   ├── noteservice-deployment.yml
│   ├── terraform.tfstate
│   ├── notekeeper/
│   │   ├── .helmignore
│   │   ├── Chart.yaml
│   │   ├── cluster-issuer.yaml
│   │   ├── values.yaml
│   │   └── templates/
│   │       ├── _helpers.tpl
│   │       ├── apigateway-deployment.yml
│   │       ├── auth-deployment.yml
│   │       ├── configmap.yml
│   │       ├── frontend-deployment.yml
│   │       ├── ingress.yaml
│   │       ├── noteservice-deployment.yml
│   │       └── secretproviderclass.yml
├── ssl/
├── terraform/
│   ├── .terraform.lock.hcl
│   ├── load-terraform-creds.sh
│   ├── main.tf
│   ├── outputs.tf
│   ├── terraform.tfstate
│   ├── terraform.tfstate.backup
│   ├── terraform.tfvars
│   └── variables.tf
├── docker-compose.yml
└── README.md
```

## Environment Variables

Create a `.env` file in the root directory:

```env
DATABASE_URL=mysql+mysqlconnector://username:password@host:3306/database
SECRET_KEY=your-secret-key
```

## Installation & Setup (Local)

Clone the repository:

```bash
git clone https://github.com/yourusername/microservices-python.git
cd microservices-python
```

Build and start the services:

```bash
docker-compose up --build
```

Access the application:

- Frontend: [http://localhost:5000](http://localhost:5000)
- API Gateway: [http://localhost:8000](http://localhost:8000)
- Auth Service: [http://localhost:8001](http://localhost:8001)
- Notes Service: [http://localhost:8002](http://localhost:8002)

## DevOps Architecture & Deployment

This project's infrastructure and deployment are automated using a modern DevOps toolchain.

### Infrastructure as Code (IaC)

- **Terraform:** Used to provision all cloud infrastructure, including the AKS cluster and Azure MySQL database, ensuring the environment is reproducible and version-controlled.

### Configuration Management

- **Ansible:** Automates the installation and configuration of critical components within the AKS cluster, such as the Ingress controller and cert-manager, to prepare the cluster for application deployment.

### Container Orchestration

- **Kubernetes (AKS):** The application is deployed to an Azure Kubernetes Service (AKS) cluster. Deployment is managed using Helm charts, which define the application's resources and configuration.

- **Secret Management:** Sensitive data like the database connection string is stored securely in **Azure Key Vault** and accessed within AKS using the CSI driver and a SecretProviderClass.

- **Ingress:** An Ingress controller is configured with Let’s Encrypt TLS certificates to enable secure HTTPS access to the application.

### CI/CD Pipeline

- **GitHub Actions:** A CI/CD pipeline is implemented to automate the build, test, and deployment process. The workflow performs:

  - Linting and testing of the codebase.
  - Docker image build and push to a container registry.
  - Deployment to the AKS cluster via `kubectl apply` or Helm.

- **GitHub Secrets:** All credentials and secrets for the pipelines are stored securely using GitHub Secrets.

### Cluster Backup & Recovery

- **Velero:** Integrated for automated backup and restoration of the entire Kubernetes cluster state, providing a robust disaster recovery solution.

## API Endpoints

### Auth Service (Port 8001)

- `POST /api/signup` - Register new user
- `POST /api/login` - User login

### Notes Service (Port 8002)

- `GET /api/notes` - Get user's notes
- `POST /api/notes` - Create new note
- `DELETE /api/notes/{note_id}` - Delete note

## Database Schema

### Users Table

```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) UNIQUE,
    name VARCHAR(255),
    hashed_password VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE
);
```

### Notes Table

```sql
CREATE TABLE notes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    content VARCHAR(255) NOT NULL,
    owner_id INT NOT NULL,
    INDEX owner_id_idx (owner_id)
);
```

## Docker Commands

```bash
# Build all services
docker-compose build

# Start all services
docker-compose up

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# Clean up
docker system prune -f
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
