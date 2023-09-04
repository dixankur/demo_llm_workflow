import streamlit as st
from streamlit_star_rating import st_star_rating

from webapp.app_config import projects
from webapp.utils import add_sidebar, chat_window


def render():

    prj_id = st.session_state['project_id']

    if prj_id in projects:
        prj_name = projects[prj_id]
    else:
        prj_name = 'Unknown Project'
    
    st.header(':red[Ask me anything]', divider='rainbow')

    # sidebar
    add_sidebar(header='CompeersAI', prj_name=prj_name, 
            notes=[
                "Ask me anything related to the project",
            ])

    chat_window(prj_id, 'S00')

