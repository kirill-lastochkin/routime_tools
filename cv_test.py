import cv2
import numpy as np
import datetime
import moviepy.editor as mp
import os

output = '__outpy.mp4'
audioName = "__audio.mp3"
outDir = 'output'
processedDir = 'processed'

def blur(image):
    return cv2.GaussianBlur(image, (161, 161), 0)

def rotate(image, koef):
    (height, width) = image.shape[:2]
    center = (width // 2, height // 2)
    degree = -90
    M = cv2.getRotationMatrix2D(center, degree, koef)
    return cv2.warpAffine(image, M, (width, height))

def crop(image):
    (height, width) = image.shape[:2]
    y = 0
    dy = height
    x = (width ** 2 - height ** 2) // (2 * width) + 1
    dx = height ** 2 // width - 1
    return image[y:y+dy, x:x+dx]

def setBack(image, backgroundImage):
    bheight, bwidth = backgroundImage.shape[:2]
    image[:bheight, :bwidth] = backgroundImage[:]

def setFront(image, foregroundImage):
    fheight, fwidth = foregroundImage.shape[:2]
    height, width = image.shape[:2]
    x = (width ** 2 - height ** 2) // (2 * width)
    image[:fheight, x:x+fwidth] = foregroundImage[:]

def makeVideo(videoIn):
    cap = cv2.VideoCapture(videoIn)
    if (cap.isOpened()== False): 
      print("Error opening video stream or file")
      return False

    width = int(cap.get(3))
    height = int(cap.get(4))
    fps = cap.get(5)

    image = np.zeros((height, width, 3), np.uint8)

    fourcc = 0x7634706d
    out = cv2.VideoWriter(output, fourcc , fps, (width, height))

    while(cap.isOpened()):
      ret, frame = cap.read()
      if ret == True:
        (height, width) = frame.shape[:2]

        foregroundImage = rotate(frame, height / width)
        foregroundImage = crop(foregroundImage)

        backgroundImage = rotate(frame, width / height * 1.5)
        backgroundImage = blur(backgroundImage)

        setBack(image, backgroundImage)
        setFront(image, foregroundImage)

        #cv2.imshow('Blur',image)
        out.write(image)

      else: 
        break
     
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    return True

def setAudio(videoIn, videoOut):
    with mp.VideoFileClip(videoIn) as videoSrc:
        videoDst = mp.VideoFileClip(output)
        audio = videoSrc.audio
        audio.write_audiofile(audioName)
        videoDst.write_videofile(videoOut, audio = audioName)

def main():
    globStart = datetime.datetime.now()
    files = os.listdir('.')
    
    if not os.path.exists(outDir):
        os.mkdir(outDir)

    if not os.path.exists(processedDir):
        os.mkdir(processedDir)

    for file in files:
        if file[-4:] != ".mp4":
            continue

        print(file)

        start = datetime.datetime.now()
        makeVideo(file)
        setAudio(file, outDir + '/' + file[:-4] + '_rotated.mp4')
        os.remove(output)
        os.remove(audioName)

        os.rename(file, processedDir + '/' + file)
        end = datetime.datetime.now()
        print(file + ': ' + str(end - start))

    globEnd = datetime.datetime.now()
    print('Total time spent: ' + str(globEnd - globStart))

if __name__ == "__main__":
    main()
