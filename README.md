# Control de Dispositivos mediante Gestos y Visión Artificial

Este repositorio contiene la implementación de un sistema de interfaz hombre-máquina (HMI) que utiliza **Visión Artificial** para detectar gestos de la mano y controlar actuadores físicos a través de una placa **Arduino**.

**Autor:** Eduardo Cano García  
**Universidad:** Universidad Autónoma Chapingo  
**Carrera:** Ingeniería Mecatrónica  

---

## 📂 Estructura del Código

El proyecto está modularizado en tres scripts principales para facilitar el mantenimiento y la escalabilidad:

### 1. `live.py` (Módulo de Visión)
Este script contiene la lógica de procesamiento de imagen utilizando **OpenCV** y **MediaPipe**.
* **Clase `HandDetector`:** Encapsula las funciones de MediaPipe.
* **`findHands()`:** Detecta y dibuja el esqueleto de la mano sobre el frame de video.
* **`findPosition()`:** Extrae las coordenadas $(x, y)$ de los 21 puntos característicos de la mano e identifica qué dedos están levantados.

### 2. `Arduino.py` (Módulo de Comunicación)
Gestiona la conexión Serial entre la computadora y la placa Arduino.
* **Clase `SerialObject`:** Se encarga de abrir el puerto COM, configurar la velocidad de baudios (Baud Rate) y enviar datos formateados.
* Maneja excepciones en caso de que el puerto no esté disponible.

### 3. `Proyect_2_P_1.py` (Script Principal)
Es el archivo ejecutable que integra los módulos anteriores.
* Inicializa la cámara y los objetos de detección.
* Ejecuta el bucle principal de captura.
* Traduce los gestos detectados (ej. número de dedos) en comandos lógicos.
* Envía la señal de control al Arduino.

---

## 🛠️ Requisitos de Software

Para ejecutar este proyecto en tu computadora, necesitas instalar **Python** y las siguientes librerías:

```bash
pip install opencv-python
pip install mediapipe
pip install pyserial
