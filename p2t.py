from PIL import Image
import colorsys

class Character:
    '''An array of chracters, sorted by brightness'''
    characters = [
        " ",
        ".",
        ":",
        "-",
        "=",
        "+",
        "*",
        "#",
        "%",
        "@"
    ]

    '''I'm not stoked about the way I'm handling tuples here.'''
    @classmethod
    def GetChar(self, pixel):
        if len(pixel) == 4:
            r, g, b, a = pixel
        else:
            r, g, b = pixel
        r = float(r / 255)
        g = float(g / 255)
        b = float(b / 255)
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        return self.characters[int(v * (len(self.characters) - 1))]

'''Unused...'''
class Color:
    RED =    "\033[0;31m"
    ORANGE = "\033[0;33m"
    YELLOW = "\033[1;33m"
    GREEN =  "\033[0;32m"
    CYAN =   "\033[0;36m"
    BLUE =   "\033[0;34m"
    PURPLE = "\033[0;35m"
    ENDC =   "\033[0m"

    '''Temp'''
    def GetNearest(self, hue):
        return self.RED

class Sampler:
    def __init__(self, texture):
        self.texture = texture

    
    def Lerp(self, min, max, t):
        if type(min) == tuple:
            if len(min) == 4:
                rmin, gmin, bmin, amin = min
                rmax, gmax, bmax, amax = max
            else:
                rmin, gmin, bmin = min
                rmax, gmax, bmax = max
            rlerp = self.Lerp(rmin, rmax, t)
            glerp = self.Lerp(gmin, gmax, t)
            blerp = self.Lerp(bmin, bmax, t)
            return (rlerp, glerp, blerp)
        return (max - min) * t + min

    def Sample(self, u, v):
        u = u * self.texture.width
        left = int(u)
        right = left + 1
        tu = u - left

        v = v * self.texture.height
        top = int(v)
        bottom = top + 1
        tv = v - top

        topleft = self.texture.getpixel((left, top))
        bottomleft = self.texture.getpixel((left, bottom))
        topright = self.texture.getpixel((right, top))
        bottomright = self.texture.getpixel((right, bottom))

        return self.Lerp(
            self.Lerp(topleft, bottomleft, tv),
            self.Lerp(topright, bottomright, tv),
            tu)

def main():
    img = Image.open("pic0.png")
    sampler2d = Sampler(img)

    height = 120 # height in characters
    aspect = float(img.width) / float(img.height)
    width = int(height * aspect) # width in characters

    line = ""
    for y in range(height):
        for x in range(width):
            pixel = sampler2d.Sample(x / width, y / height)
            line += Character.GetChar(pixel) + " "
        print (line)
        line = ""

if __name__ == "__main__":
    main()