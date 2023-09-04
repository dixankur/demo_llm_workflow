import base64
import time
import os
import streamlit as st
from streamlit_star_rating import st_star_rating

from webapp.app_config import projects, project_stages, project_stage_status
from ai_model.use_ai import generate_use_case
from webapp.utils import provide_rating, chat_window, provide_appoval, add_sidebar, update_status_and_audit


def show_pdf(file_path):
    with open(file_path,"rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def prj_click_button():
        st.session_state['current_page'] = 'prj_home'

def render():

    prj_id = st.session_state['project_id']

    if prj_id in projects:
        prj_name = projects[prj_id]
    else:
        prj_name = 'Unknown Project'
    
    st.header(':red[Use Case Document Generation]', divider='rainbow')

    # sidebar
    add_sidebar(header='CompeersAI', prj_name=prj_name, 
            notes=[
                "Upload a transcript to generate a Use case document from it.",
                "You can check and approve the use case document."
            ])

    st.markdown("<h2 style='color:tomato;font-size:150%;font-family:verdana'>Upload a transcript</h2>",
             unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose a transcript file to upload", type=['pdf'])
    if uploaded_file is not None:
        # To read file as bytes:
        #bytes_data = uploaded_file.getvalue()
        with open(f"./data/{prj_id}/transcript.pdf", "wb") as f: 
            f.write(uploaded_file.getbuffer())
        
        update_status_and_audit(prj_id, "S01", "Inprogress", "Transcript file uploaded")
        st.success("Saved File")

    transcript_uploaded = False

    try:
        creation_time = os.path.getctime(f"./data/{prj_id}/transcript.pdf")
        # Convert the timestamps to datetime objects
        creation_datetime = time.ctime(creation_time)
        st.markdown(f":green[Transcript upload at: {creation_datetime}]")
        transcript_uploaded = True
    except FileNotFoundError:
        st.markdown(":red[No transcript uploaded yet]")

    if transcript_uploaded:
        col1, col2, col3= st.columns(3)
        with col1:  
            if st.button('Read Transcript',key='1'):            
                show_pdf(f'./data/{prj_id}/transcript.pdf')
        with col2:
            st.button('Close Transcript',key='2')                   
        with col3:
            with open(f"./data/{prj_id}/transcript.pdf", "rb") as pdf_file:
                PDFbyte = pdf_file.read()
            st.download_button(label="Download Transcript PDF", key='3',
                    data=PDFbyte,
                    file_name="transcript.pdf",
                    mime='application/octet-stream')

        st.divider()
        st.markdown("<h2 style='color:tomato;font-size:150%;font-family:verdana'>Generate Use Case document</h2>",
             unsafe_allow_html=True)
        
        use_case_doc_exists = os.path.exists(f"./data/{prj_id}/use_case_document.docx")
        coll1, coll2, coll3= st.columns(3)
        with coll1:
            if st.button('Generate Use Case',key='4'):
                generate_use_case(prj_id)
                update_status_and_audit(prj_id, "S01", "Inprogress", "Use Case document generated")
                st.success('Use Case Document generated', icon="✅")

        with coll2:
            if use_case_doc_exists:
                with open(f"./data/{prj_id}/use_case_document.docx", "rb") as docx_file:
                    DOCXbyte = docx_file.read()
                if DOCXbyte:
                    if st.download_button(label="Download Document", key='5',
                            data=DOCXbyte,
                            file_name=f"./data/{prj_id}/use_case_document.docx",
                            mime='application/octet-stream'):
                        st.markdown(f":green[Use Case Document Downloaded!!]")

        with coll3:
            button_click = st.button('Upload Use Case Document', type='secondary', use_container_width=True)
            if button_click:
                uploaded_file = st.file_uploader("Choose Use Case Document to upload", type=['docx'])
                if uploaded_file is not None:
                    # To read file as bytes:
                    #bytes_data = uploaded_file.getvalue()
                    with open(f"./data/{prj_id}/use_case_document.docx", "wb") as f: 
                        f.write(uploaded_file.getbuffer())
                    st.success("Saved File")

        if not use_case_doc_exists:
            st.markdown(f":red[Use Case Document not generated yet!!]")
        else:
            use_case_doc_creation_time = os.path.getctime(f"./data/{prj_id}/use_case_document.docx")  
            # Convert the timestamps to datetime objects
            creation_datetime = time.ctime(use_case_doc_creation_time)
            st.markdown(f":green[Use Case Document generated at: {creation_datetime}]")

    provide_rating(prj_id, 'use_case_doc')

    st.divider()
    st.markdown("<h2 style='color:tomato;font-size:150%;font-family:verdana'>Approve Use Case Document</h2>",
             unsafe_allow_html=True)
    apv_time = provide_appoval(prj_id, 'usecase_doc_approval', 'Approve Use Case document')
    if apv_time:
        update_status_and_audit(prj_id, "S01", "Complete", "Use Case Document approved")
    st.divider()
    st.button('Back to Project Home', on_click=prj_click_button)

    #chat_window(prj_id, 'S01')
