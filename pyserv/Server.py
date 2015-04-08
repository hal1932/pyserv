# coding: utf8
import socket
import contextlib
import threading
import time
import Queue


class ServerConfig:
    port = 0x1234
    recvBufferSize = 1024
    backlogCount = 10
    survivalConfirmationInterval = 10.0 # クライアントの生存確認用の ping を打つ間隔（秒）


class ServerThread(threading.Thread):
    def __init__(self, config):
        super(ServerThread, self).__init__()
        self.__config = config
        self.__sendQueue = Queue.Queue()

    def pushSendData(self, data):
        self.__sendQueue.put(data, True)

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        with contextlib.closing(sock):
            sock.bind(("localhost", self.__config.port))
            sock.listen(self.__config.backlogCount)

            client, _ = sock.accept()
            client.setblocking(0)
            lastSendTime = time.clock()

            while True:
                # 受信
                received = False
                data = client.recv(self.__config.recvBufferSize)
                if len(data) > 0:
                    print "received: %s" % (data)
                    received = True

                if (not received) and self.__sendQueue.empty():
                    # クライアントの生存確認
                    currentTime = time.clock()
                    if currentTime - lastSendTime > self.__config.survivalConfirmationInterval:
                        print "ping!"
                        lastSendTime = currentTime
                    else:
                        time.sleep(1)
                else:
                    # 送信キューをさばく
                    while not self.__sendQueue.empty():
                        data = self.__sendQueue.get(True)
                        print "send %s" % (data)
                        lastSendTime = time.clock()


config = ServerConfig()
th = ServerThread(config)
th.start()

