# Two FastAPI Microservices

This repository contains two independent Python FastAPI microservices:

- `services/service_a`
- `services/service_b`

Each service has its own application package, requirements, Dockerfile, tests, service layer, repository layer, models, schemas, and PostgreSQL database setup.

## Structure

```text
services/
  service_a/
    app/
      api/
      core/
      db/
      models/
      repositories/
      schemas/
      services/
      main.py
  service_b/
    app/
      api/
      core/
      db/
      models/
      repositories/
      schemas/
      services/
      main.py
```

## AWS RDS PostgreSQL Setup

Create a `.env` file for each service from the examples:

```powershell
Copy-Item services/service_a/.env.example services/service_a/.env
Copy-Item services/service_b/.env.example services/service_b/.env
```

Set `DATABASE_URL` to your AWS RDS PostgreSQL endpoint:

```text
postgresql+psycopg://db_user:db_password@your-rds-endpoint.region.rds.amazonaws.com:5432/database_name?sslmode=require
```

Production notes:

- Do not commit real `.env` files or database passwords.
- Enable SSL on the RDS connection by keeping `sslmode=require`.
- Put the app and RDS instance in compatible VPC/security groups.
- Allow inbound PostgreSQL traffic on port `5432` only from your app runtime security group.
- Store secrets in AWS Secrets Manager or SSM Parameter Store in real deployments.

## Run Locally

From the repository root:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r services/service_a/requirements.txt
pip install -r services/service_b/requirements.txt
```

Start service A:

```powershell
uvicorn app.main:app --reload --port 8001 --app-dir services/service_a
```

Start service B:

```powershell
uvicorn app.main:app --reload --port 8002 --app-dir services/service_b
```

## Run With Docker Compose

```powershell
docker compose up --build
```

Service A: http://localhost:8001

Service B: http://localhost:8002

Health checks:

- http://localhost:8001/health/
- http://localhost:8002/health/

Database health checks:

- http://localhost:8001/health/db
- http://localhost:8002/health/db
