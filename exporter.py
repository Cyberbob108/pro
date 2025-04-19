from io import BytesIO
import base64

def export_drawing(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_bytes = buffered.getvalue()
    b64 = base64.b64encode(img_bytes).decode()
    href = f'<a href="data:file/png;base64,{b64}" download="drawing.png">📥 Download Drawing</a>'
    return href
