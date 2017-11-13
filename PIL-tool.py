from PIL import Image

img = Image.open('img/o9zsefU.png')
img = img.convert("RGBA")

pixdata = img.load()

width, height = img.size
for y in xrange(height):
    for x in xrange(width):
        if pixdata[x, y] == (255, 255, 255, 255):
            pixdata[x, y] = (255, 255, 255, 0)

img.save("menu.png", "PNG")
