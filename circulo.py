import cv2
import numpy as np

# Abre el video
cap = cv2.VideoCapture('video.mp4')

frame_counter = 0  # Inicializa el contador de fotogramas
diameter_values = []  # Lista para almacenar los últimos 20 valores de diámetro
last_message = ''  # Inicializa el último mensaje
diameter_average = 0  # Inicializa la media de diámetro

while True:  # Bucle infinito para mantener el video en bucle
    ret, frame = cap.read()

    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reinicia el video al principio
        continue

    # Incrementa el contador de fotogramas
    frame_counter += 1

    # Convierte el frame a formato HSV para el espacio de color
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define el rango de colores amarillos en HSV
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([40, 255, 255])

    # Filtra los píxeles amarillos en el rango definido
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Aplica eliminación de ruido y dilatación para mejorar la detección de contornos
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # Encuentra los contornos en la máscara
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    largest_circle = None
    max_circle_radius = 0

    for contour in contours:
        # Encuentra el círculo que se ajusta mejor al contorno
        (x, y), radius = cv2.minEnclosingCircle(contour)
        center = (int(x), int(y))
        radius = int(radius)

        # Filtra el círculo de mayor tamaño
        if radius > max_circle_radius:
            max_circle_radius = radius
            largest_circle = (center, radius)

    if largest_circle is not None and frame_counter % 10 == 0:
        (center, radius) = largest_circle
        diameter = 2 * radius

        # Verifica si el valor de diámetro no es igual a cero antes de agregarlo a la lista
        if diameter != 0:
            diameter_values.append(diameter)

            # Calcula la media de los últimos 20 valores de diámetro
            if len(diameter_values) > 20:
                diameter_values.pop(0)  # Elimina el valor más antiguo si hay más de 20 en la lista
            diameter_average = sum(diameter_values) / len(diameter_values)

            # Dibuja un círculo rosa alrededor del círculo detectado
            cv2.circle(frame, center, radius, (255, 0, 255), 2)

            # Agrega el texto "Diametro" cerca del círculo
            cv2.putText(
                frame,
                'Diametro',
                (int(x - radius), int(y) - 10),  # Posición cerca del círculo
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,  # Tamaño del texto
                (255, 0, 0),  # Color azul
                1,
            )

            # Verifica si el valor de diámetro supera el 50% de la media
            if diameter > 1.5 * diameter_average:
                last_message = 'Ligera deformación'  # Muestra "Ligera deformación" si supera el 50%
            else:
                last_message = f'Diámetro: {diameter:.2f} píxeles'
        else:
            last_message = 'Calculando'  # Muestra "Calculando" si el diámetro es cero

    # Ajusta el tamaño de la ventana de visualización
    frame = cv2.resize(frame, (640, 480))

    # Muestra el último mensaje en el video
    cv2.putText(
        frame,
        last_message,
        (10, 30),  # Posición en la esquina superior izquierda
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,  # Tamaño del texto
        (0, 255, 255),  # Color amarillo
        2,
    )

    cv2.imshow('Video en bucle con el círculo amarillo más grande', frame)

    # Muestra la información en la consola
    print(last_message)

    # Espera una tecla y verifica si 'q' (o cualquier tecla que desees) es presionada
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):  # Presiona 'q' para salir
        break

cap.release()
cv2.destroyAllWindows()
