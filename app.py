import streamlit as st
import gspread as gs
import pandas as pd
import pypdf
from tempfile import NamedTemporaryFile
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from google.oauth2.service_account import Credentials


def user_input():
    """Takes input from user"""
    name = st.text_input(label='Name')
    uploaded_files = st.file_uploader(label='Files', accept_multiple_files=True, type=["pdf"])
    note = st.text_input(label='Note')
    
    return name, uploaded_files, note


def google_auth():
    """Connects service account, sheets and drive"""
    scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive' ]
    credentials = st.secrets["service_account"]["sheet_service_account"]
    
    #auth for gspread
    gc_spread = gs.service_account_from_dict(credentials)
    
    #auth for pydrive2
    GoogleAuth().credentials = Credentials.from_service_account_info(credentials, scopes=scopes)
    gc = gs.authorize(GoogleAuth().credentials) # link service account
    
    # link drive
    drive = GoogleDrive(GoogleAuth) 
    # link sheets
    sh = gc_spread.open("Printing Datasheet") 
    ws = sh.worksheet("Data")
    
    return gc, drive, ws


def ink_choice(key, pdf_file):
    """Creates a new button"""
    ink_type = st.radio(
    f"{pdf_file.name} :red[\*]",
    ["Colored", "Black & White"],
    index=None,key=key)
    return {'value': ink_type}


def create_temp_file(any_file):
    with NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(any_file.getvalue())
    
    return temp_file


def count_pages(temp_file, pdf_file):
    with open(temp_file.name, 'rb'):
        pdfReader = pypdf.PdfReader(pdf_file)
        pages = len(pdfReader.pages)
    
    return pages


def upload_file_to_gdrive(drive, FOLDER_ID, temp, pdf_file):
    FOLDER_ID = "1qBfLSQVBMJgpbgXa7h6YdAbT3AJv_sCe" #'print' folder
    gfile = drive.CreateFile({"title": pdf_file.name, "parents": [{"id": FOLDER_ID}]})
    gfile.SetContentFile(temp.name)
    gfile.Upload()
    file_link = gfile['alternateLink']

    return file_link

def run():
    """Runs main app"""
    st.set_page_config(
        page_title="Faidz Printing",
        page_icon="🖨️",
    )

    gc, drive, ws = google_auth()

    with st.expander(label='Form', expanded=True):   
        name, uploaded_files, note = user_input() 

        # ink type choice
        st.write('Choose Ink Type:')
        col1, col2, col3 = st.columns(3)
        columns = [col1, col2, col3]
        ink_types = []

        for index, current_file in enumerate(uploaded_files):
            # spread out each radio option to columns
            with columns[(index % 3)]:
                ink = ink_choice(index, current_file)
                ink_types.append(ink)

        if uploaded_files:
            st.write(uploaded_files)
            for current_file in uploaded_files:
                temp_file = create_temp_file(current_file)
                pages = count_pages(temp_file, current_file)


run()