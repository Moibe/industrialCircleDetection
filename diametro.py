import cv2
import numpy as np

# Valores de los colores aproximados del círculo
color_mas_oscuro = np.array([0xD4, 0xE4, 0xD8], dtype=np.uint8)
color_mas_claro = np.array([0x75, 0x83, 0x79], dtype=np.uint8)

def procesar_fotograma(frame):
    # Convierte el fotograma a espacio de color HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define un rango de color verde en HSV
    verde_bajo = np.array([40, 40, 40])
    verde_alto = np.array([80, 255, 255])

    # Crea una máscara para el color verde
    mascara = cv2.inRange(hsv, verde_bajo, verde_alto)

    # Encuentra contornos en la máscara
    contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Encuentra el círculo más grande en la imagen
    radio_maximo = 0
    x_circulo = 0
    y_circulo = 0

    for contorno in contornos:
        # Encuentra el círculo que se ajusta mejor al contorno
        (x, y), radio = cv2.minEnclosingCircle(contorno)
        if radio > radio_maximo:
            radio_maximo = radio
            x_circulo = int(x)
            y_circulo = int(y)

    # Dibuja un círculo rojo alrededor del círculo verde detectado
    if radio_maximo > 0:
        # Ajusta los parámetros para un círculo más preciso
        centro = (x_circulo, y_circulo)
        radio_redondeado = int(round(radio_maximo))
        cv2.circle(frame, centro, radio_redondeado, (0, 0, 255), 2)

        # Calcula el diámetro del círculo
        diametro = 2 * radio_redondeado

        # Calcula la relación entre el ancho y el alto del círculo
        relacion_ancho_alto = frame.shape[1] / frame.shape[0]

        # Define un umbral para considerar si el círculo está deformado
        umbral_deformacion = 0.9

        # Agrega el texto del diámetro y la información de deformación en una esquina
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, f'Diametro: {diametro}px', (20, 30), font, 1, (0, 0, 255), 2)
        if abs(relacion_ancho_alto - 1) < umbral_deformacion:
            cv2.putText(frame, 'No Deformado', (20, 60), font, 1, (0, 255, 0), 2)
        else:
            cv2.putText(frame, 'Deformado', (20, 60), font, 1, (0, 0, 255), 2)

    return frame

if __name__ == "__main__":
    # Abre el video
    video = cv2.VideoCapture("video.mp4")

    while True:
        ret, frame = video.read()

        if not ret:
            break

        # Procesa el fotograma
        frame_procesado = procesar_fotograma(frame)

        # Muestra el resultado
        cv2.imshow("Video con círculo resaltado", frame_procesado)

        # Sale del bucle si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Libera el video y cierra la ventana
    video.release()
    cv2.destroyAllWindows()
