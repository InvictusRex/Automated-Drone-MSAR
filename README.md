# Autonomous Drone-Based Real-Time Maritime Search and Rescue Using Onboard CV and Precision Payload Deployment

This project implements an autonomous UAV-based system for real-time maritime Search and Rescue (SAR) operations using onboard computer vision models. The system is capable of responding to emergency alerts, autonomously navigating to GPS-tagged distress locations, performing aerial object detection to locate victims (specifically swimmers), and initiating a precision payload drop (life buoy), all while running on edge-compatible hardware.
The core innovation lies in deploying highly efficient object detection models (YOLOv8n and YOLOv11n) optimized for inference on constrained platforms such as drones. These models were trained and evaluated on a curated and augmented version of the SeaDronesSee dataset. The detection pipeline is supported by GPS, IMU-based navigation, and temporal tracking for spatial confirmation, forming a closed-loop UAV SAR system.

---

### ⚙️ System Architecture

1. **Emergency Trigger Interface**  
   Initiated via sensors or human observers, triggering automatic UAV deployment.

2. **Autonomous UAV Dispatch**  
   - Real-time GPS-based navigation
   - Dynamic waypoint generation and obstacle avoidance
   - Altitude control for optimal detection (200–250m AGL)

3. **Onboard Visual Detection**  
   - Frame-wise detection (30 FPS) using YOLOv8n/YOLOv11n
   - Real-time bounding box localization of swimmers
   - Temporal confirmation to mitigate false positives

4. **Geospatial Localization and Tracking**  
   - Bounding box centroids geo-projected using GPS and camera intrinsics
   - Track confirmed targets to adjust for drift/movement

5. **Precision Payload Drop (Simulated)**  
   - On centroid lock, drone hovers and prepares for drop
   - Logic framework for trajectory estimation and actuation

---

## 🧪 Model Evaluation and Training

### Dataset

- **Source**: Roboflow-enhanced SeaDronesSee v10
- **Images**: 10,474 (Train: 7,322 | Val: 2,077 | Test: 1,075)
- **Classes**: `swimmer`, `boat`, `buoy`, `jetski`, `life_saving_appliances`
- **Augmentations**: Cutout + auto-orientation
- **Annotations**: Reformatted with class merging and distribution balancing

### Model Configurations

| Variant | Architecture | GFLOPs | Deployment Suitability |
|---------|--------------|--------|-------------------------|
| YOLOv8n | CSPDarknet53 (C2f, PAN-FPN) | 8.1    | Edge devices (preferred) |
| YOLOv11n| Optimized PANet+Backbone     | 6.3    | Ultra low-power devices  |

- **Epochs**: 100  
- **Optimizer**: AdamW (momentum: 0.9)  
- **Learning Rate**: 0.000714  
- **IoU Threshold**: 0.7  
- **Augmented P2 Layer**: Added for small object detection

---


## 📊 Evaluation Metrics

| Model      | GFLOPs | Precision | Recall | mAP@50 | mAP@50-95 | F1 Score | Accuracy |
|------------|--------|-----------|--------|--------|-----------|----------|----------|
| YOLOv8n    | 8.1    | 0.784     | 0.712  | 0.719  | 0.367     | 0.746    | 0.553    |
| YOLOv8s    | 28.4   | 0.782     | 0.693  | 0.727  | 0.458     | 0.734    | 0.489    |
| YOLOv8m    | 78.7   | 0.841     | 0.737  | 0.759  | 0.468     | 0.836    | 0.613    |
| YOLOv11n   | 6.3    | 0.770     | 0.714  | 0.718  | 0.364     | 0.742    | 0.558    |
| YOLOv11s   | 21.3   | 0.852     | 0.699  | 0.761  | 0.466     | 0.768    | 0.588    |
| YOLOv11m   | 67.7   | 0.867     | 0.735  | 0.769  | 0.466     | 0.787    | 0.590    |

- **YOLOv8n** is selected as the final deployment model due to its strong trade-off between detection performance and low computational overhead.
- **YOLOv11n**, while more efficient (6.3 GFLOPs), lags slightly in F1 and mAP metrics.

---

## 📈 Detailed Results

### Per-Class Detection (YOLOv8n vs YOLOv11n)

| Class                   | Precision (v8n) | Recall (v8n) | mAP@50 (v8n) | Precision (v11n) | Recall (v11n) | mAP@50 (v11n) |
|------------------------|----------------|--------------|--------------|------------------|----------------|---------------|
| Swimmer                | 0.727          | 0.698        | 0.696        | 0.712            | 0.707          | 0.697         |
| Boat                   | 0.911          | 0.939        | 0.944        | 0.906            | 0.930          | 0.953         |
| Buoy                   | 0.871          | 0.817        | 0.806        | 0.862            | 0.794          | 0.790         |
| Jetski                 | 0.857          | 0.902        | 0.925        | 0.816            | 0.856          | 0.908         |
| Life Saving Appliance  | 1.000          | 0.000        | 0.115        | 1.000            | 0.000          | 0.105         |


### Observations

- Swimmer class performance is critical for SAR — YOLOv8n marginally outperforms YOLOv11n in F1.
- Boats and Jetskis are detected with high confidence due to their large, distinct shapes.
- Life-saving appliances perform poorly due to small object size, occlusion, and underrepresentation in training data.

### Visual Examples

Included in the repository are inference outputs (bounding boxes on video frames) from both:
- **Synthetic test data**
- **Real-world maritime scenarios** (e.g., open sea, coastal crowds)

### Model Selection Criteria

- **YOLOv8n** is preferred for Raspberry Pi, Jetson Nano, or Xavier NX deployments.
- **YOLOv11s** may be considered if additional compute power is available (higher mAP, 21.3 GFLOPs).

---

## 🧾 Research Outcomes

- Demonstrated the feasibility of real-time, on-drone detection of swimmers with minimal latency.
- Validated YOLOv8n’s superior F1 score, mAP, and inference accuracy for SAR use-cases.
- Established a conceptual but executable drone response pipeline using onboard edge AI and GPS-guided payload logic.

---

## ⚠️ Limitations

- Conceptual framework; physical payload release system not integrated in this study.
- Detection suffers in extreme conditions (e.g., low visibility, occlusion).
- Limited generalization due to dataset distribution biases (e.g., swimmer poses, lighting).

---

## 💡 Future Work

- Real-world field testing with live drones and mechanical payload systems.
- Dataset enhancement with synthetic overlays, night vision, and thermal imagery.
- Low-power optimization of YOLOv11 via pruning and quantization for edge deployments.
- Energy profiling on Jetson/RPi devices to ensure sustainable UAV operation.

---
