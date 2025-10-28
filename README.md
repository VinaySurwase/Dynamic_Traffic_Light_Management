# 🚦 Adaptive Traffic Signal Timer  

> A real-time adaptive traffic control system that utilizes YOLO-based vehicle detection to dynamically adjust signal durations according to traffic density, improving flow efficiency and reducing congestion.

---

## 🧠 Overview  

This system intelligently manages traffic at intersections by analyzing live camera feeds to estimate vehicle density and adjust green signal durations dynamically.  
It replaces static timers with an adaptive model that reacts to real-world traffic conditions, ensuring optimal utilization of road capacity and smoother transit.

---

## ⚙️ System Architecture  

The project is divided into three primary modules:

### 1️⃣ Vehicle Detection Module  
- Detects and classifies vehicles in real-time using **YOLO object detection**.  
- Supports multiple vehicle types — **car, bike, bus, truck, rickshaw**, etc.  
- Outputs structured vehicle count data for further processing.  

### 2️⃣ Signal Switching Algorithm  
- Determines the duration of red, yellow, and green signals based on:  
  - Real-time vehicle counts per lane  
  - Lane configuration and width  
  - Average vehicle speed per class  
- Dynamically updates signal timers to prioritize high-density directions.  

### 3️⃣ Simulation Module  
- Built using **Pygame** to visually simulate vehicle movement and signal behavior.  
- Demonstrates adaptive timing effects at a four-way intersection.  

---

## 🧩 Working Flow  

1. Capture a live traffic image from the intersection camera.  
2. Detect and classify vehicles using the YOLO model.  
3. Calculate the vehicle density for each lane.  
4. Feed the counts into the adaptive signal algorithm.  
5. Compute new green signal durations.  
6. Visualize results through the custom simulation environment.  

---

## 🧰 Prerequisites  

- Python 3.7+  
- Microsoft Visual C++ Build Tools *(for Windows users)*  

---

## 🚀 Installation & Setup  

### Step 1: Clone the Repository  
```bash
git clone https://github.com/VinaySurwase/Dynamic_Traffic_Light_Management
```
### Step 2: Install Dependencies  
```bash
pip install -r requirements.txt
python setup.py build_ext --inplace
```

### Step 4: Run the Modules  
**For Vehicle Detection:**  
```bash
python vehicle_detection.py
```
**For Simulation:**  
```bash
python simulation.py
```

---

## 🧱 Tech Stack  

- **Python 3.7+**  
- **YOLO Object Detection (Darkflow)**  
- **OpenCV** – image processing  
- **NumPy & Pandas** – data computation  
- **Pygame** – traffic simulation visualization  

---

## 📊 Results  

✅ Real-time vehicle detection and classification  
✅ Adaptive timing adjustment per traffic density  
✅ Visual simulation for analysis and demonstration  
✅ Improved throughput and reduced idle time  


