import base64

import qrcode
import json
from io import BytesIO


def generate_qr_code(data: dict):
    json_data = json.dumps(data, ensure_ascii=False)

    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(json_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    return img


def image_to_base64(img) -> str:
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return qr_base64
