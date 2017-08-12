from __future__ import print_function
from random import randint
import asyncore
import collections
import socket


MAX_MESSAGE_LENGTH = 4096


class RemoteClient(asyncore.dispatcher):

    """Wraps a remote client socket."""

    def __init__(self, host, socket, address):
        asyncore.dispatcher.__init__(self, socket)
        self.host = host
        self.outbox = collections.deque()

    def say(self, message):
        self.outbox.append(message)

    def handle_read(self):
        client_message = self.recv(MAX_MESSAGE_LENGTH)
        self.host.broadcast(client_message)

    def handle_write(self):
        if not self.outbox:
            return
        message = self.outbox.popleft()
        if len(message) > MAX_MESSAGE_LENGTH:
            raise ValueError('Message too long')
        self.send(message)


class Client(asyncore.dispatcher):

    def __init__(self, host_address, name):
        asyncore.dispatcher.__init__(self)
        print ('definition your user : (%7s)' % name)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = name
        print('Connecting to host at server...')
        self.connect(host_address)
        self.outbox = collections.deque()

    def handle_error(self):
        print("Server is down.")
        exit()

    def handle_write(self):
        if not self.outbox:
            return
        message = self.outbox.popleft()
        if len(message) > MAX_MESSAGE_LENGTH:
            raise ValueError('Message too long')
        self.send(message)

    def handle_read(self):

        message = self.recv(MAX_MESSAGE_LENGTH)

        if ["MODE", "JOIN", "QUIT", ".IP", ":v[", ":vHackXTGuard",
           "ip.vhack.biz", "#vHackXT", "PING"] in message:

            message = message.split(" ")

            correcte = ['MODE', "JOIN", "QUIT", ".IP", ":v[",
                        "admin.vhack.biz", "mod.vhack.biz", ":vHackXTGuard",
                        "#vHackXT", ":Ping", "PING", ":chat.vhackxt.com",
                        ":chat.vhackxt.com\r\n", "timeout:", "seconds\r\n",
                        "vip.vhack.biz", "ip.vhack.biz", ":Read", "error"]

            for i, list_word in enumerate(message):
                for list_match in correcte:
                    if list_match in list_word:
                        message.remove(message[i])

            if "## Cluster" in message:
                message = message.replace("##", "\r\n ##")

            print(' '.join(message))

        else:
            print(message)


if __name__ == '__main__':
    print('Creating clients')
    client = Client(("164.132.9.247", 15000), 'User_' + str(randint(0, 500)))
    asyncore.loop()
