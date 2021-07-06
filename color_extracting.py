from PIL import Image, UnidentifiedImageError
from colorthief import ColorThief
import os


def extract_dominant_colors(file, color_count):

    # Open Image
    try:
        picture = Image.open(file)
    except UnidentifiedImageError:
        return 'Image Not Identified!'
   
    
    # Optimize Image and save
    img_name = f"compressed_{file.split('/')[2]}"

    picture.thumbnail((200, 200))
    picture.save(f"static/uploads/{img_name}")

    # Open optimized Image and extract colors
    color_thief = ColorThief(f"static/uploads/{img_name}")
    # build a color palette
    palette = color_thief.get_palette(color_count=color_count)

    # delete optimized image
    os.remove(f'static/uploads/{img_name}')

    # Convert rgb colors to hex and return
    def rgb_to_hex(rgb):
        return '%02x%02x%02x' % rgb

    return list(map(rgb_to_hex, palette))

