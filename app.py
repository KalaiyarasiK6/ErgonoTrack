import cv2
import streamlit as st
import screen_brightness_control as sbc
import urllib.request
import os
import time
from plyer import notification
import pyttsx3
import threading
import pandas as pd

st.set_page_config(page_title="ErgonoTrack Dashboard", layout="wide")

st.title("🛡️ ErgonoTrack: Workspace Adaptive Controller")

xml_filename = "haarcascade_frontalface_default.xml"
if not os.path.exists(xml_filename):
    url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
    urllib.request.urlretrieve(url, xml_filename)
face_cascade = cv2.CascadeClassifier(xml_filename)

# Thread-safe, non-blocking voice alert
def speak_safely(text):
    def _target():
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 165)
            engine.say(text)
            engine.runAndWait()
            engine.stop()
        except:
            pass
    threading.Thread(target=_target, daemon=True).start()

# Session state initialization
if 'baseline_y' not in st.session_state:
    st.session_state.baseline_y = None
if 'score_history' not in st.session_state:
    st.session_state.score_history = []
if 'last_alert_time' not in st.session_state:
    st.session_state.last_alert_time = 0
if 'run_loop' not in st.session_state:
    st.session_state.run_loop = False
if 'face_lost_frames' not in st.session_state:
    st.session_state.face_lost_frames = 0

col1, col2 = st.columns([2, 1])

with col2:
    st.write("### ⚙️ System Controls")
    
    if st.button("▶️ Start ErgonoTrack", use_container_width=True):
        st.session_state.run_loop = True
        st.session_state.score_history = []
        st.session_state.last_alert_time = 0
        st.session_state.face_lost_frames = 0
        st.rerun()
        
    if st.button("🛑 Stop ErgonoTrack", use_container_width=True):
        st.session_state.run_loop = False
        st.rerun()

    calibrate_mode = st.checkbox("🚀 Lock Good Posture Baseline", value=False)
    
    st.markdown("---")
    st.write("### 📊 Live Analytics")
    status_box = st.empty()
    score_box = st.empty()

with col1:
    st.write("### 📹 Live Vision Feedback")
    frame_window = st.empty()

st.markdown("---")
st.write("### 📉 Real-Time Ergonomic Performance Chart")
chart_placeholder = st.empty()

if st.session_state.run_loop:
    cap = cv2.VideoCapture(0)
    
    while st.session_state.run_loop:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        if not face_cascade.empty():
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            current_time = time.time()
            
            # --- FACE DETECTED NORMALLY ---
            if len(faces) > 0:
                st.session_state.face_lost_frames = 0  # Reset lost frames counter
                (x, y, w, h) = faces[0]
                current_face_y = y + (h // 2)
                
                if calibrate_mode:
                    st.session_state.baseline_y = current_face_y
                    status_box.success("🎯 Baseline Locked! Uncheck the box to start tracking.")
                
                elif st.session_state.baseline_y is not None:
                    deviation = current_face_y - st.session_state.baseline_y
                    posture_score = int(max(0, min(100, 100 - (deviation * 2))))
                    
                    st.session_state.score_history.append(posture_score)
                    if len(st.session_state.score_history) > 40:
                        st.session_state.score_history.pop(0)
                    
                    # 🚨 RED ZONE
                    if deviation > 40:  
                        status_box.error("🚨 ALERT: CRITICAL SLOUCHING DETECTED!")
                        score_box.metric(label="Ergonomic Health Score", value=f"{posture_score}%", delta="Fix your posture now!")
                        
                        if current_time - st.session_state.last_alert_time > 15:
                            notification.notify(title="🚨 ErgonoTrack", message="Fix your posture.", timeout=1)
                            speak_safely("Fix your posture.")
                            st.session_state.last_alert_time = current_time
                        try: sbc.set_brightness(15)
                        except: pass
                            
                    # 🟡 YELLOW ZONE
                    elif deviation > 15:  
                        status_box.warning("😴 ALERT: Shoulders down. Feeling tired?")
                        score_box.metric(label="Ergonomic Health Score", value=f"{posture_score}%", delta="- Mild Fatigue")
                        
                        if current_time - st.session_state.last_alert_time > 15:
                            notification.notify(title="😴 ErgonoTrack", message="Sit up straight.", timeout=1)
                            speak_safely("Sit up straight.")
                            st.session_state.last_alert_time = current_time
                        try: sbc.set_brightness(60)
                        except: pass
                            
                    # 🟢 GREEN ZONE
                    else:
                        status_box.success("✅ Status: OPTIMAL")
                        score_box.metric(label="Ergonomic Health Score", value=f"{posture_score}%", delta="Perfect Alignment")
                        try: sbc.set_brightness(100)
                        except: pass
                    
                    # Live chart render
                    df_chart = pd.DataFrame(st.session_state.score_history, columns=["Posture Score (%)"])
                    chart_placeholder.line_chart(df_chart, height=200)
                
                cv2.rectangle(img_rgb, (x, y), (x+w, y+h), (0, 255, 0), 3)
                cv2.circle(img_rgb, (x + w//2, current_face_y), 5, (255, 0, 0), -1)
            
            # --- FACE LOST (LOOKING DOWN) ---
            else:
                if calibrate_mode:
                    status_box.warning("🔍 Looking for face... Please look at the camera to lock baseline.")
                elif st.session_state.baseline_y is not None:
                    st.session_state.face_lost_frames += 1
                    
                    # If face is lost for more than a few frames, assume severe head drop
                    if st.session_state.face_lost_frames > 5:
                        posture_score = 10  # Plunge score to 10%
                        
                        st.session_state.score_history.append(posture_score)
                        if len(st.session_state.score_history) > 40:
                            st.session_state.score_history.pop(0)
                            
                        status_box.error("📵 ALERT: FACE LOST! Are you looking down?")
                        score_box.metric(label="Ergonomic Health Score", value=f"{posture_score}%", delta="- Severe Head Drop")
                        
                        if current_time - st.session_state.last_alert_time > 15:
                            notification.notify(title="📵 ErgonoTrack", message="Head drop detected. Look up!", timeout=1)
                            speak_safely("Please look up. Fix your posture.")
                            st.session_state.last_alert_time = current_time
                        
                        try: sbc.set_brightness(15)
                        except: pass
                        
                        df_chart = pd.DataFrame(st.session_state.score_history, columns=["Posture Score (%)"])
                        chart_placeholder.line_chart(df_chart, height=200)

        frame_window.image(img_rgb, channels="RGB")
        time.sleep(0.01)
        
    cap.release()
    frame_window.empty()
    chart_placeholder.empty()
else:
    status_box.info("System is offline.")