import Image
import ImageFont
import ImageDraw

class BaseImage:
    def __init__(self, height, width, color=255, font='/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf'):
        self.height = height
        self.width = width

        self.image = None
        self.draw = None

        self.buffer = 5
        self.lastY = 0

        self.fontFile = font
        self.fonts = {}

        self.clear()

    # lazily load fonts
    def getFont(self, size=18):
        font = self.fonts.get(size, ImageFont.truetype(self.fontFile, size))
        self.fonts[size] = font
        return font

    def clear(self, color=255):
        self.image = Image.new('1', (self.width, self.height), color)
        self.draw = ImageDraw.Draw(self.image)
        self.lastY = 0

    def drawText(self, text, size=18, fill=0, x=5, y=None):
        if y is None:
            y = self.lastY + self.buffer

        self.lastY = y + size

        self.draw.text((x,y), text, font=self.getFont(size), fill=fill)

    def drawBorder(self, fill=0, x=0, y=None, height=1, width=1):
        if y is None:
            y = self.lastY + self.buffer
        self.lastY = y + height

        p = (x, y, x+width, y+height)
        self.draw.rectangle(p, fill=fill)
