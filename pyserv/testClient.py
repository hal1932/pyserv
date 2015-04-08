# coding: utf8

import socket
import contextlib



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
with contextlib.closing(sock):
    sock.connect(("localhost", 0x1234))
    sock.send("aaaaa")

