import qrcode
from PIL import ImageDraw, ImageFont

qr = qrcode.QRCode(
    version=9,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4
)
qr.add_data('https://money-manager-api.takatsuki.club/docs')
qr.make()
img = qr.make_image(back_color="#FFFFFF")

font = ImageFont.truetype('./NotoSansJP-Medium.ttf', 32)

draw = ImageDraw.Draw(img)
draw.text((40, 560), 'User ID: aaaa', '#000000', font=font)
img.save("test_qr.png")

# def make_qr(user_id: str, user_token: str):
