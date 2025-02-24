# FastAPI Reverse Proxy

This is a simple FastAPI-based reverse proxy that forwards API requests based on full URL path mappings.

## Features
- Dynamically forwards requests based on predefined full URL mappings.
- Supports `GET`, `POST`, `PUT`, `DELETE`, and `PATCH` methods.
- Uses `httpx.AsyncClient` for efficient asynchronous request handling.
- Automatically forwards requests to the same path but with port `8080` if not listed in `TARGET_MAP`.

## Installation
Ensure you have Python installed, then install the required dependencies:
```sh
pip install fastapi uvicorn httpx
```

## Usage
1. Save the provided code as `main.py`.
2. Run the FastAPI server with:
```sh
uvicorn main:app --host 0.0.0.0 --port 3001 --reload
```

## API Routing
This proxy forwards requests based on the following mapping:

| Incoming Request | Forwarded To |
|------------------|-------------|
| `http://localhost:3001/v1/voucher/*` | `http://localhost:8090/v1/voucher/*` |
| `http://localhost:3001/v1/user/*` | `http://localhost:8081/v1/user/*` |
| `http://localhost:3001/v1/loyalties/*` | `http://localhost:9003/v1/loyalties/*` |
| `http://localhost:3001/v1/internal/loyalties/*` | `http://localhost:9003/v1/internal/loyalties/*` |
| Any other request | `http://localhost:8080/{original_path}` |

## Example Requests

### Forwarding `v1/voucher`
```sh
curl -X GET "http://localhost:3001/v1/voucher/redeem/123"
```
➡️ Forwards to `http://localhost:8090/v1/voucher/redeem/123`

### Forwarding `v1/user`
```sh
curl -X POST "http://localhost:3001/v1/user/register" -d '{"email": "test@example.com"}'
```
➡️ Forwards to `http://localhost:8081/v1/user/register`

### Forwarding `v1/loyalties`
```sh
curl -X GET "http://localhost:3001/v1/loyalties/status"
```
➡️ Forwards to `http://localhost:9003/v1/loyalties/status`

### Forwarding Unknown Paths
```sh
curl -X GET "http://localhost:3001/other/path"
```
➡️ Forwards to `http://localhost:8080/other/path`

## Notes
- Ensure that the target APIs (`localhost:8090`, `localhost:8081`, `localhost:9003`, and `localhost:8080`) are running before testing.
- Modify the `TARGET_MAP` dictionary to add more forwarding rules as needed.

## License
This project is open-source and can be used freely.