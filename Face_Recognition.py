import cv2
import sqlite3

face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('recognizer/trainingData.yml')
cam = cv2.VideoCapture(0)
fontface = cv2.FONT_HERSHEY_SIMPLEX


# get data from sqlite by ID
def getProfile(id):
    connect = sqlite3.connect("DataFaces.db")
    query = "SELECT * FROM People WHERE ID = " + str(id)
    cursor = connect.execute(query)
    profile = None
    for row in cursor:
        profile = row
    connect.close()
    return profile


def Set_Video():
    cam.set(3, 1280)  # set width
    cam.set(4, 1024)  # set height


Set_Video()

while True:
    ret, frame = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) # Draw a green border around the faces
        id, confidence = recognizer.predict(gray[y:y+h, x:x+w])
        # set text to window
        if confidence < 45:
            profile = getProfile(id)
            confidence = "{0}%".format(round(100 - confidence))
            if profile is not None:
                cv2.putText(frame, "Name:" + str(profile[1]) + " Accuracy:" + str(confidence), (x + 10, y + h + 30), fontface, 1, (0, 255, 0), 2)
        else:
            confidence = "{0}%".format(round(100 - confidence))
            cv2.putText(frame, "Unknown" + " Accuracy:" + str(confidence), (x + 10, y + h + 30), fontface, 1, (0, 0, 255), 2)
    cv2.imshow('Face', frame)
    if cv2.waitKey(1) == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()
