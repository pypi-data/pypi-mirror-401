import sys
import os
import logging
import subprocess
from server.configs import settings
from typing import (
    Optional
)


logging.basicConfig(level=logging.INFO)
server_logger = logging.getLogger(__name__)


class ServerProcess:
    def __init__(self, port: Optional[int] = None):
        self.port = port
        self.running = False
        self.server_process = None
        self._initialized = True
        self.settings = None

    def uvicorn_process(self):
        import_string = "api.root:create_uvicorn_app"
        cmd = [
                    sys.executable,
                    "-m",
                    "uvicorn",
                    "--factory",
                    import_string,
                    "--host", "127.0.0.1",
                    "--port", str(self.port),
                    "--log-level", "info"
                ]

        subprocess.Popen(
                    args=cmd,
                    env={**os.environ.copy()}
                )

    def startup(self, port):
        if not self.running:
            if port is not None:
                self.port = port
            if self.port is None:
                self.port = 8990
        server_logger.info(f"Starting server on port {self.port}")
        try:
            self.server_process = self.uvicorn_process()
            self.running = True
            self.settings = settings
        except Exception:
            self.running = False
            raise

if __name__ == "__main__":
    p = ServerProcess()
    p.startup(8000)