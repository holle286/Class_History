#!/usr/bin/env python3
# This is a reworked version of EchoServer to get you started.
# It responds correctly to a HEAD command.
#add the following
import socket
import os
import stat
import sys
import urllib.parse
import datetime
from threading import Thread
from argparse import ArgumentParser
BUFSIZE = 4096
#add the following
CRLF = '\r\n'
METHOD_NOT_ALLOWED = 'HTTP/1.1 405 METHOD NOT ALLOWED{}Allow: GET, HEAD, POST {}Connection: close{}{}'.format(CRLF, CRLF, CRLF, CRLF)
OK = 'HTTP/1.1 200 OK{}{}{}'.format(CRLF, CRLF, CRLF)
NOT_FOUND = 'HTTP/1.1 404 NOT FOUND{}Connection: close{}{}'.format(CRLF, CRLF, CRLF)
FORBIDDEN = 'HTTP/1.1 403 FORBIDDEN{}Connection: close{}{}'.format(CRLF, CRLF, CRLF)
MOVED_PERMANENTLY = 'HTTP/1.1 301 MOVED PERMANENTLY{}Location: https://www.cs.umn.edu/{}Connection: close{}{}'.format(CRLF, CRLF, CRLF, CRLF)


def get_contents(fname):
    with open(fname, 'r') as f:
        return f.read()

def check_perms(resource):
    """Returns True if resource has read permissions set on
'others'"""
    stmode = os.stat(resource).st_mode
    return (getattr(stat, 'S_IROTH') & stmode) > 0

def client_talk(client_sock, client_addr): # Not used anymore!!!!
    print('talking to {}'.format(client_addr))
    data = client_sock.recv(BUFSIZE)
    while data:
        print(data.decode('utf-8'))
        data = client_sock.recv(BUFSIZE)

    # clean up
    client_sock.shutdown(1)
    client_sock.close()
    print('connection closed.')
class HTTP_HeadServer: #A re-worked version of EchoServer
    def __init__(self, host, port):
        print('listening on port {}'.format(port))
        self.host = host
        self.port = port
        self.setup_socket()
        self.accept()
        self.sock.shutdown()
        self.sock.close()

    def setup_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(128)

    def accept(self):
        while True:
            (client, address) = self.sock.accept()
            #th = Thread(target=client_talk, args=(client, address))
            th = Thread(target=self.accept_request, args=(client, address))
            th.start()
        # here, we add a function belonging to the class to accept
        # and process a request
    def accept_request(self, client_sock, client_addr):
        print("accept request")
        data = client_sock.recv(BUFSIZE)
        req = data.decode('utf-8') #returns a string with http request
        linelist = req.strip().split(CRLF)
        reqline = linelist[0] #get the request line
        rlwords = reqline.split() # get list of strings on request line
        type = linelist[3]
        if len(rlwords) == 0:
            return ''

        response=self.process_request(req) #ret string with http response
        #once we get a response, we chop it into utf encoded bytes
        #and send it (like EchoClient)
        if rlwords[0] == 'GET':
            resource = rlwords[1][1:] # skip beginning /
            contents = open(resource, 'rb') #gotta keep actual message in bytes so moved half of request out here
            client_sock.send(bytes(response,'utf-8') + contents.read()) # append it to response if get
        elif rlwords[0] == 'POST':
            resource = rlwords[1][1:]
            name = req[req.find("name=") + 5: req.find("&email")] #parse string for form info
            email = req[req.find("&email=") + 7: req.find("&address=")]
            address = req[req.find("&address=") + 9: req.find("&place=")]
            place = req[req.find("&place=") + 7: req.find("&url=")]
            url = req[req.find("&url=") + 5: req.find("###")]
            client_sock.send(bytes(response + "<html><head></head><body>" + #build html
                                        "Name: " + name.replace("+", " ") + "<br>" +
                                        "Email: " + email.replace("%40", "@") + "<br>" +
                                        "Address: " + address.replace("+", " ") + "<br>" +
                                        "Place: " + place.replace("+", " ") + "<br>" +
                                        "URL: " + url + "<br>" +
                                        "</body></html>",'utf-8'))
        else:
            client_sock.send(bytes(response,'utf-8')) #if not get then keep same (for head)

        #clean up the connection to the client
        #but leave the server socket for recieving requests openclient_sock.shutdown(1)
        client_sock.close()
    #added method to process requests, only head is handled in this code
    def process_request(self, request):
        print('######\nREQUEST:\n{}######'.format(request))
        linelist = request.strip().split(CRLF)
        reqline = linelist[0] #get the request line
        rlwords = reqline.split() # get list of strings on request line
        if len(rlwords) == 0:
            return ''

        if rlwords[0] == 'HEAD':
            resource = rlwords[1][1:] # skip beginning /
            return self.head_request(resource)
        elif rlwords[0] == 'GET':
            resource = rlwords[1][1:] # skip beginning /
            contents = open(resource, 'rb')
            return self.get_request(resource)
        elif rlwords[0] == 'POST':
            resource = rlwords[1][1:] # skip beginning /
            return self.post_request(resource)
        else: #add ELIF checks for GET and POST before this else..
            return METHOD_NOT_ALLOWED

    def head_request(self, resource):
        """Handles HEAD requests."""
        path = os.path.join('.', resource) #look in directory where server
        #is running
        if not os.path.exists(resource):
            ret = NOT_FOUND
        elif not check_perms(resource):
            ret = FORBIDDEN
        else:
            ret = OK
        return ret

    def get_request(self, resource):
        """Handles GET requests."""
        path = os.path.join('.', resource) #look in directory where server
        #is running
        if not os.path.exists(resource):
            ret = NOT_FOUND
        elif not check_perms(resource):
            ret = FORBIDDEN
        else:
            ret = OK
            if("png" in resource):
                ret = ret + "\n Content-type:image/png\n"

        return ret

    def post_request(self, resource):
        """Handles POST requests."""
        path = os.path.join('.', resource) #look in directory where server
        #is running
        if not os.path.exists(resource):
            ret = NOT_FOUND
        elif not check_perms(resource):
            ret = FORBIDDEN
        else:
            ret = OK
        return ret


    #to do a get request, read resource contents and append to ret value.
    #(you should check types of accept lines before doing so)
    # You figure out the rest
def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--host', type=str, default='localhost',
                        help='specify a host to operate on (default:localhost)')
    parser.add_argument('-p', '--port', type=int, default=9001,
                            help='specify a port to operate on (default:9001)')
    args = parser.parse_args()
    return (args.host, args.port)


if __name__ == '__main__':
    (host, port) = parse_args()
    HTTP_HeadServer(host, port) #Formerly EchoServer
