import cv2
import math
import serial
import time

arduino = serial.Serial(port='COM4', baudrate=9600, timeout=1)
time.sleep(2)

def send(estado):
    if estado == True:
        arduino.write(b'1')
    else:
        arduino.write(b'0')

class DetectBirds(object):
    def _init_(self, camera_url, mx_num_birds=3):
        self.cap = cv2.VideoCapture(camera_url)
        self.birdsCascade = cv2.CascadeClassifier("birds1.xml")
        self.MAX_NUM_BIRDS = mx_num_birds
        self.running = True
        self.total_unique_birds = 0
        self.previous_centers = []
        self.last_printed_multiple = 0  # Nuevo: Para monitorear múltiplos de 8

    def is_new_bird(self, center, threshold=50):
        for prev_center in self.previous_centers:
            distance = math.hypot(center[0] - prev_center[0], center[1] - prev_center[1])
            if distance < threshold:
                return False
        return True

    def detect(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.equalizeHist(gray)

            birds = self.birdsCascade.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=6,
                minSize=(30, 30),
                maxSize=(300, 300),
                flags=cv2.CASCADE_SCALE_IMAGE
            )

            valid_birds = []
            for (x, y, w, h) in birds:
                area = w * h
                aspect_ratio = w / h if h != 0 else 0

                if area < 1000:
                    continue
                if aspect_ratio < 0.5 or aspect_ratio > 2.0:
                    continue

                center = (x + w // 2, y + h // 2)

                if self.is_new_bird(center):
                    self.total_unique_birds += 1
                    self.previous_centers.append(center)

                    if self.total_unique_birds // 8 > self.last_printed_multiple:
                        self.last_printed_multiple = self.total_unique_birds // 8
                        print("Aves alerta 1")
                        aves = True
                    else:
                        aves = False

                    alerta = send(aves)

                valid_birds.append((x, y, w, h))

            if len(valid_birds) >= self.MAX_NUM_BIRDS:
                print(f"Detected {len(valid_birds)} birds in frame")

            cv2.putText(frame, f"Total unique birds: {self.total_unique_birds}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            cv2.imshow('Bird Detection', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.running = False

        print(f"\n>>> Total unique birds detected during the video: {self.total_unique_birds}")
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    D = DetectBirds("birds.mp4")
    D.detect()