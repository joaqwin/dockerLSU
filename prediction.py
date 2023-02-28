import cv2
import mediapipe as mp
import os
import numpy as np
from keras_preprocessing.image import load_img, img_to_array
from keras.models import load_model
import time
import threading
import datetime
import math
from gtts import gTTS
from playsound import playsound

modelo = '/home/usuario/PycharmProjects/pythonProject/Modelo.h5'
peso = '/home/usuario/PycharmProjects/pythonProject/pesos.h5'
cnn = load_model(modelo)
cnn.load_weights(peso)

flag = True
def change_flag():
    global flag
    time.sleep(5)
    flag = not flag

def playAudio(texto):
    os.system("python3 /home/usuario/PycharmProjects/pythonProject/test.py " + '"' + texto + '"')


fecha_actual = datetime.datetime.now().date()
hora_actual = datetime.datetime.now().time()
stringFecha = fecha_actual.strftime("%Y-%m-%d")
stringHora = hora_actual.strftime("%H:%M:%S")

translationName= "translation"+stringFecha+"-"+stringHora
direccionTranslation = f"/home/usuario/PycharmProjects/pythonProject/Traducciones/{translationName}.txt"
direccionInterfaxTxt = "/home/usuario/PycharmProjects/pythonProject/Traducciones/textoTraduccion/texto.txt"
#os.system("touch /home/usuario/PycharmProjects/pythonProject/Traducciones/{}.txt".format(translationName))
with open(direccionTranslation, "w") as file:
    file.write("")
with open(direccionInterfaxTxt, 'w') as file2:
    file2.write("")

direccion = '/home/usuario/PycharmProjects/pythonProject/Photos/validation'
dire_img = os.listdir(direccion)
print("Nombres: ", dire_img)

cam = cv2.VideoCapture(0)

#MANOS-MEDIAPIPE
class_hands = mp.solutions.hands
hands = class_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.75, min_tracking_confidence=0.5)

#FACEMESH-MEDIAPIPE
mp_face = mp.solutions.face_mesh
face = mp_face.FaceMesh(max_num_faces=1)

mpDibujo = mp.solutions.drawing_utils
confiDibujo = mpDibujo.DrawingSpec(thickness=1, circle_radius=1)

drawing = mp.solutions.drawing_utils

asombrado = False
while(1):
    ret, frame = cam.read()
    color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    copy = frame.copy()
    result = hands.process(color)
    resultadoFace = face.process(color)
    posiciones = []


    #------------------------------HANDS-----------------------------------

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            for id, lm in enumerate(hand.landmark):
                height, width, c = frame.shape
                coordx, coordy = int(lm.x*width), int(lm.y*height)
                posiciones.append([id, coordx, coordy])

                drawing.draw_landmarks(frame, hand, class_hands.HAND_CONNECTIONS)
        if len(posiciones) != 0:
            pto_i1 = posiciones[4]
            pto_i2 = posiciones[20]
            pto_i3 = posiciones[12]
            pto_i4 = posiciones[0]
            pto_i5 = posiciones[9]
            x1, y1 = (pto_i5[1]-160),(pto_i5[2]-160)
            ancho, alto = (x1+160),(y1+240)
            x2, y2 = x1+ancho, y1+alto
            dedos_reg = copy[y1:y2, x1:x2]
            cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0, 3))

            if dedos_reg.shape[0] > 199 and dedos_reg.shape[1] > 199:
                dedos_reg = cv2.resize(dedos_reg, (200, 200), interpolation=cv2.INTER_CUBIC)
                x = img_to_array(dedos_reg)
                x = np.expand_dims(x, axis=0)
                vector = cnn.predict(x)
                result = vector[0]
                response = np.argmax(result)

                file = open(direccionTranslation, "a")
                fileInterfazTxt = open(direccionInterfaxTxt, "a")

                # if respuesta == 2:
                # print(vector, resultado)
                # cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 3)
                # cv2.putText(frame , '{}'.format(dire_img[0]), (x1,y1-5), 1, 1.3, (0,255,0), 1, cv2.LINE_AA)
                # if flag:
                # file.write(" "+dire_img[0])
                # fileInterfazTxt.write(" "+dire_img[0])
                # hiloAudio = threading.Thread(target=playAudio, args=(dire_img[2],))
                # hiloAudio.start()
                # flag = False
                # hilo = threading.Thread(target=change_flag)
                # hilo.start()
                if response == 4:
                    if flag:
                        file.write(" " + dire_img[4])
                        fileInterfazTxt.write(" " + dire_img[4])
                        audio_thread = threading.Thread(target=playAudio, args=(dire_img[4],))
                        audio_thread.start()
                        flag = False
                        hilo = threading.Thread(target=change_flag)
                        hilo.start()
                elif response == 3:
                    # cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
                    # cv2.putText(frame, '{}'.format(dire_img[2]), (x1, y1 - 5), 1, 1.3, (0, 255, 0), 1, cv2.LINE_AA)
                    if flag:
                        file.write(" " + dire_img[1])
                        fileInterfazTxt.write(" " + dire_img[1])
                        audio_thread = threading.Thread(target=playAudio, args=(dire_img[1],))
                        audio_thread.start()
                        flag = False
                        hilo = threading.Thread(target=change_flag)
                        hilo.start()
                elif response == 2:
                    # cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
                    # cv2.putText(frame, '{}'.format(dire_img[2]), (x1, y1 - 5), 1, 1.3, (0, 255, 0), 1, cv2.LINE_AA)
                    if flag:
                        file.write(" " + dire_img[2])
                        fileInterfazTxt.write(" " + dire_img[2])
                        audio_thread = threading.Thread(target=playAudio, args=(dire_img[2],))
                        audio_thread.start()
                        flag = False
                        hilo = threading.Thread(target=change_flag)
                        hilo.start()
                elif response == 1:
                    # cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
                    # cv2.putText(frame, '{}'.format(dire_img[2]), (x1, y1 - 5), 1, 1.3, (0, 255, 0), 1, cv2.LINE_AA)
                    if flag:
                        file.write(" " + dire_img[3])
                        fileInterfazTxt.write(" " + dire_img[3])
                        audio_thread = threading.Thread(target=playAudio, args=(dire_img[3],))
                        audio_thread.start()
                        flag = False
                        hilo = threading.Thread(target=change_flag)
                        hilo.start()
                elif response == 0:
                    # cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
                    # cv2.putText(frame, '{}'.format(dire_img[2]), (x1, y1 - 5), 1, 1.3, (0, 255, 0), 1, cv2.LINE_AA)
                    if flag:
                        file.write(" " + dire_img[0])
                        fileInterfazTxt.write(" " + dire_img[0])
                        audio_thread = threading.Thread(target=playAudio, args=(dire_img[0],))
                        audio_thread.start()
                        flag = False
                        hilo = threading.Thread(target=change_flag)
                        hilo.start()
                fileInterfazTxt.close()
            else:
                print("La imagen de entrada tiene un tamaño inválido")


    else:
        cv2.putText(frame, "No se detectan manos", (100, 40), 2, 1.3, (0, 255, 0), 1, cv2.LINE_AA)
    #-------------------------------FACE-MESH--------------------------------------
    px = []
    py = []
    lista = []
    r = 5
    t = 3

    if resultadoFace.multi_face_landmarks:
        for rostros in resultadoFace.multi_face_landmarks:
            mpDibujo.draw_landmarks(frame, rostros, mp_face.FACEMESH_CONTOURS, confiDibujo, confiDibujo)

            for id, puntos in enumerate(rostros.landmark):
                height, width, c = frame.shape
                x, y = int(puntos.x * width), int(puntos.y * height)
                px.append(x)
                px.append(y)
                lista.append([id, x, y])
                if len(lista) == 468:
                    # ASOMBRADO
                    x1, y1 = lista[0][1:]
                    x2, y2 = lista[17][1:]
                    cv2.circle(frame, (x1, y1), 3, (0, 255, 0), 3)
                    cv2.circle(frame, (x2, y2), 3, (255, 0, 0), 3)
                    dist = math.sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2))
                    print(dist)
                    if dist > 44:
                        cv2.putText(frame, 'ASOMBRADO', (x1, y1 - 5), 1, 1.3, (0, 0, 255), 1, cv2.LINE_AA)
                        asombrado = True
    else:
        cv2.putText(frame, "No se detectan rostros", (100, 70), 2, 1.3, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.imshow("Video", frame)
    k = cv2.waitKey(1)
    if k == ord('s'):
        break

texto = ""
archivo = open(direccionTranslation, "a")
fileInterfazTxt = open(direccionInterfaxTxt, "a")

if asombrado:
    archivo.write("<break></break>  (Asombrado)")
    fileInterfazTxt.write(" (Asombrado)")
archivo.close()
fileInterfazTxt.close()

readArchivo = open(direccionTranslation, "r")
lineas = readArchivo.readlines()
i = 0
for i in range(len(lineas)):
    texto += lineas[i]

audio_thread = threading.Thread(target=playAudio, args=(texto,))
audio_thread.start()

readArchivo.close()
