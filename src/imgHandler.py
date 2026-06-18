import io
from PIL import Image, ImageDraw, ImageFont

fontPath = "fonts/PlayfairDisplay.ttf"

def draw_wrapped_text(draw, text, box_coords, font, fill_color=(255, 255, 255), line_spacing=8):

    x1, y1, x2, y2 = box_coords
    max_width = x2 - x1
    
    words = text.split(' ')
    lines = []
    current_line = []
    
    

def imgQuote(name,content,avatarBytes,time):
    bgWidth = 1024
    bgHeight = 512

    canvas = Image.new("RGB", (bgWidth, bgHeight), color=(0,0,0))

    avatarStream = io.BytesIO(avatarBytes)

    with Image.open(avatarStream) as img:
        img = img.convert("RGBA") #transparancy capabillity
        canvas.paste(img, (128,128), mask=img)

    draw = ImageDraw.Draw(canvas)

    try:
        font = ImageFont.truetype(str(fontPath), size=32)
    except IOError:
        print(f"Cant find font at {fontPath}, using sytem default")
        font = ImageFont.load_default()
    
    draw.text((612, 128), f'"{content}"', font=font, fill=(255,255,255))
    draw.text((612, 328), name, font=font, fill=(255,255,255))
    draw.text((612, 378), time, font=font, fill=(255,255,255))


    return canvas


