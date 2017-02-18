from http.server import BaseHTTPRequestHandler, HTTPServer


class HttpService():

    # def do_GET(self):
    #     # Send response status code
    #     self.send_response(200)
    #
    #     # Send headers
    #     self.send_header('Content-type','text/html')
    #     self.end_headers()
    #
    #     # Send message back to client
    #     message = "Hello world!"
    #     # Write content as utf-8 data
    #     self.wfile.write(bytes(message, "utf8"))
    #     return

    def run(self):
        server_address = ('localhost', 8081)
        httpd = HTTPServer(server_address, HttpService)
        httpd.serve_forever()

HttpService().run()
