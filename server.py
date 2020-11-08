import http.server
import os
import socketserver 
from RangeHTTPServer import RangeRequestHandler

RangeRequestHandler.protocol_version = "HTTP/1.1"
PORT = 8000

def main(directory):
    os.chdir(directory)
    server_address = ('', PORT)
    #httpd = http.server.HTTPServer(server_address, RangeRequestHandler)
    httpd = socketserver.TCPServer(server_address, RangeRequestHandler)
    httpd.serve_forever()
