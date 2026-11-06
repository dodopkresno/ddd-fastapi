"""Start Uvicorn on an ephemeral port and exercise real HTTP requests."""

import socket
import subprocess
import sys
import time

import httpx


def main() -> None:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "ddd_fastapi.main:create_app",
            "--factory",
            "--host",
            "127.0.0.1",
            "--port",
            str(port),
            "--no-access-log",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    try:
        with httpx.Client(
            base_url=f"http://127.0.0.1:{port}", timeout=1, trust_env=False
        ) as client:
            for _ in range(50):
                try:
                    if client.get("/health/live").status_code == 200:
                        break
                except httpx.TransportError:
                    time.sleep(0.1)
                if process.poll() is not None:
                    raise RuntimeError("Server exited before readiness")
            else:
                raise RuntimeError("Server did not start")
            assert client.get("/health/ready").status_code == 200
            response = client.post("/api/v1/items", json={"name": "smoke"})
            assert response.status_code == 201, response.text
            url = response.headers["location"]
            assert client.get(url).json()["name"] == "smoke"
            assert client.put(url, json={"name": "updated"}).status_code == 200
            assert client.delete(url).status_code == 204
            assert client.get(url).status_code == 404
            print("PASS: Uvicorn startup, health endpoints, Items CRUD")
    finally:
        process.terminate()
        output, _ = process.communicate(timeout=10)
        print(output)


if __name__ == "__main__":
    main()
