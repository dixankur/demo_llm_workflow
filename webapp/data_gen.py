import os
import time
import streamlit as st
import pandas as pd
import subprocess

from webapp.app_config import projects, project_stages, project_feature_list
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
                "Generate dataset.",
                "Preview and Download the generated dataset.",
                "Approve the dataset."
            ])
    
    st.header(':red[Dataset generation and Approval]', divider='rainbow')
    
    def prj_click_button():
        st.session_state['current_page'] = 'prj_home'

    dataset_generated = False
    if st.button('Generate Dataset', key='1'):            
        st.write('Dataset generation in progress ...')

        # Run as main.py
        with open(f"./data/{prj_id}/generate_dataset.py") as f:
            exec(f.read())

        update_status_and_audit(prj_id, "S04", "Inprogress", "Dataset generated")
        # Run the other script
        #subprocess.run(["python", f"./data/{prj_id}/generate_dataset.py"])    

    try:
        creation_time = os.path.getctime(f"./data/{prj_id}/final_dataset.csv")
        # Convert the timestamps to datetime objects
        creation_datetime = time.ctime(creation_time)
        st.markdown(f":green[Data generated at: {creation_datetime}]")
        dataset_generated = True
    except FileNotFoundError:
        st.markdown(":red[Data not generated yet]")
    
    st.divider()
    if dataset_generated:
        # read the generated data
        df = pd.read_csv(f"./data/{prj_id}/final_dataset.csv")
        st.dataframe(df, hide_index=True)

        provide_rating(prj_id, 'dataset_gen')

    
    dataset_exists = os.path.exists(f"./data/{prj_id}/final_dataset.csv")
    if dataset_exists:
        with open(f"./data/{prj_id}/final_dataset.csv", "rb") as docx_file:
            CSVbyte = docx_file.read()
        if CSVbyte:
            if st.download_button(label="Download Dataset", key='2',
                    data=CSVbyte,
                    file_name=f"./data/{prj_id}/final_dataset.csv",
                    mime='application/octet-stream'):
                st.markdown(f":green[Dataset Downloaded!!]")
        else:
            st.markdown(f":red[Dataset not generated yet!!]")
    
    st.divider()

    st.markdown("<h2 style='color:tomato;font-size:150%;font-family:verdana'>Approve Generated Dataset</h2>",
             unsafe_allow_html=True)
    apv_time = provide_appoval(prj_id, 'dataset_approval', 'Approve Generated Dataset')
    if apv_time:
        update_status_and_audit(prj_id, "S04", "Complete", "Dataset approved")
   
    st.divider()
    
    st.button('Back to Project Home', on_click=prj_click_button)

    #chat_window(prj_id, 'S04')
