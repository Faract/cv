from skimage.measure import label
from skimage.measure import regionprops
from skimage.morphology import binary_dilation, square
from mss import mss
import numpy as np
import pyautogui
import time
 
dino_area = 1086
 
last_nearest_object = None
 
print('waiting for 5 seconds...')
time.sleep(5)
pyautogui.press('space')
 
 
def jump():
    pyautogui.keyDown('space')
    time.sleep(0.0001)
    pyautogui.keyUp('space')
    pass
 
 
with mss() as sct:
    while True:
        monitor = {"top": 540, "left": 150, "width": 660, "height": 390}
        img = np.array(sct.grab(monitor)).mean(2)
 
        img[abs(img - 126) != 0] = 0
        img[img != 0] = 1
 
        labeled = label(img)
 
        objects = regionprops(labeled)
 
        for smallObject in filter(lambda obj: obj.area < 187 or abs(obj.bbox[0] - obj.bbox[2]) < 20, objects):
            for y, x in smallObject.coords:
                labeled[y, x] = 0
 
        labeled[labeled != 0] = 1
        labeled = label(binary_dilation(labeled, square(4)))
 
        objects = regionprops(labeled)
 
        dino_list = list(filter(lambda obj: abs(obj.area - dino_area) < 37, objects))
        if len(dino_list) == 0:
            pyautogui.press('space')
        else:
            dino = dino_list[0]
 
            closest = None
            for not_dino in filter(lambda obj: obj.label != dino.label, objects):
                distance = not_dino.bbox[1] - dino.bbox[1]
                if closest is None or closest.bbox[1] - dino.bbox[1] > distance > 0:
                    closest = not_dino
 
            if closest is not None:
                distance = closest.bbox[1] - dino.bbox[1]
                if distance >= 0:
                    if last_nearest_object is not None and last_nearest_object.area == closest.area:
                        speed = last_nearest_object.bbox[1] - closest.bbox[1]
                        if speed > 0:
                            width = closest.bbox[3] - closest.bbox[1]
                            height = closest.bbox[2] - closest.bbox[0]
                            if distance - speed - height * 1.5 < 25:
                                jump()
 
                    last_nearest_object = closest
                    