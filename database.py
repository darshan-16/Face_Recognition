import mysql.connector
import streamlit as vAR_st

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
        vAR_st.text("Frame inserted successfully")

    except mysql.connector.Error as error:
        vAR_st.text("Failed inserting frame data into MySQL table {}".format(error))

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
        vAR_st.text("Truncated successfully")

    except mysql.connector.Error as error:
        vAR_st.text("Failed truncate MySQL table {}".format(error))

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
        vAR_st.text("Truncated successfully")

    except mysql.connector.Error as error:
        vAR_st.text("Failed truncate MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def readImg():
    vAR_st.text("Reading")
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
        vAR_st.text("Failed to read frames from MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            return record

def retrieve_frames():
    vAR_st.text("Reading")
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
        vAR_st.text("Failed to read frames from MySQL table {}".format(error))

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
        vAR_st.text("Frame inserted successfully")

    except mysql.connector.Error as error:
        vAR_st.text("Failed inserting frame data into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()