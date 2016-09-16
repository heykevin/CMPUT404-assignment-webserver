#  coding: utf-8
import SocketServer

# Copyright 2016 Kevin Tang, Abram Hindle, Eddie Antonio Santos
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

responses = {
    200: ("OK", ""),
    302: ("Found", ""),
    404: ("Not found", "The requested URL was not found"),
    405: ("Method not allowed", "This method is not allowed")
}

def handleRequest(self):
    # Setting paths
    self.rootPath = os.path.realpath(ROOT)
    self.realRequestPath = os.path.realpath(ROOT+self.requestPath)

    if self.requestMethod == "GET":
        #check if path is in dir and return 404
        if not os.path.commonprefix([self.rootPath, self.realRequestPath]) == self.rootPath:
            return createErrorResponse(404)

        # If in directory, redirect to index.html
        if os.path.isdir(self.realRequestPath):
            return createResponse(302, "html", None,"index.html")

        # If retrieving a file, try to open and read
        else:
            try:
                filehandler = open(self.realRequestPath, "rb")
                filename, extension = os.path.splitext(self.realRequestPath)
                return createResponse(200, extension.strip("."), filehandler.read())
            # return 404 if file does not exist
            except IOError:
                return createErrorResponse(404)

    # generate 405 other method used
    return createErrorResponse(405)

# createResponse was adapted from stackoverflow. Author: toriningen
# http://stackoverflow.com/questions/10114224/how-to-properly-send-http-response-with-python-using-socket-library-only
def createResponse(code, ext, body, location=None) :
    resStatus = "HTTP/1.1 %s %s" % (code, responses[code][0])
    headers = {
        "Content-Type": "text/%s" % ext,
        "Connection": "close"
    }

    # Adding additional headers
    if code == 200 or code == 404:
        headers["Content-Length"] = len(body)
    if code == 302:
        headers["Location"] = location

    # Joining headers into a string
    resHeaders =  "".join("%s: %s\r\n" % (k, v) for k, v in headers.iteritems())
    return "%s\r\n%s\r\n%s" % (resStatus, resHeaders, body)

def createErrorResponse(code):
    body = "<html><head><title> %s %s </title></head>" % (code, responses[code][0]) + \
        "<body><b>%s</b> %s" % (code, responses[code][1]) + \
        "</body></html>"
    return createResponse(code, "html", body)

# Separate headers in the request
def parseHeaders(self):
    rawHeaders = self.data.split("\r\n")
    try:
        self.requestMethod, self.requestPath, self.requestConn = rawHeaders[0].split(" ")
        self.headers = dict(item.split(": ", 1) for item in rawHeaders[1:])
    except ValueError as e:
        print e

class MyWebServer(SocketServer.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print("data: "+self.data)
        # ignore empty requests
        if self.data:
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
