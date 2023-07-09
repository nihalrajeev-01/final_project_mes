from utils.plots import plot_one_box
from PIL import ImageColor
import subprocess
import streamlit as st
import psutil


#import database as db
from datetime import datetime
import spreadsheetData as sprd

import time

import twilioSMS as twil

import logTime

import pygame

from PIL import Image
import numpy as np
import cv2

pygame.mixer.init()
sound = pygame.mixer.Sound("alarm.mp3")


def get_gpu_memory():
    result = subprocess.check_output(
        [
            'nvidia-smi', '--query-gpu=memory.used',
            '--format=csv,nounits,noheader'
        ], encoding='utf-8')
    gpu_memory = [int(x) for x in result.strip().split('\n')]
    return gpu_memory[0]

def color_picker_fn(classname, key):
    color_picke = st.sidebar.color_picker(f'{classname}:', '#ff0003', key=key)
    color_rgb_list = list(ImageColor.getcolor(str(color_picke), "RGB"))
    color = [color_rgb_list[2], color_rgb_list[1], color_rgb_list[0]]
    return color


def get_yolo(img, model_type, model, confidence, color_pick_list, class_list, draw_thick):
    current_no_class = []
    results = model(img)
    if model_type == 'YOLOv7':
        box = results.pandas().xyxy[0]

        for i in box.index:
            xmin, ymin, xmax, ymax, conf, id, class_name = int(box['xmin'][i]), int(box['ymin'][i]), int(box['xmax'][i]), \
                int(box['ymax'][i]), box['confidence'][i], box['class'][i], box['name'][i]
            if conf > confidence:
                plot_one_box([xmin, ymin, xmax, ymax], img, label=class_name,
                                color=color_pick_list[id], line_thickness=draw_thick)
            current_no_class.append([class_name])

    if model_type == 'YOLOv8':
        for result in results:
            bboxs = result.boxes.xyxy
            conf = result.boxes.conf
            cls = result.boxes.cls
            for bbox, cnf, cs in zip(bboxs, conf, cls):
                xmin = int(bbox[0])
                ymin = int(bbox[1])
                xmax = int(bbox[2])
                ymax = int(bbox[3])
                if cnf > confidence:
                    plot_one_box([xmin, ymin, xmax, ymax], img, label=class_list[int(cs)],
                                    color=color_pick_list[int(cs)], line_thickness=draw_thick)
                    current_no_class.append([class_list[int(cs)]])
    return img, current_no_class


def get_system_stat(stframe1, stframe2, fps, df_fq, pic, time_now, time_before, manualMode: bool):
    # Updating Inference results (FPS, Title)
    with stframe1.container():
        st.markdown("<h2>Inference Statistics</h2>", unsafe_allow_html=True)
        if round(fps, 4)>1:
            st.markdown(f"<h4 style='color:green;'>Frame Rate: {round(fps, 4)}</h4>", unsafe_allow_html=True)
        else:
            st.markdown(f"<h4 style='color:red;'>Frame Rate: {round(fps, 4)}</h4>", unsafe_allow_html=True)
    
    #Detected objects table
    with stframe2.container():
        st.markdown("<h3>Detected objects in current Frame</h3>", unsafe_allow_html=True)
        st.dataframe(df_fq, use_container_width=True)
        for ind in df_fq.index:
            # Get the current date and time
            current_datetime = datetime.now()

            # Extract the time components
            current_time = current_datetime.strftime("%H:%M:%S")

            # Extract the date components
            current_date = current_datetime.strftime("%Y-%m-%d")
    
                
            if df_fq['Class'][ind] == 'knife':
                st.markdown(f"<h3 style='color:red;'>Detected a {df_fq['Class'][ind]} 🚨</h3>", unsafe_allow_html=True)
                st.image(pic, use_column_width=True, channels='BGR') 

                if not manualMode:
                    sound.play()
                    # send Twilio msg

                # Check if the time difference since the previous detection is greater than 10 seconds
                if time_now - time_before > 10:
                    sprd.insert_log(f"{df_fq['Class'][ind]}", "Camera 1", current_time, current_date)
                    
                    time_before = time_now  # Update the previous detection time

                    # Update the value of my_variable
                    logTime.time_before = time_before

                    # Save the updated value back to file1.py
                    with open("logTime.py", "w") as file:
                        file.write(f"time_before = {logTime.time_before}")
                        
                
                    
                    image_array = np.array(pic)  # Replace `...` with your actual ndarray representing the image
                    image_array_rgb = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
                    image = Image.fromarray(image_array_rgb)
                    image.save(f"C:/Tahir/Projects/YoloStreamlit/{df_fq['Class'][ind]}{current_date}{time.time()}.jpg")  # Replace with the desired save path and file name

            



    
