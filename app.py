import streamlit as st
import gspread as gs
import pandas as pd
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials

def user_input():
    """Takes input from user"""
    name = st.text_input(label='Name')
    uploaded_files = st.file_uploader(label='Files', accept_multiple_files=True, type=["pdf"])
    note = st.text_input(label='Note')
    
    return name, uploaded_files, note

def google_auth():
    """Connects service account, sheets and drive"""
    SCOPE = ["https://www.googleapis.com/auth/drive"]
    GoogleAuth().credentials = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["service_account"]["sheet_service_account"], SCOPE)
    gc = gs.authorize(GoogleAuth().credentials) # link service account
    
    drive = GoogleDrive(GoogleAuth) # link drive

    sh = gc.open("Printing Datasheet") # link sheets
    ws = sh.worksheet("Data") # get the worksheet
    
    return gc, drive, ws

def run():
    """Runs main app"""
    st.set_page_config(
        page_title="Faidz Printing",
        page_icon="🖨️",
    )
    
    gc, drive, ws = google_auth()
    name, uploaded_files, note = user_input()


run()