import re
import cv2
import app
import pafy
import requests
import database as vAR_db
import streamlit as vAR_st
from base64 import b64decode, b64encode

def capture_frames_url(url, stop):
    reg = "^((?:https?:\/\/))?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(watch\?(.*&)?v=\/?))([^\?\&\"\'>]+)$"
    if url!='':
        if not stop:
            url = str(url)
            vAR_st.write(url)
            if re.match(reg, url):
                x = requests.get(url)
                if("Video unavailable" in x.text):
                    vAR_st.text("Video unavailable")
                vAR_st.text("URL verified")
            else:
                vAR_st.write("URL not valid")
            video = pafy.new(url)
            best  = video.getbest(preftype="mp4")
            cap = cv2.VideoCapture(best.url)
            vAR_db.truncateTable()
            while True:
                ret, frame = cap.read()
                _, buffer = cv2.imencode('.jpg', frame)
                im_bytes = buffer.tobytes()
                encodedJPG = b64encode(im_bytes)
                vAR_db.insertFrame(encodedJPG)
                if stop:
                    break
            cap.release()
            cv2.destroyAllWindows()