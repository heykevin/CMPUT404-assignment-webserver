#  coding: utf-8 
import SocketServer

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

import os

ROOT = "www"

def handleRequest(self):
    if (self.requestMethod == "GET"):
        #check if path is in dir and return 404
        print(ROOT+self.requestPath)
        try:
            # get file or index if dir
            if os.path.isdir(ROOT+self.requestPath):
                # redirect 303? or whatever to index
                print("isDirectory: " +ROOT+"/index.html")
                filehandler = open(os.path.realpath(ROOT+self.requestPath+"index.html"), "rb")
                filename, extension = os.path.splitext(os.path.realpath(ROOT+self.requestPath+"index.html"))
                return createResponse(filehandler.read(), extension)
            else:
                print("isFile: " +ROOT+self.requestPath)
                filehandler = open(os.path.realpath(ROOT+self.requestPath), "rb")
                filename, extension = os.path.splitext(os.path.realpath(ROOT+self.requestPath))
                print (os.path.realpath(ROOT+self.requestPath))
                return createResponse(filehandler.read(), extension)

        except IOError:
            # return 404 if file does not exist
            print("NO GOOD")
            return "HTTP/1.1 404 NOT FOUND\r\n"
        return "OK MAN"
    return "NOTOK"

# createresponse adapted from stackoverflow
def createResponse(body, ext):
    # body no sending head
    print(body)
    print(ext.strip("."))
    responseBody = body
    # get proper mimetype
    responseHeaders = {
        "Content-Type": "text/"+ext.strip(".")+"; charset=utf-8",
        "Content-Length": len(body),
        "Connection": "close"
    }
    responseStatus = "HTTP/1.1 200 OK\r\n"
    response_headers_raw = "".join("%s: %s\r\n" % (k, v) for k, v in responseHeaders.iteritems())
    print(responseBody)
    # need extra \n before body for css to work?
    return responseStatus + response_headers_raw +"\r\n"+responseBody

def getHeaders(self):
    headers = dict()
    print("data: "+self.data)
    rawHeaders = self.data.split("\r\n")
    self.requestMethod, self.requestPath, self.requestConn = rawHeaders[0].split(" ")
    self.headers = dict(item.split(": ", 1) for item in rawHeaders[1:])

class MyWebServer(SocketServer.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        getHeaders(self)
        self.request.sendall(handleRequest(self))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
