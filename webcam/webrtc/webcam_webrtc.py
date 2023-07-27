from streamlit_webrtc import webrtc_streamer
import os
import cv2
from matplotlib import pyplot as plt
from twilio.rest import Client
import streamlit as st
from ultralytics import YOLO
import numpy as np

# for audio
import av
from pydub import AudioSegment
from pydub.playback import play
import threading
import base64
import time
from warning_system.warning_system import warning_state_Algorithm
import queue


def generate_label_colors():
    colors = np.array([
        [0, 255, 0],    # 초록
        [255, 255, 0],  # 노랑
        [255, 255, 0],  # 노랑
        [255, 255, 0],  # 노랑 
        [255, 165, 0],  # 주황
        [255, 165, 0],  # 주황 
        [255, 165, 0],  # 주황 
        [255, 0, 0],    # 빨강
    ])
    return colors


COLORS = generate_label_colors()
WARNING_LEVELS = {
    "1": (1, "right"),
    "2": (1, "left"),
    "3": (1, "center"),
    "4": (2, "right"),
    "5": (2, "left"),
    "6": (2, "center"),
    "7": (3, "center"),
}
result_queue: "queue.Queue[List[Detection]]" = queue.Queue()
frame_queue = queue.Queue()


def create_video_frame_callback():
    frame_count = 0

    def video_frame_callback(frame: av.VideoFrame) -> av.VideoFrame:
        nonlocal frame_count

        frame_count += 1
        image = frame.to_ndarray(format="bgr24")
        preds = model(image)
        h, w = preds[0].orig_shape

        boxes = preds[0].boxes.data
        classes = preds[0].names
        danger = []

        for xmin, ymin, xmax, ymax, score, label in boxes:
            xmin, ymin, xmax, ymax = map(int, [xmin, ymin, xmax, ymax])
            label_name = classes[int(label.item())]
            
            classnum,warning_state = warning_state_Algorithm(xmin, ymin, xmax, ymax, label_name, h, w)
            color = COLORS[warning_state] # 위험 상태에 따른 bbox color 설정
            
            if frame_count % 50 == 0: # 50 frame 마다 danger에 append
                # danger.append(label_name)
                danger.append(
                    (classnum,warning_state)
                )

            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, 2)
            cv2.putText(
                image,
                label_name,
                (xmin, ymin - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                color,
                2,
            )
            
        if frame_count % 50 == 0:
            result_queue.put(danger)
        frame_queue.put(frame_count)

        return av.VideoFrame.from_ndarray(image, format="bgr24")

    return video_frame_callback


def autoplay_audio(file_path: str, playback_rate=1.5):
    audio_place = st.empty()
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls autoplay="true" playbackRate="{playback_rate}">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        audio_place.markdown(
            md,
            unsafe_allow_html=True,
        )
    time.sleep(1.5)
    audio_place.empty()


def webrtc_init():
    global model

    model = YOLO("/app/level3_cv_finalproject-cv-10/weights/yolov8n_jp.pt")
    os.environ["TWILIO_ACCOUNT_SID"] = st.secrets["TWILIO_ACCOUNT_SID"]
    os.environ["TWILIO_AUTH_TOKEN"] = st.secrets["TWILIO_AUTH_TOKEN"]

    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    client = Client(account_sid, auth_token)

    token = client.tokens.create()

    video_frame_cb = create_video_frame_callback()

    ctx = webrtc_streamer(
        rtc_configuration={"iceServers": token.ice_servers},
        media_stream_constraints={"video": True, "audio": False},
        video_frame_callback=video_frame_cb,
        async_processing=True,
        key="apas",
    )

    text_place = st.empty()
    
    mode = "nomal_mode"
    
    while ctx.state.playing:
        
        frame_num = frame_queue.get()
        if frame_num % 50 == 0:  # for every 50 frames
            result = result_queue.get()

            if len(result) != 0:
                result.sort(key=lambda x: x[1], reverse=True)
                
                # 1. 노말 모드였는데 5개이상이 detect -> warning mode
                if len(result) >= 5 and mode == "nomal_mode": 
                    if result[4][1] >= 1:                      # 5개 이상이 위험구역 안에 들어왔을때
                        mode = "warning_mode" 
                        text_place.warning("주변에 탐지되는 물체가 5개 이상입니다!")
                        audio_file_path = f"/app/level3_cv_finalproject-cv-10/warning_system/tts/{mode}.mp3"
                        autoplay_audio(audio_file_path)
                    else:                                      # 5개 이상 detect가 되었으나 위험구역안에 5개 이하
                        danger_class, danger_level = result[0]
                        if danger_level != 0:  # except safe
                            text_place.warning("주의하세요 !")
                            lv, dir = WARNING_LEVELS[str(danger_level)]
                            audio_file_path = f"/app/level3_cv_finalproject-cv-10/warning_system/tts/{danger_class}_{lv}_{dir}.mp3"
                            autoplay_audio(audio_file_path)
                        else:
                            text_place.success("안전합니다 !")
                # 2. 워닝 모드였는데 5개 이하가 detect -> nomal mode         
                elif len(result) < 5 and mode == "warning_mode": 
                        mode = "nomal_mode"
                        text_place.warning("주변에 탐지되는 물체가 5개 이하입니다!")
                        audio_file_path = f"/app/level3_cv_finalproject-cv-10/warning_system/tts/{mode}.mp3"
                        autoplay_audio(audio_file_path)
                        
                # 3. 워닝 모드였는데 5개 이상 detect -> stil 워닝모드
                elif len(result) >= 5 and mode == "warning_mode":
                    danger_class, danger_level = result[0]
                    if danger_level != 0:  # except safe
                        text_place.warning("주의하세요 !")
                        lv, dir = WARNING_LEVELS[str(danger_level)]
                        audio_file_path = f"/app/level3_cv_finalproject-cv-10/warning_system/tts/{danger_class}_{lv}_{dir}.mp3"
                        autoplay_audio(audio_file_path)
                    else:
                        text_place.success("안전합니다 !")
                
                # 4. 노말 모드였는데 5개 이하 detect -> still nomal mode
                elif len(result) < 5 and mode ==  "nomal_mode":
                    danger_class, danger_level = result[0]
                    if danger_level != 0:  # except safe
                        text_place.warning("주의하세요 !")
                        lv, dir = WARNING_LEVELS[str(danger_level)]
                        audio_file_path = f"/app/level3_cv_finalproject-cv-10/warning_system/tts/{danger_class}_{lv}_{dir}.mp3"
                        autoplay_audio(audio_file_path)
                    else:
                        text_place.success("안전합니다 !")
            else:
                text_place.success("안전합니다 !")