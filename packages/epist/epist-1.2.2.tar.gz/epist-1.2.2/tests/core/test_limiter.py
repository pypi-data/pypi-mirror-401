from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address


def test_rate_limiting():
    # Setup isolated test app
    limiter = Limiter(key_func=get_remote_address)
    app = FastAPI()
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.add_middleware(SlowAPIMiddleware)

    @app.get("/limited")
    @limiter.limit("2/minute")
    def limited(request: Request):
        return {"status": "ok"}

    @app.get("/unlimited")
    def unlimited(request: Request):
        return {"status": "ok"}

    client = TestClient(app)

    # Test limited endpoint
    response = client.get("/limited")
    assert response.status_code == 200
    response = client.get("/limited")
    assert response.status_code == 200

    # 3rd request should fail
    response = client.get("/limited")
    assert response.status_code == 429
    assert "Rate limit exceeded" in response.text

    # Test unlimited endpoint (should still work)
    response = client.get("/unlimited")
    assert response.status_code == 200
    response = client.get("/unlimited")
    assert response.status_code == 200
    response = client.get("/unlimited")
    assert response.status_code == 200
