from ultralytics import YOLO
from PIL import Image


YOLO_MODEL_PATH = "utils/yolo11n.pt"


class YoloModel:
    def __init__(self, model_path=YOLO_MODEL_PATH):
        self.model = YOLO(model_path)

    def count_people_in_img(self, source: Image.Image) -> tuple[int, Image.Image]:
        results = self.model.predict(source=source, classes=[0])
        results[0].save("annotated.jpg")
        plot_img = Image.open("annotated.jpg")
        return len(results[0].boxes), plot_img
