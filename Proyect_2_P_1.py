# Importamos las librerías que vamos a usar.
# 'cv2' es la librería OpenCV, que nos ayuda a trabajar con imágenes y videos.
import cv2
# 'YOLO' es parte de la librería ultralytics, que nos permite cargar y usar modelos YOLO.
from ultralytics import YOLO

# --- PASO 1: Cargar el modelo entrenado ---
# Aquí le decimos a nuestro programa dónde está el modelo (nuestro archivo 'best.pt').
model_path = './runs/detect/train/weights/best.pt'

# Cargamos el modelo YOLO. Ahora el programa ya sabe cómo "ver" los pollos.
model = YOLO(model_path)

# --- PASO 2: Cargar una imagen para analizar ---
# Vamos a tomar una foto y pasársela a nuestro modelo para que la analice.
image_path = 'images/image--11-.jpg'
# Leemos la imagen usando OpenCV. 'img' ahora contiene los datos de la imagen.
img = cv2.imread(image_path)
# Redimensionamos la imagen a un tamaño más manejable (600 píxeles de ancho por 400 de alto).
# Esto es útil para que el procesamiento sea más rápido y para mostrarla mejor en pantalla.
img = cv2.resize(img, (710, 640), interpolation=cv2.INTER_AREA)

# --- Verificamos si la imagen se cargó correctamente ---
# Si 'img' es None, significa que hubo un error y la imagen no se encontró o no se pudo abrir.
if img is None:
    print(f"Error: No se pudo cargar la imagen en: {image_path}")
else:
    # --- PASO 3: Realizar la detección de objetos (inferencia) ---
    # Le pedimos al modelo que "prediga" dónde están los pollos en la imagen.
    # 'source=img' le da la imagen a analizar.
    # 'save=False' significa que no queremos que guarde la imagen procesada en un archivo.
    # 'conf=0.5' es el umbral de confianza: solo queremos ver las detecciones
    # donde el modelo esté al menos 50% seguro de que encontró un pollo.
    results = model.predict(source=img, save=False, conf=0.5)

    # --- PASO 4: Procesar los resultados y dibujarlos en la imagen ---
    # Hacemos una copia de la imagen original para poder dibujar sobre ella sin modificar la original.
    annotated_img = img.copy()
    # Creamos una variable para contar cuántos pollos detectamos. Empezamos en cero.
    chicken_count = 0

    # 'results' puede contener resultados para varias imágenes, pero como solo pasamos una,
    # solo habrá un elemento en 'results'.
    for r in results:
        # Extraemos las coordenadas de los cuadros que el modelo dibujó.
        # 'xyxy' significa (x1, y1, x2, y2) que son las esquinas superior izquierda e inferior derecha del cuadro.
        boxes = r.boxes.xyxy.cpu().numpy()
        # Obtenemos el nivel de confianza para cada detección (qué tan seguro está el modelo).
        confs = r.boxes.conf.cpu().numpy()
        # Obtenemos el ID de la clase para cada detección (por ejemplo, 0 para "pollo_muerto", 1 para "pollo_vivo").
        clss = r.boxes.cls.cpu().numpy()

        # Recorremos cada detección individual que el modelo encontró.
        for i in range(len(boxes)):
            # Convertimos las coordenadas a números enteros para poder usarlas con OpenCV.
            x1, y1, x2, y2 = map(int, boxes[i])
            confidence = confs[i]
            class_id = int(clss[i])

            # Obtenemos el nombre real de la clase a partir de su ID.
            # 'model.names' es un diccionario que mapea IDs a nombres (ej: {0: 'dead_chicken', 1: 'healthy'}).
            # Si 'model.names' no existe (muy raro), usará 'Class X'.
            class_name = model.names[class_id] if hasattr(model, 'names') else f'Class {class_id}'

            # Verificamos si la clase detectada es uno de los tipos de pollo que queremos contar.
            if class_name in ['Dead_chicken', 'Healthly']:
                chicken_count += 1 # Si es un pollo, aumentamos el contador.

            # Creamos la etiqueta de texto para mostrar en el cuadro delimitador.
            # Por ejemplo: "dead_chicken 0.95"
            label = f"{class_name} {confidence:.2f} {chicken_count}"
            # Definimos el color del cuadro delimitador (verde en formato BGR de OpenCV).
            color = (0, 255, 0)
            # Definimos el grosor de la línea del cuadro.
            thickness = 2

            # Dibujamos el cuadro delimitador en la imagen.
            cv2.rectangle(annotated_img, (x1, y1), (x2, y2), color, thickness)

            # Calculamos dónde colocar el texto de la etiqueta para que no se salga de la imagen.
            text_x = x1
            text_y = y1 - 10 if y1 - 10 > 10 else y1 + 10 # Si está muy arriba, lo ponemos un poco más abajo.
            # Dibujamos el texto de la etiqueta en la imagen.
            # Usamos una fuente, escala y color específicos.
            cv2.putText(annotated_img, label, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), thickness, cv2.LINE_AA)


    # --- PASO 5: Mostrar la imagen final y esperar a que el usuario presione una tecla ---
    # Abrimos una ventana para mostrar la imagen con las detecciones y el contador.
    cv2.imshow('Detecciones con Contador de Pollos', annotated_img)
    # Esperamos a que el usuario presione cualquier tecla. Si ponemos 0, espera indefinidamente.
    cv2.waitKey(0)
    # Cerramos todas las ventanas de OpenCV abiertas.
    cv2.destroyAllWindows()