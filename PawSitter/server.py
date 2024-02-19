from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess

request = None

class RequestHandler_httpd(BaseHTTPRequestHandler):
  def do_GET(self):
    global request
    
    request = self.requestline
    request = request[5 : int(len(request)-9)]
    print(request)
    if request == 'on':
        subprocess.run(['python', 'recognition.py'])
        #exec(open('recognition.py').read())
    if request == 'off':
        exit()
    if request == 'cam':
        subprocess.run(['python', 'webCamera.py'])
        

server_address_httpd = ('192.168.43.155',8080)
httpd = HTTPServer(server_address_httpd, RequestHandler_httpd)
print('Starting server')
httpd.serve_forever()
GPIO.cleanup()
