from ultralytics import YOLO
from PIL import Image


YOLO_MODEL_PATH = "yolo11n.pt"

class YoloModel:
    def __init__(self, model_path = YOLO_MODEL_PATH):
        self.model = YOLO(model_path)
    

    def count_people_in_img(self, source: Image.Image) -> tuple[int, Image.Image]:
        results = self.model.predict(source=source, classes=[0])
        results[0].save("output.jpg")
        plot_img = results[0].plot(pil=True)
        return len(results[0].boxes), plot_img
    