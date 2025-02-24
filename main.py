from fastapi import FastAPI, Request
import httpx

app = FastAPI()

# URL path mapping
TARGET_MAP = {
    "http://localhost:3001/v1/voucher": "http://localhost:8090/v1/voucher",
    "http://localhost:3001/v1/user": "http://localhost:8081/v1/user",
    "http://localhost:3001/v1/loyalties": "http://localhost:9003/v1/loyalties",
    "http://localhost:3001/v1/internal/loyalties": "http://localhost:9003/v1/internal/loyalties",
}
DEFAULT_PORT = 8080  # Default fallback port

@app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def forward_request(request: Request, full_path: str):
    source_url = f"http://{request.headers.get('host', 'localhost:3001')}/{full_path}"
    base_url = None

    for src, target in TARGET_MAP.items():
        if source_url.startswith(src):
            base_url = target + source_url[len(src):]
            break

    if not base_url:
        base_url = f"http://localhost:{DEFAULT_PORT}/{full_path}"

    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=base_url,
            headers={k: v for k, v in request.headers.items() if k.lower() != "host"},
            content=await request.body()
        )

    return response.json()
