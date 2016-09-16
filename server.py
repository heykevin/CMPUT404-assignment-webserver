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
    if self.requestMethod == "GET":
        #check if path is in dir and return 404
        realpath = os.path.realpath(ROOT+self.requestPath)
        print "Checking path and dir"
        print os.path.realpath(ROOT+self.requestPath)
        print os.path.realpath(ROOT)
        print os.path.commonprefix([os.path.realpath(ROOT), os.path.realpath(ROOT+self.requestPath)])
        print os.path.commonprefix([os.path.realpath(ROOT), os.path.realpath(ROOT+self.requestPath)]) == os.path.realpath(ROOT)
        if not os.path.commonprefix([os.path.realpath(ROOT), os.path.realpath(ROOT+self.requestPath)]) == os.path.realpath(ROOT):
            print "not in same dir"
            return createErrorResponse()

        try:
            # get file or index if dir
            if os.path.isdir(realpath):
                # redirect 303? or whatever to index
                print("isDirectory: " +ROOT+self.requestPath+"index.html")
                filehandler = open(os.path.realpath(ROOT+self.requestPath+"index.html"), "rb")
                return createRedirectResponse(self.requestPath+"index.html", "html")
            else:
                print("isFile: " + ROOT+self.requestPath)
                filehandler = open(os.path.realpath(ROOT+self.requestPath), "rb")
                filename, extension = os.path.splitext(os.path.realpath(ROOT+self.requestPath))
                print (os.path.realpath(ROOT+self.requestPath))
                return createResponse(filehandler.read(), extension.strip("."))

        except IOError:
            # return 404 if file does not exist
            print("NO GOOD")
            return createErrorResponse()
        return "OK MAN"
    return "NOTOK"

# createresponse adapted from stackoverflow
def createResponse(body, ext):
    print 200
    responseHeaders = {
        "Content-Type": "text/%s" % ext,
        "Content-Length": len(body),
        "Connection": "close"
    }
    responseStatus = "HTTP/1.1 200 OK\r\n"
    response_headers_raw = "".join("%s: %s\r\n" % (k, v) for k, v in responseHeaders.iteritems())
    return "%s%s\r\n%s" % (responseStatus, response_headers_raw, body)

def createErrorResponse():
    body = "<HTML><BODY>NOT FOUDNAKL DJAKLSDJ ALSJKD</BODY></HTML>"
    responseHeaders = {
        "Content-Type": "text/html",
        "Content-Length": len(body),
        "Connection": "close"
    }

    responseStatus = "HTTP/1.1 404 NOT FOUND\r\n"
    response_headers_raw = "".join("%s: %s\r\n" % (k, v) for k, v in responseHeaders.iteritems())
    return "%s%s\r\n%s" % (responseStatus, response_headers_raw, body)

def createRedirectResponse(location, ext):
    print("Redirecting")
    print location
    responseHeaders = {
        "Content-Type": "text/%s" % ext,
        "Location": location,
        "Connection": "close"
    }
    responseStatus = "HTTP/1.1 302 FOUND\r\n"
    response_headers_raw = "".join("%s: %s\r\n" % (k, v) for k, v in responseHeaders.iteritems())
    return "%s%s\r\n" % (responseStatus, response_headers_raw)

def parseHeaders(self):
    headers = dict()
    print("data: "+self.data)
    rawHeaders = self.data.split("\r\n")
    # empty requests
    try: 
        self.requestMethod, self.requestPath, self.requestConn = rawHeaders[0].split(" ")
        self.headers = dict(item.split(": ", 1) for item in rawHeaders[1:])
    except ValueError as e:
        print e

class MyWebServer(SocketServer.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        parseHeaders(self)
        self.request.sendall(handleRequest(self))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
