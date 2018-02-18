import picamera
import time
import picamera.array


camera = picamera.PiCamera()

stream = picamera.array.PiRGBArray(camera)

camera.resolution = (100,100)
#camera.start_preview()
#time.sleep(2)
camera.capture(stream,'rgb')

print(stream.array)

#camera.close()
