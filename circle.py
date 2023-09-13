import cv2
import numpy as np
import vlc

# Abre el video con OpenCV
cap = cv2.VideoCapture('Video.mp4')

# Configura el reproductor VLC
instance = vlc.Instance('--no-xlib')
player = instance.media_player_new()
media = instance.media_new('Video.mp4')
player.set_media(media)
player.audio_toggle_mute()  # Desactiva el audio por defecto

# Inicializa una ventana de OpenCV para mostrar el procesamiento
cv2.namedWindow('Deteccion de deformacion en tuberia', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Deteccion de deformacion en tuberia', 640, 480)

while True:
    ret, frame = cap.read()

    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reinicia el video al principio si llega al final
        player.set_time(0)  # Reinicia el tiempo del reproductor VLC
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

<<<<<<< Updated upstream
    # Espera una tecla y verifica si 'q' (o cualquier tecla que desees) es presionada
=======
    # Calcula el porcentaje de píxeles azules en relación al verde en la región central
    blue_pixels = np.sum(central_region[:, :, 0] == 255)
    green_pixels = np.sum(central_region[:, :, 1] == 255)
    total_pixels = central_region.shape[0] * central_region.shape[1]
    blue_percentage = (blue_pixels / green_pixels) * 100

    # Verifica si el porcentaje es superior al 9% y muestra "deformación detectada" en el frame
    if blue_percentage > 9:
        cv2.putText(frame, "Deformación detectada", (width - 300, height - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Reproduce el audio
    audio_time = int(cap.get(cv2.CAP_PROP_POS_MSEC))
    player.set_time(audio_time)
    player.audio_toggle_mute()  # Activa el audio

    # Muestra el frame con las curvas, líneas y texto adicional en la región central en una ventana
    cv2.imshow('Deteccion de deformacion en tuberia', frame)

    # Captura el evento de cierre de la ventana
>>>>>>> Stashed changes
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):  # Presiona 'q' para salir
        break

# Libera los objetos de captura y reproductor VLC, y cierra todas las ventanas
cap.release()
player.release()
cv2.destroyAllWindows()


