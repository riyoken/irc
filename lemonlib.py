import socket
import urllib.request
import time
import select


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
'''
to do:
    create regex patterns to handle all of the events
'''

class Chat:

    def __init__(self, **kw):
        [setattr(self, x, kw[x]) for x in kw]        
        self.connect()

    def connect(self):
        self.cumsock = socket.socket()
        self.cumsock.connect((self.server, self.port))
        self.wbyte += ('NICK %s\r\n' % self.nick).encode()
        self.wbyte += ('USER %s %s bla :%s\r\n' % (self.nick, self.server, self.realname)).encode()        

    def auth(self):
        self.wbyte += ('JOIN %s\r\n' % self.chat.lower()).encode()
        
class Main:
    def __init__(self):
        self.interpret = Interpret(self)
        self.connections = dict()
       
    def start(self, chats, nick):
        [self.join(x, nick) for x in chats]
        self.matrix()

    def getConnections(self):
        return [x for x in self.connections.values() if x.cumsock.fileno() != -1 and x.cumsock != None]
        
    def matrix(self):
        self.lemon = True
        while self.lemon:
            self.rdata = b''
            connections = self.getConnections()
            rsocks = [x.cumsock for x in connections]
            wsocks = [x.cumsock for x in connections if x.wbyte != b'']
            rsock, wsock, e = select.select(rsocks, wsocks, [], 0.1)
            for i in rsock:
                net = [x for x in connections if x.cumsock == i][0]
                while not self.rdata.endswith(b'\r\n'): self.rdata += i.recv(1024)
                self.interpret.parse_data(self.rdata, net)
                self.rdata = b''
            for i in wsock:
                net = [x for x in connections if x.cumsock == i][0]
                i.send(net.wbyte)
                net.wbyte = b''

    def join(self, x, nick):
        chat = '#'+(x[0].lower().lstrip('#'))
        server = x[1]
        self.connections[chat] = Chat(**{
            'server': server,
            'port': 6667,
            'nick': nick,
            'wbyte': b'',
            'realname': 'nomnomnom',
            'chat': chat
        })

class Interpret:

    def __init__(self, main):
        self.main = main

    def clean(self, data):
        return [x.rstrip() for x in data]
        
    def parse_data(self, data, net):
        data = data.decode().split('\r\n')
        [self.handle_data(self.clean(x.split(':')), net) for x in data]

    def handle_data(self, data, net):
        print(data)
        if len(data) > 1:
            if data[0] == 'PING':
                ping = 'PONG :%s\r\n' % data[1]
                net.wbyte += ping.encode()
                
            elif 'MODE' in data[1].split(' '):
                if data[1].split(' ')[2] == net.nick:
                    net.auth()

if __name__ == '__main__':
    Main().start([('chat','irc.obsidianirc.net')], 'riyoirc')
