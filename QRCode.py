#This is the non web app version that I made just to familiarize myself with using segno and figuring out all of the functionality I might need

import segno

#Important variables
content = "" # The actual content of the QR Code
output_format = ".png" # The file format of the QR code once it's exported
border_size = 0 # The amount of border on the QR code
scale = 1 # Scale factor of qr code --> how many pixels represent 1 pixel

qrcode = segno.make_qr("Hello World")
qrcode.save("qrcodes/hellowrldqrcode.png")