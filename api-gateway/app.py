from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Service URLs
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth-service:8001")
NOTES_SERVICE_URL = os.getenv("NOTES_SERVICE_URL", "http://notes-service:8002")
USER_SERVICE_URL = "http://user-service:8003"


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def gateway(path: str, request: Request):
    try:
        # Forward to appropriate service based on path
        if path in ["api/signup", "api/login"]:
            service_url = f"{AUTH_SERVICE_URL}/{path}"
        elif path.startswith("api/notes"):
            service_url = f"{NOTES_SERVICE_URL}/{path}"
        else:
            raise HTTPException(status_code=404, detail="Path not found")

        print(f"Forwarding {request.method} request to: {service_url}")

        # Forward the request
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

            # Important: Forward the status code from the service
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
