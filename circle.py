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
    frame = cv2.resize(frame, (640, 480))

    # Convierte el frame a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Aplica un desenfoque para reducir el ruido
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Detecta bordes en la imagen
    edges = cv2.Canny(blurred, 50, 150)

    # Encuentra contornos en los bordes
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filtra contornos que pueden ser medias elipses
    ellipse_contours = []

    for contour in contours:
        if len(contour) >= 5:
            ellipse = cv2.fitEllipse(contour)
            if 0 < ellipse[2] < 180:  # Filtra medias elipses (0 < ángulo < 180 grados)
                ellipse_contours.append(contour)

    # Dibuja las medias elipses encontradas
    cv2.drawContours(frame, ellipse_contours, -1, (0, 0, 255), 2)

    # Muestra el frame con las medias elipses en una ventana
    cv2.imshow('Video con medias elipses detectadas', frame)

    # Espera una tecla y verifica si 'q' (o cualquier tecla que desees) es presionada
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):  # Presiona 'q' para salir
        break

cap.release()
cv2.destroyAllWindows()


