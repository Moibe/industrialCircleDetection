import cv2
import numpy as np

# Abre el video
cap = cv2.VideoCapture('Video.mp4')

while True:
    ret, frame = cap.read()

    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reinicia el video al principio si llega al final
        continue

    # Redimensiona el frame para una ventana más pequeña
    frame = cv2.resize(frame, (640, 360))

    ####### CIRCULO 

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
            cv2.putText(frame, '', (20, 60), font, 1, (0, 255, 0), 2)
        else:
            cv2.putText(frame, 'Deformado', (20, 60), font, 1, (0, 0, 255), 2)

    ####### CIRCULO

    # Obtiene las dimensiones de la ventana
    height, width = frame.shape[:2]

    # # Define la región central (10% en horizontal y 55% en vertical)
    x1 = int(0.10 * width)
    x2 = int(0.95 * width)
    y1 = int(0.10 * height)
    y2 = int(0.65 * height)

    # Recorta la región central
    central_region = frame[y1:y2, x1:x2]

    # Convierte la región recortada a escala de grises
    gray = cv2.cvtColor(central_region, cv2.COLOR_BGR2GRAY)

    # Aplica un desenfoque para reducir el ruido
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Detecta bordes en la imagen
    edges = cv2.Canny(blurred, 50, 150)

    # Encuentra contornos en los bordes
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Dibuja las curvas detectadas en la región central en verde
    #cv2.drawContours(central_region, contours, -1, (0, 255, 0), 2)

    # Detecta líneas en la región central utilizando la transformada de Hough
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=50, maxLineGap=10)

    if lines is not None:
        # Agrupa líneas cercanas en pares
        line_pairs = []
        for i in range(len(lines)):
            for j in range(i + 1, len(lines)):
                line1 = lines[i][0]
                line2 = lines[j][0]
                distance = np.sqrt((line1[0] - line2[0]) ** 2 + (line1[1] - line2[1]) ** 2)
                if distance < 20:  # Ajusta este valor según la distancia que consideres cercana
                    line_pairs.append((line1, line2))

        # Dibuja las líneas en azul si forman parte de un par cercano
        for line1, line2 in line_pairs:
            x1, y1, x2, y2 = line1
            cv2.line(central_region, (x1, y1), (x2, y2), (255, 0, 0), 2)
            x1, y1, x2, y2 = line2
            cv2.line(central_region, (x1, y1), (x2, y2), (255, 0, 0), 2)

    # Calcula el porcentaje de píxeles azules en relación al verde en la región central
    blue_pixels = np.sum(central_region[:, :, 0] == 255)
    green_pixels = np.sum(central_region[:, :, 1] == 255)
    total_pixels = central_region.shape[0] * central_region.shape[1]
    blue_percentage = (blue_pixels / green_pixels) * 100

    # Verifica si el porcentaje es superior al 9% y muestra "deformación detectada" en el frame
    if blue_percentage > 9:
        cv2.putText(frame, "Deformacion detectada", (width - 300, height - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    # Muestra el frame con las curvas, líneas y texto adicional en la región central en una ventana
    cv2.imshow('Detector de circulo y deformaciones', frame)

    # Espera medio segundo antes de mostrar el siguiente fotograma
    key = cv2.waitKey(100) & 0xFF
 
    #Termina el programa con 'q'
    if key == ord('q'):  # Presiona 'q' para salir
        break

cap.release()
cv2.destroyAllWindows()