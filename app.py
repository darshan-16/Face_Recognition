import io
import re
import cv2
import time
import pafy
import html
import base64
import requests
import numpy as np
import pandas as pd
import mysql.connector
from mtcnn import MTCNN
from deepface import DeepFace
from pathlib import Path
from base64 import b64decode, b64encode
from deepface.basemodels import VGGFace
import streamlit as vAR_st
import streamlit.components.v1 as components
timestr = time.strftime("%Y%m%d-%H%M%S")

#for Setting the page layout to wide
vAR_st.set_page_config(layout="wide")

col1, col2, col3 = vAR_st.columns([3,5,3])
with col2:
  vAR_st.image('https://raw.githubusercontent.com/tarun243/Streamlit-commonToAllIndustry/master/Web_app/Logo_final.png')

#setting font size and colour for the title 
#by this text-align: centre, we can align the title to the centre of the page
vAR_st.markdown("<h1 style='text-align: center; color: black; font-size:29px;'>ENERGY EFFICIENCY AND ENERGY BENCH MARKING </h1>", unsafe_allow_html=True)
vAR_st.markdown("<h1 style='text-align: center; color: blue; font-size:29px;'>Powered by Google Cloud and Streamlit</h1>", unsafe_allow_html=True)

#for clear/reset button
vAR_st.markdown("""<style>#root > div:nth-child(1) > div > div > div > div > section.css-1lcbmhc.e1fqkh3o0 > div.css-17eq0hr.e1fqkh3o1 > div.block-container.css-1gx893w.eknhn3m2 > div:nth-child(1) > div:nth-child(5)  
{
    background-color:rgb(47 236 106);  
    top: 40px; 
    border: 0px solid; 
    padding: 10px;
    border-radius:3px; }
</style>""", unsafe_allow_html=True)


#for clear/reset button
vAR_st.markdown("""<style>p, ol, ul, dl {
    margin: 0px 80px 1rem;
    font-size: 1rem;
    font-weight: 400;
}
</style>""", unsafe_allow_html=True)

vAR_st.markdown("""<style>a {
    text-decoration: none;
}
</style>""", unsafe_allow_html=True)

#To customize the background colour of the submit button  
m = vAR_st.markdown("""
<style>
div.stButton > button:first-child {border: 1px solid; width: 55%;
    background-color: rgb(47 236 106) ;
}
</style>""", unsafe_allow_html=True)

#for horizontal line
vAR_st.markdown("""
<hr style="width:100%;height:3px;background-color:gray;border-width:10">
""", unsafe_allow_html=True)

mod = VGGFace.loadModel()

customers_csv_path = Path('sample_customers.csv').resolve().parents[1]/'face_recognition/Customers/sample_customers.csv'
df = pd.read_csv(customers_csv_path, names=['cid', 'name', 'city', 'phone'])
df = df.astype(str)


def capture_frames_url(url):
    reg = "^((?:https?:\/\/))?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(watch\?(.*&)?v=\/?))([^\?\&\"\'>]+)$"
    if url!='':
        global stop
        if stop:
            t = vAR_st.empty()
            t.text_input('Enter the URL', '')
            return
        if not stop:
            url = str(url)
            vAR_st.write(url)
            if re.match(reg, url):
                x = requests.get(url)
                if("Video unavailable" in x.text):
                    vAR_st.write("Video unavailable")
                vAR_st.write("URL verified")
            else:
                vAR_st.write("URL not valid")
            video = pafy.new(url)
            best  = video.getbest(preftype="mp4")
            cap = cv2.VideoCapture(best.url)
            truncateTable()
            while True:
                ret, frame = cap.read()
                _, buffer = cv2.imencode('.jpg', frame)
                im_bytes = buffer.tobytes()
                encodedJPG = base64.b64encode(im_bytes)
                insertFrame(encodedJPG)
            cap.release()
            cv2.destroyAllWindows()

def process_frames():
    if vAR_process:
        truncateProTable()
        res = readImg()
        for code in res:
            data = base64.b64decode(code[0])
            nparr = np.frombuffer(data, np.uint8)
            nparr.reshape(len(nparr),1)
            img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            frame_process(img_np)

def frame_process(frame):
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    det = MTCNN()
    face = det.detect_faces(img = img)
    race = []
    gender = []
    customer = []
    cid = []
    city = []
    phone = []
    male = 0
    female = 0
    for f in face:
        x, y, width, height = f['box']
        (startX, startY) = x, y
        (endX, endY) = x+width, y+height
        face_crop = np.copy(frame[startY:endY,startX:endX])
        if (face_crop.shape[0]) < 10 or (face_crop.shape[1]) < 10:
            continue
        obj = DeepFace.analyze(np.array(face_crop,dtype=np.uint8), actions = ['gender', 'race'] ,enforce_detection=False)
        gender.append(obj['gender'])
        race.append(obj['dominant_race'])
        df1 = DeepFace.find(np.array(face_crop,dtype=np.uint8), db_path=Path('sample_customers.csv').resolve().parents[1]/'face_recognition/Customers', 
                             model_name='VGG-Face', model=mod, enforce_detection=False)
        if(df1.shape[0]>0):
            name = str(df1.iloc[0].identity)
            name = name.split('/')
            if(name[6] not in customer):
                try:
                    customer.append(name[6])
                    df2 = df.loc[df['name']==name[6]]
                    city.append(df2.iloc[0]['city'])
                    phone.append(df2.iloc[0]['phone'])
                    cid.append(df2.iloc[0]['cid'])
                except:
                    pass
        cv2.rectangle(frame, (x, y), (x+width, y+height), (0,155,255), 2)
        if(gender[-1] == 'Man'):
            male += 1
        else:
            female += 1
    vAR_st.write(str(customer))
    vAR_st.write(str(race))
    vAR_st.image(frame, channels="BGR")
    _, buffer = cv2.imencode('.jpg', frame)
    im_bytes = buffer.tobytes()
    encodedJPG = base64.b64encode(im_bytes)
    insertFrameData(encodedJPG, str(cid), str(customer), str(phone), str(city), str(race), male, female)

def retrieve_video():
    if vAR_retrieve:
        vAR_st.write("Start retrieve")
        row = 1280
        col = 720
        size = (row,col)
        result = cv2.VideoWriter('/content/drive/MyDrive/output/output.avi',cv2.VideoWriter_fourcc(*'MJPG'),10, size)
        res = retrieve_frames()
        for code in res:
            data = base64.b64decode(code[0])
            nparr = np.fromstring(data, np.uint8)
            img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            result.write(img_np)
        result.release()
        print("Saved video")

def insertFrame(photo):
    try:
        connection = mysql.connector.connect(host='66.42.60.177',
                                             database='dssaiai_dssaiai',
                                             user='dssaiai_struct_u',
                                             password='~z=wL1jg~Q4$')

        cursor = connection.cursor()
        sql_insert_frame_query = """ INSERT INTO captured_frames (frame) VALUES (%s) """
        insert_frame = (photo, )
        result = cursor.execute(sql_insert_frame_query, insert_frame)
        connection.commit()
        vAR_st.write("Frame inserted successfully")

    except mysql.connector.Error as error:
        vAR_st.write("Failed inserting frame data into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def truncateTable():
    try:
        connection = mysql.connector.connect(host='66.42.60.177',
                                             database='dssaiai_dssaiai',
                                             user='dssaiai_struct_u',
                                             password='~z=wL1jg~Q4$')

        cursor = connection.cursor()
        truncate_frame_query = """ TRUNCATE captured_frames """
        truncate = cursor.execute(truncate_frame_query)
        connection.commit()
        vAR_st.write("Truncated successfully")

    except mysql.connector.Error as error:
        vAR_st.write("Failed truncate MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def truncateProTable():
    try:
        connection = mysql.connector.connect(host='66.42.60.177',
                                             database='dssaiai_dssaiai',
                                             user='dssaiai_struct_u',
                                             password='~z=wL1jg~Q4$')

        cursor = connection.cursor()
        truncate_frame_query = """ TRUNCATE processed_frames """
        truncate = cursor.execute(truncate_frame_query)
        connection.commit()
        vAR_st.write("Truncated successfully")

    except mysql.connector.Error as error:
        vAR_st.write("Failed truncate MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def readImg():
    vAR_st.write("Reading")
    try:
        connection = mysql.connector.connect(host='66.42.60.177',
                                             database='dssaiai_dssaiai',
                                             user='dssaiai_struct_u',
                                             password='~z=wL1jg~Q4$')
        cursor = connection.cursor()
        sql_fetch_frame_query = """SELECT frame from captured_frames"""
        cursor.execute(sql_fetch_frame_query)
        record = cursor.fetchall()

    except mysql.connector.Error as error:
        vAR_st.write("Failed to read frames from MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            return record

def retrieve_frames():
    vAR_st.write("Reading")
    try:
        connection = mysql.connector.connect(host='66.42.60.177',
                                             database='dssaiai_dssaiai',
                                             user='dssaiai_struct_u',
                                             password='~z=wL1jg~Q4$')
        cursor = connection.cursor()
        sql_fetch_frame_query = """SELECT frame from processed_frames"""
        cursor.execute(sql_fetch_frame_query)
        record = cursor.fetchall()

    except mysql.connector.Error as error:
        vAR_st.write("Failed to read frames from MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            return record

def insertFrameData(photo, cid, name, phone, city, race, male, female):
    try:
        connection = mysql.connector.connect(host='66.42.60.177',
                                             database='dssaiai_dssaiai',
                                             user='dssaiai_struct_u',
                                             password='~z=wL1jg~Q4$')

        cursor = connection.cursor()
        sql_insert_frame_query = """ INSERT INTO processed_frames (frame, cid, name, phone, city, race, male, female) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        insert_frame = (photo, cid, name, city, phone, race, male, female)
        result = cursor.execute(sql_insert_frame_query, insert_frame)
        connection.commit()
        vAR_st.write("Frame inserted successfully")

    except mysql.connector.Error as error:
        vAR_st.write("Failed inserting frame data into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

vAR_data_pipeline=vAR_st.button("Initailize data pipeline and model pipeline")

url = vAR_st.text_input('Enter the URL',key = 2)
if url!='':
    stop = vAR_st.button("Stop")
    capture_frames_url(url)

vAR_process=vAR_st.button("Run Model")
if vAR_process:
    process_frames()

vAR_retrieve=vAR_st.button("Save video in drive")
if vAR_retrieve:
    retrieve_video()