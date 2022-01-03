import numpy as np
import matplotlib.pyplot as plt

image = np.load('ps.npy').astype('bool')

masks_4_6 = {
    'left': [
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [0, 0, 1, 1],
        [0, 0, 1, 1],
        [1, 1, 1, 1],
        [1, 1, 1, 1],
    ],
    'right': [
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [1, 1, 0, 0],
        [1, 1, 0, 0],
        [1, 1, 1, 1],
        [1, 1, 1, 1],
    ],
    'filled_4*6': [
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [1, 1, 1, 1],
    ]
}

masks_6_4 = {
    'up': [
        [1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1],
    ],
    'down': [
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1],
    ],
    'filled_6*4': [
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1],
    ]
}


def get_matched(arr, masks):
    for key in masks.keys():
        mask = masks[key]
        if np.all(mask == arr):
            return key
    return None


stats = {}

for y in range(image.shape[0] - 4):
    
    for x in range(image.shape[1] - 4):
        if x + 4 < image.shape[1] and y + 6 < image.shape[0]:
            sub = image[y:y + 6, x:x + 4]
            mask = get_matched(sub, masks_4_6)
            if mask is not None:
                if mask in stats:
                    stats[mask] += 1
                else:
                    stats[mask] = 1
        if x + 6 < image.shape[1] and y + 4 < image.shape[0]:
            sub = image[y:y + 4, x:x + 6]
            mask = get_matched(sub, masks_6_4)
            if mask is not None:
                if mask in stats:
                    stats[mask] += 1
                else:
                    stats[mask] = 1

print(stats)

plt.imshow(image)
plt.show()