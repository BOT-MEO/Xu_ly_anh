import cv2
import numpy as np
import os
from PIL import Image


recognizer = cv2.face.LBPHFaceRecognizer_create()
path = 'Data'


def getImageWithID(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    IDs = []
    for imagePath in imagePaths:
        faceImg = Image.open(imagePath).convert('L')
        faceNp = np.array(faceImg, 'uint8')
        print(faceNp)
        ID = int(os.path.split(imagePath)[-1].split('.')[1])
        faces.append(faceNp)
        IDs.append(ID)
        cv2.imshow("Training", faceNp)
        cv2.waitKey(10)
    return faces, IDs


faces, Ids = getImageWithID(path)
recognizer.train(faces, np.array(Ids))
if not os.path.exists('recognizer'):
    os.makedirs('recognizer')
recognizer.save('recognizer/trainingData.yml')
cv2.destroyAllWindows()
