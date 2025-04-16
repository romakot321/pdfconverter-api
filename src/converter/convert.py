import os
from unoserver.client import UnoClient
from unoserver.server import UnoServer
from threading import Thread

client = UnoClient()


def run_server():
    def _handle(server: UnoServer):
        process = server.start()
        if process is None:
            raise ValueError("Server not started")
        print("[+] Server PID: " + str(process.pid))
        process.wait()
        server.stop()

        try:
            os.kill(process.pid, 9)
        except OSError as e:
            if e.errno == 3:
                return
            raise

    server = UnoServer()
    Thread(target=_handle, args=(server,)).start()


def convert_file(file_body: bytes, convert_to: str) -> bytes | None:
    return client.convert(indata=file_body, convert_to=convert_to)

