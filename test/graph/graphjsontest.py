import json
import networkx as nx
from networkx.readwrite import json_graph
import sys

def load_url(path):
    PORT = 8000
    httpd = StoppableHTTPServer(("127.0.0.1",PORT), handler)
    thread.start_new_thread(httpd.serve, ())
    webbrowser.open_new('http://localhost:%s/%s'%(PORT,path))
    input("Press <RETURN> to stop server\n")
    httpd.stop()
    print("To restart server run: \n%s"%server)


if sys.version_info[0] == 2:
    import SimpleHTTPServer, BaseHTTPServer
    import socket
    import thread
    import webbrowser
    handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    server = "python -m SimpleHTTPServer 8000"

    class StoppableHTTPServer(BaseHTTPServer.HTTPServer):

        def server_bind(self):
            BaseHTTPServer.HTTPServer.server_bind(self)
            self.socket.settimeout(1)
            self.run = True

        def get_request(self):
            while self.run:
                try:
                    sock, addr = self.socket.accept()
                    sock.settimeout(None)
                    return (sock, addr)
                except socket.timeout:
                    pass

        def stop(self):
            self.run = False

        def serve(self):
            while self.run:
                self.handle_request()


else:
    import http.server, http.server
    import socket
    import _thread as thread
    import webbrowser
    handler = http.server.SimpleHTTPRequestHandler
    server = "python -m http.server 8000"

    class StoppableHTTPServer(http.server.HTTPServer):

        def server_bind(self):
            http.server.HTTPServer.server_bind(self)
            self.socket.settimeout(1)
            self.run = True

        def get_request(self):
            while self.run:
                try:
                    sock, addr = self.socket.accept()
                    sock.settimeout(None)
                    return (sock, addr)
                except socket.timeout:
                    pass

        def stop(self):
            self.run = False

        def serve(self):
            while self.run:
                self.handle_request()

G = nx.barbell_graph(6, 3)
# this d3 example uses the name attribute for the mouse-hover value,
# so add a name to each node
for n in G:
    G.node[n]['name'] = n
# write json formatted data
d = json_graph.node_link_data(G)  # node-link format to serialize
# write json
json.dump(d, open('force.json', 'w'))
