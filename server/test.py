from collections import OrderedDict
from geventwebsocket import WebSocketServer, WebSocketApplication, Resource

class EchoApplication(WebSocketApplication):
    def on_open(self):
        print "Connection opened"

    def on_message(self, message):
        self.ws.send(message)

    def on_close(self, reason):
        print reason

res = OrderedDict()
res["/"] = EchoApplication
WebSocketServer(
    ('localhost', 8000),
    Resource(res)).serve_forever()
