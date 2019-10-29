try:
    import http.server as BaseHTTPServer  # Python 3.x
except ImportError:
    import BaseHTTPServer  # Python 2.x
import os
import shutil
import sys

#FILEPATH = sys.argv[1] if sys.argv[1:] else __file__
FILEPATH = "Expedition_Curved.mp4"
class SimpleHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        with open(FILEPATH, 'rb') as f:
            self.send_response(200)
            self.send_header("Content-Type", 'application/octet-stream')
            self.send_header("Content-Disposition", 'attachment; filename="{}"'.format(os.path.basename(FILEPATH)))
            fs = os.fstat(f.fileno())
            self.send_header("Content-Length", str(fs.st_size))
            self.end_headers()
            shutil.copyfileobj(f, self.wfile)

def test(HandlerClass=SimpleHTTPRequestHandler,
         ServerClass=BaseHTTPServer.HTTPServer,
         protocol="HTTP/1.0"):
    if sys.argv[2:]:
        port = int(sys.argv[2])
    else:
        port = 7079
    server_address = ('', port)

    HandlerClass.protocol_version = protocol
    httpd = BaseHTTPServer.HTTPServer(server_address, HandlerClass)

    sa = httpd.socket.getsockname()
    print("Serving HTTP on {0[0]} port {0[1]} ... {1}".format(sa, FILEPATH))
    httpd.serve_forever()

if __name__ == '__main__':
    test()