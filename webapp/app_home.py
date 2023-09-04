import streamlit as st
from PIL import Image

from webapp.app_config import projects, project_stages

# show title
def render():

    with st.sidebar:
        st.markdown("<h1 style='color:tomato;font-size:200%;font-family:verdana'>Home</h1>",
             unsafe_allow_html=True)
        
        st.divider()

        image = Image.open('./img/ai_icon.png')
        st.image(image)

    st.markdown("<h1 style='color:tomato;font-size:400%;font-family:verdana'>CompeersAI</h1>",
             unsafe_allow_html=True)
    st.divider()

    def app_click_button():
        st.session_state['current_page'] = 'prj_home'

    st.markdown("<h1 style='color:tomato;font-size:150%;font-family:verdana'>Select a project</h1>",
             unsafe_allow_html=True)
    option = st.selectbox(
        'Please select a project to continue:',
        (item[0] + ' - ' + item[1] for item in projects.items()),
        placeholder='Select a project ...')
    
    # set project id based on selection
    prj_id = option.split(' - ')[0]
    #st.text(prj_id)
    st.session_state['project_id'] = prj_id

    st.button('Take me to selected project home', on_click=app_click_button)
