"""One-command demo with a real HTTP server on an automatically selected port."""
from threading import Thread
from client import run
from provider import make_server

if __name__ == '__main__':
    with make_server() as server:
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            run(f'http://127.0.0.1:{server.server_port}')
        finally:
            server.shutdown()
            thread.join()
