from fastapi import FastAPI, Request, Response
import httpx
import re
import json

app = FastAPI()

FALLBACK_PORT = "8080" # Default fallback port
FALLBACK_URL = "https://kfc-be.sandbait.work"
# FALLBACK_URL = "https://api-core.kfcku-dev.com"
TARGET_PORT = "8080"

# URL path mapping without API version prefixes
TARGET_MAP = {
    "voucher": "http://0.0.0.0:8090",
    "admin": "http://0.0.0.0:8085",
    # "user": "http://0.0.0.0:8081",
    "loyalties": "http://0.0.0.0:9003",
    # "internal/loyalties": "http://0.0.0.0:9003",
    # "orders": "http://0.0.0.0:8091",
    # "notif": "http://0.0.0.0:8099",
    # "payment": "http://0.0.0.0:8097",
    # "common": "http://0.0.0.0:8083",
    # "store": "http://0.0.0.0:8066",
}

@app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def forward_request(request: Request, full_path: str):
    # Remove API version prefix (v1/, v2/, etc.)
    sanitized_path = re.sub(r"^v\d+/", "", full_path)
    base_url = None

    print("full_path = ", full_path)
    print("sanitized_path = ", sanitized_path)
    
    for src, target in TARGET_MAP.items():
        if sanitized_path.startswith(src):
            base_url = f"{target}/{full_path}"
            break

    if not base_url:
        base_url = f"{FALLBACK_URL}/{full_path}"

    print("target URL = ", base_url)
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=request.method,
                url=base_url,
                headers={k: v for k, v in request.headers.items() if k.lower() != "host"},
                follow_redirects=True,
                timeout=None,
                content=await request.body(),
                params=request.query_params
            )
            
            return json.loads(response.content.decode("utf-8"))
        except httpx.HTTPStatusError as e:
            return Response(
                content=str(e),
                status_code=e.response.status_code if e.response else 500
            )
        except Exception as e:
            return Response(
                content=str(e),
                status_code=500
            )