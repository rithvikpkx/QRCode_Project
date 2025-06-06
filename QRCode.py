import segno
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import os
import cgi
# import socket


class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        #serve html file
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open ("index.html", "r", encoding="utf-8") as f:
                html_content = f.read()
            self.wfile.write(html_content.encode('utf-8'))
        
        #serve css file
        if self.path == "/styles.css":
            self.send_response(200)
            self.send_header("Content-type", "text/css")
            self.end_headers()
            with open("styles.css", "r", encoding = "utf-8") as f:
                css_content = f.read()
            self.wfile.write(css_content.encode('utf-8'))
        
        #serve font resource files
        if self.path.startswith("/resources/"):
            font_file_path = self.path.lstrip('/')
            if os.path.exists(font_file_path):
                self.send_response(200)
                self.send_header("Content-type", "font/ttf")
                self.end_headers()
                with open (font_file_path, 'rb') as f:
                    self.wfile.write(f.read())

        if self.path.startswith("/QRimage/"):
            qrname = self.path[len("/QRimage/"):]  # Extract the filename
            image_file_path = os.path.join("qrcodes", qrname)
            self.send_response(200)
            self.send_header("Content-type", "image/png")
            self.end_headers()
            with open(image_file_path, "rb") as f:
                self.wfile.write(f.read())            





    def do_POST(self):
        
        #recieve data from input field on website and send back qr code image
        if self.path == "/process":

            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            if ctype == 'multipart/form-data':
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                pdict['CONTENT-LENGTH'] = int(self.headers['content-length'])
                fields = cgi.parse_multipart(self.rfile, pdict)
                # fields['content_field'] is a list of values
                data = fields.get('content_field', [None])[0]
                print(data)
        
            #generate qr code
            content = data # The actual content of the QR Code, recieved from website
            output_format = ".png" # The file format of the QR code once it's exported
            border = 0 # The amount of border on the QR code
            scale = 10 # Scale factor of qr code --> how many pixels represent 1 pixel
            qrTime = str(time.time())

            os.makedirs("qrcodes", exist_ok=True)
            #file_path = "qrcodes/qrcode" + qrTime + output_format
            qrname = "qrcode" + qrTime + output_format
            qrcode_file_path = os.path.join("qrcodes", qrname)
            qrcode = segno.make_qr(content)
            qrcode.save(qrcode_file_path, border = border, scale = scale)

            #return response to website
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.send_header("Content-length", str(len(qrname.encode("utf-8"))))
            self.end_headers()
            self.wfile.write(qrname.encode("utf-8"))


server = HTTPServer(('0.0.0.0', 8000), MyHandler)
print("server started")
server.serve_forever()