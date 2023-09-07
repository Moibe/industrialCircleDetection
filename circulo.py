import cv2
import numpy as np

# Abre el video
cap = cv2.VideoCapture('video.mp4')

frame_counter = 0  # Inicializa el contador de fotogramas

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

    # Encuentra los contornos en la máscara
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Encuentra el contorno más grande
    largest_contour = None
    max_area = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_area:
            max_area = area
            largest_contour = contour

    if largest_contour is not None and frame_counter % 10 == 0:
        # Encuentra el círculo que se ajusta mejor al contorno
        (x, y), radius = cv2.minEnclosingCircle(largest_contour)
        center = (int(x), int(y))
        radius = int(radius)
        diameter = 2 * radius

        if diameter != 0:
            # Dibuja el círculo encontrado en la ventana de visualización
            cv2.circle(frame, center, radius, (0, 255, 0), 2)
            cv2.putText(
                frame,
                f'Diámetro: {diameter:.2f} píxeles',
                (int(x) - 70, int(y) - 30),
                cv2.FONT_HERSHEY_SIMPLEX,  # Utiliza la fuente predeterminada
                0.5,
                (0, 0, 255),
                2,
            )

            # Muestra la información en la consola
            print(f'Diámetro: {diameter:.2f} píxeles')

    cv2.imshow('Video en bucle con el círculo amarillo más grande', frame)

    # Espera una tecla y verifica si 'q' (o cualquier tecla que desees) es presionada
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):  # Presiona 'q' para salir
        break

cap.release()
cv2.destroyAllWindows()
