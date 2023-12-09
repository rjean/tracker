import numpy as np
import cv2
from tflite_runtime.interpreter import Interpreter

import numpy as np

def compute_iou(box1, box2):
    """
    Compute the Intersection over Union (IoU) of two bounding boxes.

    :param box1: (list or array) bounding box, format: [x1, y1, x2, y2]
    :param box2: (list or array) bounding box, format: [x1, y1, x2, y2]
    :return: float IoU value.
    """
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    intersection_area = max(0, x2 - x1) * max(0, y2 - y1)
    box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
    box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])

    union_area = box1_area + box2_area - intersection_area

    if union_area == 0:
        return 0

    return intersection_area / union_area

def non_max_suppression(boxes, scores, iou_threshold):
    """
    Remove overlapping bounding boxes with lower confidence scores.

    :param boxes: (list of lists or 2D numpy array) bounding boxes, format: [x1, y1, x2, y2].
    :param scores: (list or 1D numpy array) confidence scores for each bounding box.
    :param iou_threshold: (float) threshold where overlapping boxes are removed.
    :return: list of indices of boxes to keep.
    """
    if len(boxes) == 0:
        return []

    if isinstance(boxes, list):
        boxes = np.array(boxes)

    sorted_indices = np.argsort(scores)[::-1]
    selected_indices = []

    while len(sorted_indices) > 0:
        current_index = sorted_indices[0]
        selected_indices.append(current_index)

        current_box = boxes[current_index]
        remaining_boxes = boxes[sorted_indices[1:]]

        ious = np.array([compute_iou(current_box, box) for box in remaining_boxes])

        sorted_indices = sorted_indices[1:][ious < iou_threshold]

    return selected_indices

class TFLiteObjectDetector:
    def __init__(self, model_path="weights/yolov8n_integer_quant.tflite", min_confidence=0.3, categories_file="data/coco_labels.txt"):
        # Load TFLite model and allocate tensors
        self.interpreter = Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()

        # Get input and output tensors information
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.min_confidence = min_confidence
        self.categories = self.load_categories(categories_file)

    def load_categories(self, categories_file):
        with open(categories_file, 'r') as f:
            return [line.strip().split(" ")[-1].strip() for line in f.readlines()]
        

    def preprocess_image(self, image: np.ndarray):
        # Preprocess the image for the model
        #img = cv2.imread(image_path)
        img = cv2.resize(image, (self.input_details[0]['shape'][2], self.input_details[0]['shape'][1]))
        img = np.expand_dims(img, axis=0)
        if self.input_details[0]['dtype'] == np.float32:
            img = (img - 127.5) / 127.5
        return img.astype(self.input_details[0]['dtype'])

    def run_inference(self, image_path):
        # Preprocess the image
        input_data = self.preprocess_image(image_path)

        # Set the tensor to point to the input data to be inferred
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)

        # Run the inference
        self.interpreter.invoke()

        # Get the result
        output_data = self.interpreter.get_tensor(self.output_details[0]['index'])

        # Postprocess the result
        output_data = np.squeeze(output_data)
        output_data = np.transpose(output_data, [1,0])

        # Get the confidence level for each prediction and filter out the predictions with low confidence
        confidences = output_data[:,4]
        filtered_data = output_data[confidences >= self.min_confidence]
        # get the class id for each prediction using the argmax function
        class_ids = np.argmax(filtered_data[:,5:], axis=0)
        # get the bounding boxes for each prediction
        filtered_boxes = filtered_data[:,:4]
        filtered_confidences = filtered_data[:,4]
        filtered_class_ids = class_ids
        # Convert filtered boxes from x, y, w, h to x1, y1, x2, y2
        filtered_boxes[:,2] += filtered_boxes[:,0]
        filtered_boxes[:,3] += filtered_boxes[:,1]
        # Convert the boxes from relative coordinates to absolute coordinates
        filtered_boxes[:,0] *= image_path.shape[1]
        filtered_boxes[:,1] *= image_path.shape[0]
        filtered_boxes[:,2] *= image_path.shape[1]
        filtered_boxes[:,3] *= image_path.shape[0]
        # Convert the boxes from float to int
        filtered_boxes = filtered_boxes.astype(int)
        # Apply non-max suppression
        nms_boxes = non_max_suppression(filtered_boxes, filtered_confidences, 0.5)
        nms_confidences = confidences[nms_boxes]
        nms_class_ids = class_ids[nms_boxes]
        nms_boxes = filtered_boxes[:,nms_boxes]

        return  nms_confidences, nms_boxes, nms_class_ids
