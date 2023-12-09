from ultralytics import YOLO

model = YOLO("yolov8n.pt")

model.export(format="tflite", int8=True, imgsz=(128,128))

