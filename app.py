import streamlit as st
from webapp import app_home, project_home, feature_list, use_case, code_gen, data_gen 
from webapp import rf_gen, tbi_page, ask_me_anything, model_train_viz
from webapp.app_config import update_data

update_data()

# Initialization
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'app_home'
if 'project_id' not in st.session_state:
    st.session_state['project_id'] = ''

# select a page to render
if st.session_state['current_page'] == 'app_home':
    app_home.render()

if st.session_state['current_page'] == 'prj_home':
    project_home.render()

if st.session_state['current_page'] == 'usecase_home':
    use_case.render()

if st.session_state['current_page'] == 'feature_home':
    feature_list.render()

if st.session_state['current_page'] == 'code_gen':
    code_gen.render()
    
if st.session_state['current_page'] == 'data_gen':
    data_gen.render()

if st.session_state['current_page'] == 'rf_gen':
    rf_gen.render()

if st.session_state['current_page'] == 'train_viz':
    model_train_viz.render()

if st.session_state['current_page'] == 'amy_chat':
    ask_me_anything.render()

if st.session_state['current_page'] == 'tbi':
    tbi_page.render()
