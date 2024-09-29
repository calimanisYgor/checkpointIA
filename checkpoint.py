import cv2
import requests
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
import threading
import time

class SleepDetectionApp:
    # Construtor da classe e inicialização dos componentes
    def __init__(self, api_key, model_id):
        self.api_key = api_key
        self.model_id = model_id
        self.cap = cv2.VideoCapture(0)
        self.frame = None
        self.predictions = None
        self.stop_event = threading.Event()
        self.frame_lock = threading.Lock()

        self.root = tk.Tk()
        self.root.title("Detecção de Sono em Tempo Real")
        self.label_img = tk.Label(self.root)
        self.label_img.pack()

        self.video_thread = threading.Thread(target=self.capture_video)
        self.video_thread.daemon = True
        self.video_thread.start()

        self.infer_thread = threading.Thread(target=self.infer_periodically)
        self.infer_thread.daemon = True
        self.infer_thread.start()

        self.update_frame()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    # Captura de vídeo da câmera
    def capture_video(self):
        while not self.stop_event.is_set():
            ret, frame = self.cap.read()
            if ret:
                frame_resized = cv2.resize(frame, (640, 640))
                with self.frame_lock:
                    self.frame = frame_resized
            else:
                time.sleep(0.01)

    # Inferência da imagem usando o modelo da API do Roboflow
    def infer_image(self, image):
        try:
            _, img_encoded = cv2.imencode('.jpg', image)
            url = f"https://detect.roboflow.com/{self.model_id}?api_key={self.api_key}"
            response = requests.post(url, files={"file": img_encoded.tobytes()})
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Erro ao enviar para o modelo: {str(e)}")
        return None

    # Inferência periódica em segundo plano
    def infer_periodically(self):
        while not self.stop_event.is_set():
            with self.frame_lock:
                current_frame = self.frame.copy() if self.frame is not None else None
            if current_frame is not None:
                predictions = self.infer_image(current_frame)
                with self.frame_lock:
                    self.predictions = predictions
            time.sleep(0.5)

    # Desenho das previsões na imagem
    def draw_predictions(self, image, predictions):
        if predictions and 'predictions' in predictions:
            for pred in predictions['predictions']:
                x, y, w, h = pred['x'], pred['y'], pred['width'], pred['height']
                label = pred['class']
                cv2.rectangle(image, (int(x - w / 2), int(y - h / 2)),
                              (int(x + w / 2), int(y + h / 2)), (0, 255, 0), 2)
                cv2.putText(image, label, (int(x - w / 2), int(y - h / 2) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
        return image

    # Atualização do quadro na interface gráfica
    def update_frame(self):
        with self.frame_lock:
            frame_to_show = self.frame.copy() if self.frame is not None else None
            predictions = self.predictions

        if frame_to_show is not None:
            if predictions:
                frame_with_predictions = self.draw_predictions(frame_to_show, predictions)
            else:
                frame_with_predictions = frame_to_show

            frame_rgb = cv2.cvtColor(frame_with_predictions, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(image=img)
            self.label_img.imgtk = imgtk
            self.label_img.configure(image=imgtk)
        self.root.after(15, self.update_frame)

    # Encerramento do aplicativo e liberação da câmera
    def on_closing(self):
        self.stop_event.set()
        self.cap.release()
        self.root.destroy()

# Execução do aplicativo
if __name__ == "__main__":
    API_KEY = "chave_da_api" 
    MODEL_ID = "detector-de-sono/3" 
    app = SleepDetectionApp(API_KEY, MODEL_ID)
