import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
from skimage.color import rgb2hsv

img = plt.imread('balls_and_rects.png')

def hues(hue):
    for i in range(30, 360, 60):
        if (i - 30) / 360 <= hue <= (i + 30) / 360:
            return i / 360
    return None


bi = np.mean(img.copy(), 2)
bi[bi > 0] = 1

balls = []
rects = []
fbc = {}

labeled = label(bi)
regions = regionprops(labeled)

for region in regions:
    hue = hues(rgb2hsv(img[region.coords[0][0], region.coords[0][1]])[0])

    if hue not in fbc:
        fbc[hue] = {
            'rects': 0,
            'balls': 0
        }

    if np.all(region.image):
        rects.append(region)
        fbc[hue]['rects'] += 1
    else:
        balls.append(region)
        fbc[hue]['balls'] += 1

print('all figures:', len(rects) + len(balls))
print('balls -', len(rects))
print('rects-', len(balls))
print('hues:')

for key in sorted(fbc.keys()):
    stat = fbc[key]
    print(f"{key}: {stat['balls']} balls, {stat['rects']} rects")