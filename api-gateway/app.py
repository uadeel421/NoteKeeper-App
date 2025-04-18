from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os

app = FastAPI(root_path="/api")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can tighten this later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Microservice URLs
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth-service:8001")
NOTES_SERVICE_URL = os.getenv("NOTES_SERVICE_URL", "http://notes-service:8002")

# ✅ Add this
@app.get("/health")
def health_check():
    return {"status": "api-gateway is alive"}

# ✅ Add this
@app.get("/")
def root_check():
    return {"message": "Welcome to the API Gateway"}

# Catch-all routing
@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def gateway(path: str, request: Request):
    try:
        if path in ["api/signup", "api/login", "signup", "login"]:
            if not path.startswith("api/"):
                service_path = f"api/{path}"
            else:
                service_path = path
            service_url = f"{AUTH_SERVICE_URL}/{service_path}"
        elif path.startswith("api/notes") or path.startswith("notes"):
            if not path.startswith("api/"):
                service_path = f"api/{path}"
            else:
                service_path = path
            service_url = f"{NOTES_SERVICE_URL}/{service_path}"
        else:
            raise HTTPException(status_code=404, detail="Path not found")

        print(f"Forwarding {request.method} request to: {service_url}")
        body = await request.body()
        headers = {key: value for key, value in request.headers.items()
                   if key.lower() not in ["host", "content-length"]}

        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=request.method,
                url=service_url,
                headers=headers,
                content=body
            )

            if response.status_code >= 400:
                error_detail = response.json()
                raise HTTPException(
                    status_code=response.status_code,
                    detail=error_detail.get("detail", "Service error")
                )

            return response.json()

    except HTTPException:
        raise
    except Exception as e:
        print(f"Gateway Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
