import io
from PIL import Image, ImageDraw, ImageFont

fontPath = "fonts/PlayfairDisplay.ttf"


def draw_wrapped_text(draw, text, box_coords, font, fill_color=(255, 255, 255), line_spacing=8):

    """Wrapper function for draw, wraps text around specified bounding box dimensions"""

    x1, y1, x2, y2 = box_coords
    max_width = x2 - x1
    
    words = text.split(' ')
    lines = []
    current_line = []

    # group words into lines that fit pixel limit
    for word in words:
        if current_line:
            test = " ".join(current_line + [word])
        else:
            test = word
        
        if draw.textlength(test, font=font) <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
        
    if current_line:
        lines.append(" ".join(current_line))
    
    # find line height based on font
    bbox = draw.textbbox((0,0), "Hg", font=font)
    line_height = (bbox[3] - bbox[1]) + line_spacing

    # draw lines
    curY = y1
    for line in lines:
        if curY + line_height > y2:
            break
        
        draw.text((x1, curY), line, font=font, fill=fill_color)
        curY += line_height


    


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
    
    content_box = (412, 60, 984, 320)

    draw_wrapped_text(draw, f'"{content}"', content_box, font, fill_color=(255,255,255))
    
    draw.text((612, 350), name, font=font, fill=(255,255,255))
    draw.text((612, 420), time, font=font, fill=(255,255,255))


    return canvas


