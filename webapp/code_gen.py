import os
import time
import streamlit as st
import pandas as pd

from ai_model.generate_dataset_code import generate_code
from webapp.app_config import projects
from webapp.utils import provide_rating, chat_window, add_sidebar, provide_appoval, update_status_and_audit

# show title
def render():
    prj_id = st.session_state['project_id']

    if prj_id in projects:
        prj_name = projects[prj_id]
    else:
        prj_name = 'Unknown Project'

    # sidebar
    add_sidebar(header='CompeersAI', prj_name=prj_name, 
            notes=[
                "Generate code to prepare dataset.",
                "Preview and Download the generated code.",
                "Upload edited final version of code."
            ])

    
    st.header(':red[Code generation for Dataset creation]', divider='rainbow')
    
    def prj_click_button():
        st.session_state['current_page'] = 'prj_home'

    if st.button('Generate Code for dataset creation', key='1'):            
        st.write('Code generation in progress ...')
        generate_code(prj_id)
        update_status_and_audit(prj_id, "S03", "Inprogress", "Code generated")

    code_generated = False

    try:
        creation_time = os.path.getctime(f"./data/{prj_id}/generate_dataset.py")
        # Convert the timestamps to datetime objects
        creation_datetime = time.ctime(creation_time)
        st.markdown(f":green[Code generated at: {creation_datetime}]")
        code_generated = True
    except FileNotFoundError:
        st.markdown(":red[Code not generated yet]")
    
    if code_generated:
        # read the generated code
        with open (f"./data/{prj_id}/generate_dataset.py", "r") as f:
            code = f.read()
        st.code(code, language='python')

        provide_rating(prj_id, 'dataset_code_gen')

    side1, side2 = st.columns(2)
    with side1:
        code_file_exists = os.path.exists(f"./data/{prj_id}/generate_dataset.py")
        if code_file_exists:
            with open(f"./data/{prj_id}/generate_dataset.py", "rb") as docx_file:
                Pybyte = docx_file.read()
            if Pybyte:
                if st.download_button(label="Download Code", key='2',
                        data=Pybyte,
                        file_name=f"./data/{prj_id}/generate_dataset.py",
                        mime='application/octet-stream'):
                    st.markdown(f":green[Code Downloaded!!]")
            else:
                st.markdown(f":red[Code not generated yet!!]")
    
    with side2:
        button_click = st.button('Upload Python Script', type='secondary', use_container_width=True)
        if button_click:
            uploaded_file = st.file_uploader("Choose a Python script to upload", type=['py'])
            if uploaded_file is not None:
                # To read file as bytes:
                with open(f"./data/{prj_id}/generate_dataset.py", "wb") as f: 
                    f.write(uploaded_file.getbuffer())
                st.success("Code file upload done!!")

    st.divider()
    st.markdown("<h2 style='color:tomato;font-size:150%;font-family:verdana'>Approve Dataset Generation Code</h2>",
             unsafe_allow_html=True)
    apv_time = provide_appoval(prj_id, 'datagen_code_approval', 'Approve Dataset Generation Code')
    if apv_time:
        update_status_and_audit(prj_id, "S03", "Complete", "Code approved")
    st.divider()

    st.button('Back to Project Home', on_click=prj_click_button)

    #chat_window(prj_id, 'S03')
