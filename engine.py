import cv2
from camera import Camera

camera = Camera()
img = camera.capture()
cv2.imwrite('test.jpg', img)