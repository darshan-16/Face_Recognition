import cv2
import app
import numpy as np
from mtcnn import MTCNN
import database as vAR_db
import streamlit as vAR_st
from deepface import DeepFace
from deepface.basemodels import VGGFace
from base64 import b64decode, b64encode

mod = VGGFace.loadModel()

def process_frames(vAR_process):
    if vAR_process:
        vAR_db.truncateProTable()
        res = vAR_db.readImg()
        for code in res:
            data = b64decode(code[0])
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
        df1 = DeepFace.find(np.array(face_crop,dtype=np.uint8), db_path='/content/drive/MyDrive/face',
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
    vAR_st.text(str(customer))
    vAR_st.text(str(race))
    vAR_st.image(frame, channels="BGR")
    _, buffer = cv2.imencode('.jpg', frame)
    im_bytes = buffer.tobytes()
    encodedJPG = b64encode(im_bytes)
    vAR_db.insertFrameData(encodedJPG, str(cid), str(customer), str(phone), str(city), str(race), male, female)