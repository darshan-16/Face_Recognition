import html
import process_frames as vAR_pf
import capture_frames_url as vAR_cfu
import pandas as pd
import streamlit as vAR_st
import streamlit.components.v1 as components

if __name__ == '__main__':
    vAR_st.set_page_config(layout="wide")
    col1, col2, col3 = vAR_st.columns([3,5,3])
    with col2:
        vAR_st.image('https://raw.githubusercontent.com/tarun243/Streamlit-commonToAllIndustry/master/Web_app/Logo_final.png')

    vAR_st.markdown("<h1 style='text-align: center; color: black; font-size:29px;'>ENERGY EFFICIENCY AND ENERGY BENCH MARKING </h1>", unsafe_allow_html=True)

    vAR_st.markdown("<h1 style='text-align: center; color: blue; font-size:29px;'>Powered by Google Cloud and Streamlit</h1>", unsafe_allow_html=True)

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

    customers_csv_path = '/content/drive/MyDrive/face/Customers/sample_customers.csv'
    df = pd.read_csv(customers_csv_path, names=['cid', 'name', 'city', 'phone'])
    df = df.astype(str)

    if 'f' not in vAR_st.session_state:
        vAR_st.session_state.f = False
    url = vAR_st.text_input('Enter the URL')
    stop = vAR_st.button("Stop")
    if (url!='') and (not vAR_st.session_state.f):
        vAR_cfu.capture_frames_url(url, stop)
    if stop:
        vAR_st.session_state.f = True

    vAR_process=vAR_st.button("Run Model")
    if vAR_process:
        vAR_pf.process_frames(vAR_process)
        vAR_st.session_state.f = False