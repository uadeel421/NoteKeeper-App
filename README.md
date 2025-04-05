# Python Microservices with AWS RDS

## Application Structure
- Frontend: Flask web interface (port 5000)
- Backend: FastAPI service (port 8000)
- Database: MySQL (port 3306)

## Local Development
1. Install Docker and Docker Compose
2. Run: `docker-compose up --build`
3. Access frontend at: http://localhost:5000

## AWS RDS Configuration
1. Create MySQL RDS instance in AWS
2. Update backend environment variables:
   ```
   DATABASE_URL=mysql+mysqlconnector://<username>:<password>@<rds-endpoint>:3306/notesdb
   ```
3. For production, remove the local `db` service from docker-compose.yml

## Deployment Options
1. **Docker**: Build and run individual containers
2. **Kubernetes**: 
   - Create deployments and services for each component
   - Use AWS RDS as external service
   - Configure secrets for database credentials

## Important Notes
- For production, use environment variables for all sensitive data
- The frontend communicates with backend via REST API
- Backend handles all database operations
