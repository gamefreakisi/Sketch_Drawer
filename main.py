import cv2
import numpy as np
import imutils
from progress.bar import ChargingBar
import time
import sys
import threading
from math import floor



input_image_path = r"C:\Users\Dell\Desktop\Color Image to hand drawn sketch\Image\img2.jpeg"      
output_video_path = r"C:\Users\Dell\Desktop\Color Image to hand drawn sketch\Output Video\sketch_video_1.avi"         
background_color = [255, 255, 255]             
foreground_color = [43, 47, 54]                
duration = 12                                  
skip_pixels = 20                               



img = None
blank_image = None
done = None
bar = None
height = 0
width = 0
channel = 0
count_done = 0
num_foreground_pixels = 0
video_writer = None
frame_rate = 30



def createSketch(img, blurX=21, blurY=21):
    img = imutils.resize(img, height=600)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inv = 255 - gray
    blur = cv2.GaussianBlur(inv, (blurX, blurY), 0)
    inv_blur = 255 - blur
    sketch = cv2.divide(gray, inv_blur, scale=256.0)
    return sketch

def createLineDrawing(input_img, foregroundColor, backgroundColor):
    global img  
    sketch = createSketch(input_img)

    if isinstance(backgroundColor, str):
        bg = cv2.imread(backgroundColor)
        bg = cv2.resize(bg, (sketch.shape[1], sketch.shape[0]))
        is_bg_img = True
    else:
        bg = np.full((sketch.shape[0], sketch.shape[1], 3), backgroundColor, dtype=np.uint8)
        is_bg_img = False

    result = np.zeros((sketch.shape[0], sketch.shape[1], 3), dtype=np.uint8)
    for y in range(sketch.shape[0]):
        for x in range(sketch.shape[1]):
            if sketch[y, x] < 240:
                result[y, x] = foregroundColor
            else:
                result[y, x] = bg[y, x] if is_bg_img else backgroundColor

    img = result  
    return result



def setVideoWriter(name, size):
    global video_writer, frame_rate, duration, num_foreground_pixels, skip_pixels
    frame_rate = floor(num_foreground_pixels / (skip_pixels * duration))
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    video_writer = cv2.VideoWriter(name, fourcc, frame_rate, size)

def addToVideo(frame):
    video_writer.write(frame)

def completeVideo():
    cv2.destroyAllWindows()
    video_writer.release()



def searchNeighbour(x, y, foreground):
    global done, count_done, bar, blank_image, img

    if done[y, x]:
        return

    if list(img[y, x]) != foreground:
        return

    done[y, x] = 1
    count_done += 1
    blank_image[y, x] = foreground

    if count_done % skip_pixels == 0:
        addToVideo(blank_image.copy())

    if x > 0:
        searchNeighbour(x - 1, y, foreground)
    if x < width - 1:
        searchNeighbour(x + 1, y, foreground)
    if y > 0:
        searchNeighbour(x, y - 1, foreground)
    if y < height - 1:
        searchNeighbour(x, y + 1, foreground)

def animateDrawing(foreground):
    global img, height, width, done, blank_image, num_foreground_pixels, bar

    for i in range(height):
        for j in range(width):
            bar.next()
            if not done[i, j] and list(img[i, j]) == foreground:
                searchNeighbour(j, i, foreground)
    bar.finish()


    for _ in range(frame_rate * 2):
        addToVideo(blank_image.copy())

    completeVideo()



def generateSketchVideo():
    global img, blank_image, done, bar, height, width, channel, num_foreground_pixels

    input_img = cv2.imread(input_image_path)
    line_drawing = createLineDrawing(input_img, foreground_color, background_color)
    img = line_drawing
    height, width, channel = img.shape

    
    num_foreground_pixels = np.count_nonzero(np.all(img == foreground_color, axis=2))


    if isinstance(background_color, str):
        blank_image = cv2.imread(background_color)
        blank_image = cv2.resize(blank_image, (width, height))
    else:
        blank_image = np.full((height, width, channel), background_color, dtype=np.uint8)

    done = np.zeros((height, width), dtype=np.uint8)
    bar = ChargingBar("Rendering Sketch Video", max=(height * width))

    setVideoWriter(output_video_path, (width, height))

    print("Starting animation rendering...")
    threading.Thread(target=animateDrawing, args=(foreground_color,)).start()


if __name__ == "__main__":
    sys.setrecursionlimit(1000000000)
    threading.stack_size(100000000)

    generateSketchVideo()
