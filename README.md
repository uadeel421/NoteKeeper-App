# Python Microservices Application

A full-stack notes application built with Python microservices architecture, using FastAPI, Docker, and Azure MySQL.

## Architecture

```
┌─────────────┐     ┌──────────────┐
│   Frontend  │────▶│  API Gateway │
│  (Port 5000)│     │  (Port 8000) │
└─────────────┘     └──────┬───────┘
                           │
                    ┌──────┴───────┐
                    │              │
              ┌─────▼────┐   ┌────▼─────┐
              │   Auth   │   │  Notes   │
              │Service   │   │ Service  │
              │Port 8001 │   │Port 8002 │
              └─────┬────┘   └────┬─────┘
                    │             │
                    └─────┐ ┌─────┘
                          │ │
                     ┌────▼─▼────┐
                     │   Azure   │
                     │   MySQL   │
                     └───────────┘
```

## Features

- User authentication (signup/login)
- JWT token-based authorization
- Create, read, and delete notes
- Microservices architecture
- Docker containerization
- Azure MySQL database integration

## Prerequisites

- Docker and Docker Compose
- Python 3.9+
- Azure MySQL Database
- Node.js and npm (for frontend)

## Project Structure

```
microservices-python/
├── api-gateway/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── auth-service/
│   ├── app.py
│   ├── database.py
│   ├── models.py
│   ├── Dockerfile
│   └── requirements.txt
├── notes-service/
│   ├── app.py
│   ├── database.py
│   ├── models.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── templates/
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── signup.html
│   │   └── notes.html
│   ├── app.py
│   └── Dockerfile
├── docker-compose.yml
└── .env
```

## Environment Variables

Create a `.env` file in the root directory:

```env
DATABASE_URL=mysql+mysqlconnector://username:password@host:3306/database
SECRET_KEY=your-secret-key
```

## Installation & Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/microservices-python.git
cd microservices-python
```

2. Build and start the services:
```bash
docker-compose up --build
```

3. Access the application:
- Frontend: http://localhost:5000
- API Gateway: http://localhost:8000
- Auth Service: http://localhost:8001
- Notes Service: http://localhost:8002

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

## Development

To run services individually:

```bash
# API Gateway
cd api-gateway
uvicorn app:app --reload --port 8000

# Auth Service
cd auth-service
uvicorn app:app --reload --port 8001

# Notes Service
cd notes-service
uvicorn app:app --reload --port 8002

# Frontend
cd frontend
python app.py
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
