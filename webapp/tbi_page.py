import base64
import time
import os
import streamlit as st
from streamlit_star_rating import st_star_rating

from webapp.app_config import projects, project_stages, project_stage_status
from ai_model.use_ai import generate_use_case
from webapp.utils import provide_rating, chat_window, provide_appoval, add_sidebar

def prj_click_button():
    st.session_state['current_page'] = 'prj_home'

def render():

    prj_id = st.session_state['project_id']

    if prj_id in projects:
        prj_name = projects[prj_id]
    else:
        prj_name = 'Unknown Project'
    
    st.header(':red[To be implemented]', divider='rainbow')

    # sidebar
    add_sidebar(header='CompeersAI', prj_name=prj_name, 
            notes=[
                "To be implemented.",
            ])

    st.markdown("<h2 style='color:tomato;font-size:150%;font-family:verdana'>To be implemented</h2>",
             unsafe_allow_html=True)
    
    st.divider()
    st.button('Back to Project Home', on_click=prj_click_button)

