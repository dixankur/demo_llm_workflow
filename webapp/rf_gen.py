import os
import time
import streamlit as st
from webapp.app_config import projects, project_stages, project_feature_list
import pandas as pd

from ai_model.generate_random_forest import generate_code
from webapp.utils import provide_rating, chat_window, provide_appoval, add_sidebar, update_status_and_audit


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
                "Generate Random forest model code.",
                "Preview and Download the generated code.",
                "Upload edited final version of code."
            ])
    
    st.header(':red[Random Forest model code Generation]', divider='rainbow')
    
    def prj_click_button():
        st.session_state['current_page'] = 'prj_home'

    if st.button('Generate Code for Random forest model', key='1'):            
        st.write('Code generation in progress ...')
        generate_code(prj_id)
        update_status_and_audit(prj_id, "S05", "Inprogress", "Code generated")

    code_generated = False

    try:
        creation_time = os.path.getctime(f"./data/{prj_id}/random_forest.py")
        # Convert the timestamps to datetime objects
        creation_datetime = time.ctime(creation_time)
        st.markdown(f":green[Code generated at: {creation_datetime}]")
        code_generated = True
    except FileNotFoundError:
        st.markdown(":red[Code not generated yet]")
    
    st.divider()
    if code_generated:
        # read the generated code
        with open (f"./data/{prj_id}/random_forest.py", "r") as f:
            code = f.read()
        st.code(code, language='python')

        provide_rating(prj_id, 'random_forest_code')


    side1, side2 = st.columns(2)
    with side1:
        code_file_exists = os.path.exists(f"./data/{prj_id}/random_forest.py")
        if code_file_exists:
            with open(f"./data/{prj_id}/random_forest.py", "rb") as docx_file:
                Pybyte = docx_file.read()
            if Pybyte:
                if st.download_button(label="Download Code", key='2',
                        data=Pybyte,
                        file_name=f"./data/{prj_id}/random_forest.py",
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
                with open(f"./data/{prj_id}/random_forest.py", "wb") as f: 
                    f.write(uploaded_file.getbuffer())
                st.success("Code file upload done!!")
    
    st.divider()

    st.markdown("<h2 style='color:tomato;font-size:150%;font-family:verdana'>Approve Random Forest Code</h2>",
             unsafe_allow_html=True)
    apv_time = provide_appoval(prj_id, 'rf_code_approval', 'Approve Random Forest Code')
    if apv_time:
        update_status_and_audit(prj_id, "S05", "Complete", "Code approved")

    st.divider()

    st.button('Back to Project Home', on_click=prj_click_button)

    #chat_window(prj_id, 'S05')

