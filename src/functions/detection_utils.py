import cv2
import os
from ultralytics import YOLO
from state_manager import StateManager
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

MODEL_PATH = "src/models/object-detection-v1.pt"

def handle_detection(conf, main_window):
    state_manager = StateManager()
    
    select_content_widget = main_window.get_select_content_widget()
        
    image_path = state_manager.get('image_path')
    
    if image_path.endswith((".mp4", ".avi", ".mov")):
        # Video dosyası ise video tespiti yap
        handle_video_detection(image_path, conf, main_window)
        return

    print(f"Selected Image Path: {image_path}")
    print(f"Confidence Threshold: {conf}")

    try:
        model = YOLO(MODEL_PATH)
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    try:
        results = model.predict(source=image_path, conf=conf, save=False, iou=0.2)[0]        
        # Orijinal görseli oku
        image = cv2.imread(image_path)

        # Kutular
        boxes = results.boxes.xyxy.cpu().numpy()
        confidences = results.boxes.conf.cpu().numpy()  
        class_ids = results.boxes.cls.cpu().numpy().astype(int)  

        # Etiket isimleri
        label_map = results.names

        for box, conf_score, cls_id in zip(boxes, confidences, class_ids):
            x1, y1, x2, y2 = map(int, box)
            label = f"{label_map[cls_id]} {conf_score:.2f}"
            
            # Dikdörtgen çiz
            cv2.rectangle(image, (x1, y1), (x2, y2), color=(0, 255, 0), thickness=2)
            
            # Etiketi çiz
            cv2.putText(image, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        # Görseli kaydet
        output_path = "output/annotated_result.jpg"
        cv2.imwrite(output_path, image)
                        
        # --- GÖRSELİ GUI’DE GÖSTER ---
        pixmap = QPixmap(output_path)
        if not pixmap.isNull():
            # media_label = select_content_widget.get_media_label()
            # scaled_pixmap = pixmap.scaled(
            #     media_label.size(),
            #     Qt.KeepAspectRatio,
            #     Qt.SmoothTransformation
            # )
            # media_label.setPixmap(scaled_pixmap)
            select_content_widget.set_image(pixmap, file_path=output_path)
        # print(f"Yeni state ayarlandi: {state_manager.get('image_path')}")
        
        print(f"Annotated image saved to {output_path}")

    except Exception as e:
        print(f"Error during inference: {e}")

    
    
def handle_video_detection(video_path, conf, main_window):
    try:
        model = YOLO(MODEL_PATH)
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Failed to open video: {video_path}")
        return

    # Video bilgileri
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # VideoWriter objesi (annotate edilmiş videoyu yazmak için)
    output_path = "output/annotated_result_video.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        print(f"Processing frame {frame_count}")

        # Detection yap
        results = model.predict(source=frame, conf=conf, iou=0.2, save=False)[0]

        boxes = results.boxes.xyxy.cpu().numpy()
        confidences = results.boxes.conf.cpu().numpy()
        class_ids = results.boxes.cls.cpu().numpy().astype(int)
        label_map = results.names

        for box, conf_score, cls_id in zip(boxes, confidences, class_ids):
            x1, y1, x2, y2 = map(int, box)
            label = f"{label_map[cls_id]} {conf_score:.2f}"
            cv2.rectangle(frame, (x1, y1), (x2, y2), color=(0, 255, 0), thickness=2)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        out.write(frame)


    cap.release()
    out.release()
    print(f"Video saved to {output_path}")
    
    # --- VIDEO GUI'DE GÖSTER ---
    select_content_widget = main_window.get_select_content_widget()
    select_content_widget.set_video(output_path)
