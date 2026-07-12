# 🛡️ ErgonoTrack
### Smart Workspace Adaptive Controller

## 📖 Overview

ErgonoTrack is a computer vision-based ergonomic monitoring system developed during the **HackZen 2026 Open Challenge**. The system uses a webcam to monitor the user's sitting posture in real time and provides immediate feedback to encourage healthy workstation habits.

The application detects face position using OpenCV's Haar Cascade classifier. After calibrating a correct sitting posture, ErgonoTrack continuously compares the current face position with the baseline and classifies posture into Optimal, Mild Fatigue, or Critical Slouching.

To improve user awareness, the system provides visual alerts, desktop notifications, voice reminders, brightness adjustment, and a live posture score graph.

---  

## ✨ Features

- 🎥 Real-time webcam monitoring
- 😀 Face detection using OpenCV Haar Cascade
- 🎯 Baseline posture calibration
- 📊 Live ergonomic posture score
- 🟢 Good posture detection
- 🟡 Mild fatigue warning
- 🔴 Critical slouching detection
- 📵 Head-down / face lost detection
- 🔔 Desktop notifications
- 🔊 Voice alerts using Text-to-Speech
- 💡 Automatic screen brightness adjustment
- 📈 Live posture score chart
- 🖥️ Interactive Streamlit dashboard

---

## 🧩 Problem Statement

Students and professionals often spend several hours working on computers without maintaining proper posture. Continuous poor posture can lead to:

- Neck pain
- Back pain
- Shoulder strain
- Eye fatigue
- Reduced productivity

ErgonoTrack provides real-time ergonomic feedback to help users maintain a healthier posture while working.

---

## ⚙️ How It Works

1. Open the Streamlit application.
2. Start ErgonoTrack.
3. Sit in a correct posture.
4. Enable **Lock Good Posture Baseline** to save the ideal posture.
5. Disable calibration.
6. The application continuously monitors posture.

Depending on face movement:

- 🟢 Good posture → Optimal
- 🟡 Slight downward movement → Mild Fatigue
- 🔴 Large downward movement → Critical Slouching
- 📵 Face disappears → Head Drop Alert

---

## 🛠️ Technologies Used

### Programming Language
- Python

### Framework
- Streamlit

### Computer Vision
- OpenCV

### Libraries
- Pandas
- pyttsx3
- plyer
- screen-brightness-control
- threading
- urllib

---

## 📂 Project Structure

```
ErgonoTrack/
│
├── app.py
├── README.md
├── requirements.txt
└── haarcascade_frontalface_default.xml
```

---

## 🚀 Installation

Clone the repository

```bash
git clone https://github.com/KalaiyarasiK6/ErgonoTrack.git
```

Move into the project folder

```bash
cd ErgonoTrack
```

Install the required packages

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

---

## 📊 Alert Levels

| Status | Condition | Action |
|---------|-----------|--------|
| 🟢 Optimal | Correct posture | Full brightness |
| 🟡 Mild Fatigue | Slight slouch | Notification + Voice Alert |
| 🔴 Critical Slouch | Significant slouch | Notification + Voice Alert + Low Brightness |
| 📵 Face Lost | Looking down or face not detected | Head Drop Alert |

---

## 📈 Output

The application displays:

- Live webcam feed
- Current ergonomic health score
- Real-time posture status
- Desktop notifications
- Voice guidance
- Live posture trend graph

---

## 🔮 Future Enhancements

- MediaPipe Pose-based posture detection
- Shoulder and spine angle estimation
- Multi-user support
- Daily posture reports
- Mobile application
- AI-based posture prediction
- Cloud data storage
- Personalized ergonomic recommendations

---

## 👩‍💻 Team

**HackZen 2026 Open Challenge**

- Kalaiyarasi K
- *(Add your teammates here)*

---

## 📄 License

Developed for the HackZen 2026 Open Challenge for educational and demonstration purposes.

---

## 🙏 Acknowledgements

- OpenCV
- Streamlit
- Python Community
- HackZen 2026 Organizers