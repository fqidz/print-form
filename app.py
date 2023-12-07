import streamlit as st

def user_input():
    name = st.text_input(label='Name')
    uploaded_files = st.file_uploader(label='Files', accept_multiple_files=True, type=["pdf"])
    note = st.text_input(label='Note')
    return name, uploaded_files, note

def run():
    st.set_page_config(
        page_title="Faidz Printing",
        page_icon="🖨️",
    )
    
    name, uploaded_files, note = user_input()


run()