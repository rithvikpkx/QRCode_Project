import segno
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import time
import os


#Getting data from HTML form on website

data = ""

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        #What to do when endpoint is acessed --> serve the html files to acessor
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open ("index.html", "r", encoding="utf-8") as f:
                html_content = f.read()
            self.wfile.write(html_content.encode('utf-8'))
        
        if self.path == "/styles.css":
            self.send_response(200)
            self.send_header("Content-type", "text/css")
            self.end_headers()
            with open("styles.css", "r", encoding = "utf-8") as f:
                css_content = f.read()
            self.wfile.write(css_content.encode('utf-8'))



    def do_POST(self):

        if self.path == "/process":
            print("process?")
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

            os.makedirs("qrcodes", exist_ok=True)
            #file_path = "qrcodes/qrcode" + qrTime + output_format
            file_path = os.path.join("qrcodes", "qrcode" + qrTime + output_format)
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

        # if self.path == "/get_image":
        #     print('this is to handle get requests for qr images from the website')



server = HTTPServer(('0.0.0.0', 8000), MyHandler)
print("server started")
server.serve_forever()

