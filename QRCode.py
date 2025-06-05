import segno

#Important variables
content = "" # The actual content of the QR Code
output_format = ".png" # The file format of the QR code once it's exported
border = 0 # The amount of border on the QR code
scale = 1 # Scale factor of qr code --> how many pixels represent 1 pixel
id_num = 0 # Id number used in filename to save the qrcode

qrcode = segno.make_qr(content)
qrcode.save("qrcodes/qrcode" + str(id_num) + output_format, border = border, scale = scale)
