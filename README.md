Color Image to Hand-Drawn Sketch Video Generator
This Python project converts a color image into a hand-drawn sketch-style video. The program processes the input image to create a pencil sketch effect and then generates an animation video showing the sketch being “drawn” gradually, pixel by pixel, producing a smooth hand-drawn animation effect.

Features
Converts any color image to a pencil sketch using OpenCV and image processing techniques.

Generates a progressive hand-drawing animation saved as a video (.avi by default).

Supports customizable foreground (sketch) and background colors or background images.

Allows adjustable frame rate and animation duration.

Easy-to-use Python script with minimal dependencies (numpy, opencv-python, imutils, progress).

How It Works
The input image is converted to a grayscale pencil sketch.

The sketch is colorized based on specified foreground and background colors or images.

The program iteratively reveals sketch pixels and saves each step as a video frame.

The frames are compiled into a video showing the drawing process in real time.
