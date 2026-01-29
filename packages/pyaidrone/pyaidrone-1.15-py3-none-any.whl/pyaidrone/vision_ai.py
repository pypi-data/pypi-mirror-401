import cv2
import numpy as np
import time
from typing import Optional, Union, List, Tuple

# --- [파트 1: 기존 vision_enhanced의 핵심 유틸리티] ---

class FPSMeter:
    def __init__(self):
        self.p_time = 0
    def get_fps(self):
        c_time = time.time()
        fps = 1 / (c_time - self.p_time) if (c_time - self.p_time) > 0 else 0
        self.p_time = c_time
        return int(fps)

def draw_box(img, box, label="", color=(0, 255, 0), thickness=2):
    x1, y1, x2, y2 = map(int, box)
    cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness)
    if label:
        cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

def letterbox(img, new_shape=(640, 640), color=(114, 114, 114)):
    shape = img.shape[:2]
    if isinstance(new_shape, int): new_shape = (new_shape, new_shape)
    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]
    dw /= 2; dh /= 2
    if shape[::-1] != new_unpad:
        img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
    return img, r, (left, top)

def nms(boxes, scores, iou_threshold=0.45):
    if len(boxes) == 0: return []
    indices = cv2.dnn.NMSBoxes(boxes, scores, 0.1, iou_threshold)
    return indices.flatten() if len(indices) > 0 else []

# --- [파트 2: 좌표 변환 및 컨투어 유틸리티] ---

def xywh_to_xyxy(x, y, w, h):
    return [x, y, x + w, y + h]

def xyxy_to_xywh(x1, y1, x2, y2):
    return [x1, y1, x2 - x1, y2 - y1]

def largest_contour(contours):
    if not contours: return None
    return max(contours, key=cv2.contourArea)

def contour_centroid(c):
    M = cv2.moments(c)
    if M['m00'] == 0: return None
    return (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

# --- [파트 3: TFLite AI 추론 클래스 (기존 vision_ai 핵심)] ---

class DetResult:
    """AI 인식 결과를 깔끔하게 담는 바구니"""
    def __init__(self, class_id, score, box):
        self.class_id = class_id
        self.score = score
        self.box = box  # [x1, y1, x2, y2]

def yolo_decode(outputs, orig_wh, inp_wh, r, pad):
    choices = outputs[0]
    if len(choices.shape) == 3:
        choices = choices[0].transpose()
    
    boxes_for_nms, scores, class_ids, raw_boxes = [], [], [], []
    
    for det in choices:
        cls_scores = det[4:] 
        score = np.max(cls_scores)
        if score > 0.25:
            cls_id = np.argmax(cls_scores)
            cx, cy, w, h = det[0:4]
            
            # 좌표 복원
            x1 = (cx - w / 2 - pad[0]) / r
            y1 = (cy - h / 2 - pad[1]) / r
            x2 = (cx + w / 2 - pad[0]) / r
            y2 = (cy + h / 2 - pad[1]) / r
            
            # NMS는 [x, y, w, h] 형식을 선호함
            boxes_for_nms.append([int(x1), int(y1), int((x2-x1)), int((y2-y1))])
            raw_boxes.append([x1, y1, x2, y2])
            scores.append(float(score))
            class_ids.append(int(cls_id))
            
    # nms 함수 호출 시 수정된 리스트 전달
    indices = nms(boxes_for_nms, scores)
    return [DetResult(class_ids[i], scores[i], raw_boxes[i]) for i in indices]
    

class TFLiteDetector:
    def __init__(self, model_path: str):
        try:
            # 1. 전체 TensorFlow가 설치된 경우 (현재 선생님 환경)
            from tensorflow.lite.interpreter import Interpreter
        except ImportError:
            try:
                # 2. 경량 tflite-runtime만 설치된 경우
                from tflite_runtime.interpreter import Interpreter
            except ImportError:
                print("❌ TFLite를 실행할 라이브러리(tensorflow 또는 tflite-runtime)가 없습니다.")
                return

        self.interpreter = Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    def infer(self, frame, decode_fn):
        # 전처리: 모델 입력 크기에 맞춰 리사이즈
        ih, iw = self.input_details[0]['shape'][1:3]
        input_data, r, pad = letterbox(frame, (ih, iw))
        input_data = input_data.astype(np.float32) / 255.0
        input_data = np.expand_dims(input_data, axis=0)

        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()
        
        # 출력 데이터 후처리
        outputs = [self.interpreter.get_tensor(out['index']) for out in self.output_details]
        return decode_fn(outputs, (frame.shape[1], frame.shape[0]), (iw, ih), r, pad)

# --- [파트 4: 통합 헬퍼] ---

def draw_box_xywh(img, box_xywh, label="", color=(0, 255, 0)):
    x, y, w, h = box_xywh
    draw_box(img, (x, y, x + w, y + h), label, color)

    
# --- [OpenCV의 CSRT 트래커] ---   

class VisionTracker:
    def __init__(self):
        self.tracker = None
        self.is_tracking = False

    def set_target(self, frame, x, y):    # 클릭한 지점을 추적 대상으로 지정.
        """클릭한 지점 주변(80x80)을 추적 대상으로 설정"""
        self.tracker = cv2.TrackerCSRT_create()
        roi = (int(x - 40), int(y - 40), 80, 80)
        self.tracker.init(frame, roi)
        self.is_tracking = True

    def get_error(self, frame):  # 현재 추적 중인 물체의 중심 좌표와 화면 중심과의 오차를 반환.
        """화면 중심(320, 240)과 물체 중심의 차이 계산"""
        if not self.is_tracking: return None
        
        success, box = self.tracker.update(frame)
        if success:
            x, y, w, h = [int(v) for v in box]
            target_center_x = x + w // 2
            target_center_y = y + h // 2
            # 중심과의 오차 (가운데가 0)
            error_x = target_center_x - 320
            error_y = 240 - target_center_y
            return error_x, error_y, (x, y, w, h)
        
        self.is_tracking = False
        return None