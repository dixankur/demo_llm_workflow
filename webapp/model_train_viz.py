import os
import time
import streamlit as st
from webapp.app_config import projects, project_stages, project_feature_list
import pandas as pd

from ai_model.generate_random_forest import generate_code
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
                "Train the generated Random forest model code.",
                "Preview the suggested visualizations."
            ])
    
    st.header(':red[Random Forest model training & Visualization]', divider='rainbow')
    
    def prj_click_button():
        st.session_state['current_page'] = 'prj_home'

    prediction_generated = False
    if st.button('Generate Predictions', key='4'):            
        st.write('Prediction generation in progress ...')

        # Run as main.py
        with open(f"./data/{prj_id}/random_forest.py") as f:
            exec(f.read())

        update_status_and_audit(prj_id, "S06", "Inprogress", "Prediction generated")
        # Run the other script
        #subprocess.run(["python", f"./data/{prj_id}/generate_dataset.py"])    

    try:
        creation_time = os.path.getctime(f"./data/{prj_id}/final_predictions.csv")
        # Convert the timestamps to datetime objects
        creation_datetime = time.ctime(creation_time)
        st.markdown(f":green[Prediction generated at: {creation_datetime}]")
        dataset_generated = True
    except FileNotFoundError:
        st.markdown(":red[Prediction not generated yet]")
    
    st.divider()

    st.markdown("<h2 style='color:tomato;font-size:150%;font-family:verdana'>Approve Model training & Suggested Visualizations</h2>",
             unsafe_allow_html=True)
    apv_time = provide_appoval(prj_id, 'rf_train_viz_approval', 'Approve Model training & Suggested Visualizations')
    if apv_time:
        update_status_and_audit(prj_id, "S06", "Complete", "Model predictions & Visualizations approved")
    st.divider()

    st.button('Back to Project Home', on_click=prj_click_button)

