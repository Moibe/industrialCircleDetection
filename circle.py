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

    # Encuentra los contornos en la imagen
    contours, _ = cv2.findContours(blurred, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Encuentra la elipse más grande
    largest_ellipse = None
    max_area = 0

    for contour in contours:
        if len(contour) >= 5:
            ellipse = cv2.fitEllipse(contour)
            area = ellipse[1][0] * ellipse[1][1] * np.pi  # Área de la elipse

            if area > max_area:
                max_area = area
                largest_ellipse = ellipse

    if largest_ellipse is not None:
        # Dibuja la elipse más grande
        cv2.ellipse(frame, largest_ellipse, (0, 0, 255), 2)

    # Muestra el frame con la elipse más grande en una ventana
    cv2.imshow('Video con la elipse más grande detectada', frame)

    # Espera una tecla y verifica si 'q' (o cualquier tecla que desees) es presionada
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):  # Presiona 'q' para salir
        break

cap.release()
cv2.destroyAllWindows()

