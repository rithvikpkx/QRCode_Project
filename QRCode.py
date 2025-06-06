import segno
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import time
import os


#Getting data from HTML form on website

data = ""

class MyHandler(BaseHTTPRequestHandler):
    def do_POST(self):

        #recieve and store data from website
        content_length = int(self.headers['Content-Length'])
        raw_data = self.rfile.read(content_length)
        data = urllib.parse.parse_qs(raw_data.decode('utf-8'))
        print(data)
        print(data['content_field'][0])
        data = data['content_field'][0]

       
        #generate qr code
        content = data # The actual content of the QR Code, recieved from website
        output_format = ".png" # The file format of the QR code once it's exported
        border = 0 # The amount of border on the QR code
        scale = 1 # Scale factor of qr code --> how many pixels represent 1 pixel
        qrTime = str(time.time())

        #file_path = "qrcodes/qrcode" + qrTime + output_format
        file_path = os.path.join("Python", "QRCode_Project", "qrcodes", "qrcode" + qrTime + output_format)
        qrcode = segno.make_qr(content)
        qrcode.save(file_path, border = border, scale = scale)



        #return response to website
        #full_file_path = "C:/Users/prave/Documents/Code/Python/QRCode_Project/" + file_path
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                image_bytes = f.read()
            
            self.send_response(200)
            self.send_header("Content-type", "image/png")
            self.send_header("Content-length", str(len(image_bytes)))
            self.end_headers()
            self.wfile.write(image_bytes)



server = HTTPServer(('localhost', 8000), MyHandler)
print("server started")
server.serve_forever()

