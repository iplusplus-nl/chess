#https://opengameart.org/content/2d-chess-pack

from PIL import Image
import os
dir = os.getcwd()



img = Image.open(dir+'/sprites/raw/white-topdown.png')

class tile:
    def __init__(self, x, y):
        self.left = x * 128
        self.right = self.left + 128
        self.top = y * 128
        self.bottom = self.top + 128

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))

tiles = []
for y in range(0, 4):
    for x in range(0, 4):
        var = tile(x, y)
        var.img = img.crop((var.left, var.top, var.right, var.bottom))
        tiles.append(var)

#iso
#tiles[0].img.save(dir+'/sprites/_b-45.png')
#tiles[1].img.save(dir+'/sprites/_b-135.png')
#tiles[2].img.save(dir+'/sprites/_b-315.png')
#tiles[3].img.save(dir+'/sprites/_b-225.png')
#
#tiles[4].img.save(dir+'/sprites/_n-45.png')
#tiles[5].img.save(dir+'/sprites/_n-135.png')
#tiles[6].img.save(dir+'/sprites/_n-315.png')
#tiles[7].img.save(dir+'/sprites/_n-225.png')
#
#tiles[8].img.save(dir+'/sprites/_k-45.png')
#tiles[9].img.save(dir+'/sprites/_k-135.png')
#tiles[9].img.save(dir+'/sprites/_k-315.png')
#tiles[8].img.save(dir+'/sprites/_k-225.png')
#
#tiles[10].img.save(dir+'/sprites/_q-45.png')
#tiles[10].img.save(dir+'/sprites/_q-135.png')
#tiles[10].img.save(dir+'/sprites/_q-315.png')
#tiles[10].img.save(dir+'/sprites/_q-225.png')
#
#tiles[11].img.save(dir+'/sprites/_r-45.png')
#tiles[11].img.save(dir+'/sprites/_r-135.png')
#tiles[11].img.save(dir+'/sprites/_r-315.png')
#tiles[11].img.save(dir+'/sprites/_r-225.png')
#
#tiles[12].img.save(dir+'/sprites/_p-45.png')
#tiles[12].img.save(dir+'/sprites/_p-135.png')
#tiles[12].img.save(dir+'/sprites/_p-315.png')
#tiles[12].img.save(dir+'/sprites/_p-225.png')

#topdown
tiles[0].img.save(dir+'/sprites/_b-0.png')
tiles[1].img.save(dir+'/sprites/_b-90.png')
tiles[2].img.save(dir+'/sprites/_b-270.png')
tiles[3].img.save(dir+'/sprites/_b-180.png')

tiles[4].img.save(dir+'/sprites/_n-0.png')
tiles[5].img.save(dir+'/sprites/_n-90.png')
tiles[6].img.save(dir+'/sprites/_n-270.png')
tiles[7].img.save(dir+'/sprites/_n-180.png')

tiles[8].img.save(dir+'/sprites/_k-90.png')
tiles[8].img.save(dir+'/sprites/_k-270.png')
tiles[9].img.save(dir+'/sprites/_k-0.png')
tiles[9].img.save(dir+'/sprites/_k-180.png')

tiles[10].img.save(dir+'/sprites/_q-90.png')
tiles[10].img.save(dir+'/sprites/_q-270.png')
tiles[10].img.save(dir+'/sprites/_q-0.png')
tiles[10].img.save(dir+'/sprites/_q-180.png')

tiles[11].img.save(dir+'/sprites/_r-90.png')
tiles[11].img.save(dir+'/sprites/_r-270.png')
tiles[11].img.save(dir+'/sprites/_r-0.png')
tiles[11].img.save(dir+'/sprites/_r-180.png')

tiles[12].img.save(dir+'/sprites/_p-90.png')
tiles[12].img.save(dir+'/sprites/_p-270.png')
tiles[12].img.save(dir+'/sprites/_p-0.png')
tiles[12].img.save(dir+'/sprites/_p-180.png')