# I need to make overlapping tiles for the Aerb map. 
# Why? Because the map doesn't have a simple multiple which can be looped across,
# so I need each tile able to be offset.

#%%
from PIL import Image
#img = Image.open("aerbtile.png")
img = Image.open("../AerbTileLargeLabels.webp")


# %%
TILESIZE = 300
STRIPWIDTH = 2000
for x in range(img.width//STRIPWIDTH):
    for y in range(img.height//TILESIZE):
        area = (STRIPWIDTH*x, TILESIZE*y, STRIPWIDTH*(x+1)+TILESIZE, TILESIZE*(y+1))
        print(area)
        cropped_img = img.crop(area)
        cropped_img.save(f"x{x}y{y}.webp")
        #w{STRIPWIDTH}h{TILESIZE}


# %%
