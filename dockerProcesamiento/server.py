import socket
import pickle
import cv2
import mediapipe as mp
import pika
import numpy as np

def send_image(processed_image):
    # Establecer conexión con el servidor de RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('svc-rabbit'))
    channel = connection.channel()
    print("casi que envia")
    # Declarar el exchange al que se quiere enviar el mensaje
    exchange_name = 'my_exchange'
    # Mensaje a enviar
    message = pickle.dumps(processed_image)
    # Enviar el mensaje al exchange
    routing_key = 'my_queue'
    channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=message)
    # ---------
    print("envió")
    # Cerrar la conexión
    connection.close()

#send_image("está funcionando")
class_hands = mp.solutions.hands
hands = class_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.75, min_tracking_confidence=0.5)


# Puerto de escucha
port = 8080

# Crea el socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Enlaza el socket al puerto
s.bind(('0.0.0.0', port))

# Escucha las conexiones entrantes
s.listen(1)

print(f"Servidor escuchando en el puerto {port}...")

while True:
    # Acepta la conexión entrante
    conn, addr = s.accept()

    data = b""
    while True:
        packet = conn.recv(4096)
        if not packet: break
        data += packet

    img_received = pickle.loads(data)
    #cv2.imwrite('img.jpg', img)
    #img_received = cv2.imread('img.jpg')
    print("se recibió la imagen")
    color = cv2.cvtColor(img_received, cv2.COLOR_BGR2RGB)
    print("se procesó el color")
    copy = img_received.copy()
    result = hands.process(color)
    posiciones = []

    # ------------------------------HANDS-----------------------------------

    if result.multi_hand_landmarks:
        print("hay manos")
        for hand in result.multi_hand_landmarks:
            for id, lm in enumerate(hand.landmark):
                height, width, c = img_received.shape
                coordx, coordy = int(lm.x * width), int(lm.y * height)
                posiciones.append([id, coordx, coordy])

        if len(posiciones) != 0:
            pto_i5 = posiciones[9]
            x1, y1 = (pto_i5[1] - 160), (pto_i5[2] - 160)
            ancho, alto = (x1 + 160), (y1 + 240)
            x2, y2 = x1 + ancho, y1 + alto
            dedos_reg = copy[y1:y2, x1:x2]
            cv2.rectangle(img_received, (x1, y1), (x2, y2), (0, 255, 0, 3))

            img_to_predict = cv2.resize(dedos_reg, (200, 200), interpolation=cv2.INTER_CUBIC)
            send_image(img_to_predict)
            print("se mandó la imagen")

    # -----------------------------SEND-----------------------------------------


    print(f"Conexión entrante desde {addr}")

    # Cierra la conexión
    conn.close()
