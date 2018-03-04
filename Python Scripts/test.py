from wand import image
import pytesseract
from PIL import Image

with image.Image(
        filename="/home/manobhav/Downloads/FIR-I.I.F.-I(30).pdf[0]",
        resolution=500) as img:
    img.save(filename="temp.jpg")

img = Image.open('temp.jpg')
img2 = img.crop((1792, 1480, 2252, 1600))
print(pytesseract.image_to_string(img2))
