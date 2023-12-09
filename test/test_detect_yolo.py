from turret.detect_yolo import TFLiteObjectDetector
import cv2
import numpy as np

def test_init_yolo():
    detector = TFLiteObjectDetector()
    assert detector is not None
    # check the categories
    assert detector.categories is not None
    assert isinstance(detector.categories, list)
    assert len(detector.categories) > 0
    assert detector.categories[0] == "person"
    
def test_detect_yolo():
    detector = TFLiteObjectDetector()
    assert detector is not None
    # Run the inference
    test_image_path = "test/turret_targets.jpg"
    test_image = cv2.imread(test_image_path)
    # convert to RGB
    test_image = cv2.cvtColor(test_image, cv2.COLOR_BGR2RGB)
    assert test_image is not None
    assert isinstance(test_image, np.ndarray)

    # Run the inference
    output_data = detector.run_inference(test_image)
    assert output_data is not None
    assert len(output_data) == 1
