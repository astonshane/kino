import epd2in7.epd2in7 as epd

class Display:
    def __init__(self):
        self.screen = epd.EPD()
        self.screen.init()

        self.height = epd.EPD_HEIGHT
        self.width = epd.EPD_WIDTH

        self.fontFile = '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf'
        self.fonts = {}

    def displayImage(self, image):
        self.screen.display_frame(self.screen.get_frame_buffer(image))

        # display images
        #epd.display_frame(epd.get_frame_buffer(Image.open('monocolor.bmp')))
