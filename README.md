# 🚁 Autonomous Security Drone with FPGA Integration

> **A real-time surveillance system combining Computer Vision, Drone technology, and Hardware interfacing (FPGA & Arduino).**

## 📖 Overview
In light of the escalating security challenges in our environment, this project was conceived to provide a technological solution for real-time threat detection. 

We developed an autonomous system using a **DJI Tello Drone** to scan areas and identify potential security threats using **Face Recognition**. The system integrates software (Python) with hardware (Arduino & FPGA) to display alerts and suspect identity on a dedicated hardware screen, while simultaneously tracking the drone's distance from the base station.

## 🛠️ Tech Stack & Hardware
* **Software:** Python, OpenCV, `face_recognition`, `djitellopy`.
* **Hardware Control:** VHDL (for FPGA), C++ (for Arduino).
* **Components:**
    * 🚁 **Drone:** DJI Tello (Wi-Fi connected).
    * 🧠 **Microcontroller:** Seeeduino Lotus (USB connected).
    * ⚡ **FPGA:** Altera DE2 (GPIO connected to Seeeduino).
    * 📡 **Sensors:** TOF (Time of Flight) Distance Sensor.

## ⚙️ System Architecture
The project bridges the gap between high-level software and low-level hardware logic:

1.  **Surveillance:** The Tello drone streams video via Wi-Fi to the PC.
2.  **Processing:** A Python script processes the feed frame-by-frame:
    * Detects faces.
    * Compares them against a pre-loaded database of "suspects".
3.  **Communication:**
    * If a match is found, the PC sends a signal via **USB** to the **Seeeduino**.
    * The Seeeduino relays the signal via **GPIO** to the **Altera FPGA**.
4.  **Hardware Display:**
    * The FPGA (programmed in **VHDL**) receives the signal and renders the specific suspect's image and name on the connected LCD screen in real-time.
    * If the face is unknown, it displays "NO RISK".
5.  **Telemetry:** A **TOF sensor** measures the drone's distance from the operator, displaying a live graph on the PC dashboard to estimate response time.

## 🚀 Key Features
* **Real-Time Face Recognition:** Identifies known suspects instantly from the live video feed.
* **Visual Feedback:** Draws a bounding box and label around the subject on the computer screen.
* **Hardware Alert System:** Changes the FPGA display dynamically based on the identified person.
* **Distance Tracking:** Live graphical monitoring of the drone's proximity to the control center.

## 📸 Demo
https://youtu.be/iXTirhR4eHo?si=bqFUp26u5LY3DYZ-

---
*Developed by Yarin Gaida & Noam Atia as a final engineering project.*