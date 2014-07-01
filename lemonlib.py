import socket
import urllib.request
import time


'''
(C) Copyright 2014 Riyoken:

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

Version [Pre Alpha]
'''

class Chat:

    def __init__(self, **kw):
        [setattr(self, x, kw[x]) for x in kw]        
        self.connect()

    def connect(self):
        self.cumsock = socket.socket()
        self.cumsock.connect((self.server, self.port))
        self.cumsock.send(('NICK %s\r\n' % self.nick).encode())
        self.cumsock.send(('USER %s %s bla :%s\r\n' % (self.nick, self.server, self.realname)).encode())
        self.cumsock.send(('JOIN %s\r\n' % self.chat.lower()).encode())
        
class Main:
    def __init__(self):
        self.interpret = Interpret(self)
        self.net = None
       
    def start(self, chat, nick, server):
        self.join('#'+chat.lower(), nick, server)
        self.matrix()
        
    def matrix(self):
        while True:
            self.rdata = b''
            while not self.rdata.endswith(b'\r\n'):
                self.rdata += self.net.cumsock.recv(1024)
            self.interpret.parse_data(self.rdata)
            self.rdata = b''

    def join(self, chat, nick, server):
        self.net = Chat(**{
            'server': server,
            'port': 6667,
            'nick': nick,
            'realname': 'nomnomnom',
            'chat': chat
        })

class Interpret:

    def __init__(self, main):
        self.main = main
        self.spam = False
        
    def parse_data(self, data):
        data = data.decode().split('\r\n')
        [self.handle_data(x.split(':')) for x in data]

    def handle_data(self, data):
        print(data)        
        if data[0] == 'PING ':
            ping = 'PONG :%s\r\n' % data[1]
            self.main.net.cumsock.send(ping.encode())
