# Python Microservices Notes Application

A full-stack notes application built with Python microservices architecture, using FastAPI for the backend, Flask for the frontend, and Azure MySQL for the database.

## Tech Stack
- **Frontend**: Flask (Python web framework)
- **Backend**: FastAPI (Modern, fast API framework)
- **Database**: Azure MySQL Database
- **Authentication**: JWT (JSON Web Tokens)
- **Container**: Docker & Docker Compose

## Features
- User authentication (signup/login)
- Create, read, and delete notes
- Secure API with JWT tokens
- Responsive web interface
- Containerized deployment

## Prerequisites
- Docker and Docker Compose
- Python 3.9 or higher
- Azure MySQL Database instance
- SSL certificate for database connection

## Project Structure
```
microservices-python/
├── backend/
│   ├── app.py              # FastAPI application
│   ├── requirements.txt    # Backend dependencies
│   ├── Dockerfile         # Backend container configuration
│   └── ssl/               # SSL certificates for Azure MySQL
├── frontend/
│   ├── app.py             # Flask application
│   ├── requirements.txt   # Frontend dependencies
│   ├── Dockerfile        # Frontend container configuration
│   └── templates/        # HTML templates
└── docker-compose.yml    # Container orchestration
```

## Environment Variables
Create a `.env` file in the root directory:
```
# Azure MySQL Configuration
DATABASE_URL=mysql+mysqlconnector://username:password@server.mysql.database.azure.com:3306/dbname?ssl_ca=backend/ssl/DigiCertGlobalRootCA.crt.pem

# Application Security
SECRET_KEY=your_secret_key_here

# Frontend Configuration
FRONTEND_URL=http://localhost:5000
```

## Getting Started
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd microservices-python
   ```

2. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Update with your Azure MySQL credentials

3. Start the application:
   ```bash
   docker-compose up --build
   ```

4. Access the application:
   - Frontend: http://localhost:5000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## API Endpoints
- `POST /api/signup`: Create new user account
- `POST /api/login`: Authenticate user and get JWT token
- `GET /api/notes`: Get all notes for current user
- `POST /api/notes`: Create a new note
- `DELETE /api/notes/{note_id}`: Delete a specific note

## Development
### Backend (FastAPI)
```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Frontend (Flask)
```bash
cd frontend
pip install -r requirements.txt
flask run --host=0.0.0.0
```

## Docker Commands
- Build and start containers: `docker-compose up --build`
- Stop containers: `docker-compose down`
- View logs: `docker-compose logs`
- Restart services: `docker-compose restart`

## Security Features
- Password hashing with bcrypt
- JWT token authentication
- SSL/TLS database connection
- CORS protection
- Environment variable configuration

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details
