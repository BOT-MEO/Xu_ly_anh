import cv2
import os
import sqlite3

face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
cam = cv2.VideoCapture(0)
numbers = 0


def Set_Video():
    cam.set(3, 640)  # set width
    cam.set(4, 480)  # set height


def Insert_Update(id, name):
    connect = sqlite3.connect("DataFaces.db")
    query = "SELECT * FROM People WHERE ID = " + str(id)
    cusror = connect.execute(query)
    isRecordExists = 0
    for row in cusror:
        isRecordExists = 1
    if isRecordExists == 1:
        query = "UPDATE People SET Name= " + str(name) + "WHERE ID=" + str(id)
    else:
        query = "INSERT INTO People(ID, Name) VALUES (" + str(id) + ",'" + str(name) + "')"
    connect.execute(query)
    connect.commit()
    connect.close()


id = input("Enter ID: ")
name = input("Enter Name: ")

Set_Video()
Insert_Update(id, name)

while True:
    ret, frame = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        if not os.path.exists('Data'):
            os.makedirs('Data')
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Draw a green border around the faces
        numbers = numbers + 1
        cv2.imwrite("Data/User." + str(id) + '.' + str(numbers) + ".jpg", gray[y:y + h, x:x + w])
    cv2.imshow("Video", frame)
    if numbers > 100:
        break
    elif cv2.waitKey(300) & 0xFF == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()
