import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops

image = plt.imread('symbols.png')
bi = np.sum(image, 2)
bi[bi > 0] = 1


def lb(image):
    b = ~image
    lb = label(b)
    regs = regionprops(lb)
    count_lakes = 0
    count_bays = 0
    for reg in regs:
        on_bound = False
        for y, x in reg.coords:
            if y == 0 or x == 0 or y == image.shape[0] - 1 or x == image.shape[1] - 1:
                on_bound = True
                break
        if not on_bound:
            count_lakes += 1
        else:
            count_bays += 1

    return count_lakes, count_bays


def has_vline(region):
    lines_count = 0
    lines = np.sum(region.image, 0) // region.image.shape[0]
    for line in lines:
        if line == 1:
            lines_count += 1
    return lines_count >= 3


def filling_factor(region):
    return np.sum(region.image) / region.image.size


def recognize(region):
    if np.all(region.image):
        return '-'
    lcnt, bcnt = lb(region.image)
    if lcnt == 0:
        if has_vline(region):
            return '1'
        if bcnt == 2:
            return '/'
        _, cut_cb = lb(region.image[1: -1, 1: -1])
        if cut_cb == 4:
            return 'X'
        else:
            cy = region.image.shape[0] // 2
            cx = region.image.shape[1] // 2
            if region.image[cy, cx] > 0:
                return '*'
            return 'W'
    if lcnt == 2:
        if has_vline(region):
            return 'B'
        else:
            return '8'
    if lcnt == 1:
        if bcnt == 3:
            return 'A'
        else:
            if has_vline(region):
                cy = region.image.shape[0] // 2
                cx = region.image.shape[1] // 2
                if region.image[cy, cx] > 0:
                    return 'P'
                return 'D'
            return '0'
    return None



labeled = label(bi)

regions = regionprops(labeled)

d = {None: 0}

for region in regions:
    symbol = recognize(region)

    if symbol is not None:
        labeled[np.where(labeled == region.label)] = ord(symbol)
    if symbol not in d:
        d[symbol] = 1
    else:
        d[symbol] += 1

if d[None] == 0:
    print('100%')
else:
    print(f"{(1 - d[None] / np.max(labeled)) * 100}%")
print(d)

plt.imshow(labeled, cmap='gray')
plt.show()
