import socket
import cv2
import pickle
import numpy as np
from time import sleep

def send_img(img_arr):
    img = np.array(img_arr)
    message = pickle.dumps(img)

    server_address = ('127.0.0.1', 40591)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect(server_address)

    client_socket.sendall(message)

    client_socket.close()
    sleep(2)


cap = cv2.VideoCapture(0)

while (cap.isOpened()):
    ret, frame = cap.read()
    if ret:
        #img_array = img_to_array(frame)
        print(frame)
        send_img(frame)
        cv2.imshow("video", frame)

    k = cv2.waitKey(1)
    if k == ord('s'):
        break

cap.release()
cv2.destroyAllWindows()

