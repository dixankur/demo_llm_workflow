import streamlit as st
import streamlit.components.v1 as components
from webapp.app_config import projects, project_stages, project_stage_status
from webapp.utils import ChangeButtonColour, add_sidebar, load_json

color_map = {
    'button-green': '#85e085',
    'button-yellow': '#ffff00',
    'button-grey': '#a6a6a6'
}

def render():
    #project_stages = load_json('./datamodel/project_stages.json')

    prj_id = st.session_state['project_id']

    if prj_id in projects:
        prj_name = projects[prj_id]
    else:
        prj_name = 'Unknown Project'

    # sidebar
    add_sidebar(header='CompeersAI', prj_name=prj_name, 
            notes=[
                "Select a workflow stage to know more about it."
            ])
    
    # show title
    st.header(':blue[Workflow Stages]', divider='rainbow')

    def prj_click_button():
        st.session_state['current_page'] = 'app_home'

    def S01_click_button():
        st.session_state['current_page'] = 'usecase_home'

    def S02_click_button():
        st.session_state['current_page'] = 'feature_home'

    def S03_click_button():
        st.session_state['current_page'] = 'code_gen'

    def S04_click_button():
        st.session_state['current_page'] = 'data_gen'

    def S05_click_button():
        st.session_state['current_page'] = 'rf_gen'

    def S06_click_button():
        st.session_state['current_page'] = 'train_viz'

    def S07_click_button():
        st.session_state['current_page'] = 'tbi'

    def S08_click_button():
        st.session_state['current_page'] = 'tbi'

    def S09_click_button():
        st.session_state['current_page'] = 'tbi'

    for stages in project_stages:
        col1, col2, col3 = st.columns([1, 5, 7])
        with col1:
            if prj_id in project_stage_status:
                if stages[0] in project_stage_status[prj_id]:
                    if project_stage_status[prj_id][stages[0]][0] == 'Complete':
                        st.markdown(":white_check_mark:")
                    if project_stage_status[prj_id][stages[0]][0] == 'Inprogress':
                        st.markdown(":hourglass_flowing_sand:")
                    if project_stage_status[prj_id][stages[0]][0] == 'Notstarted':
                        st.markdown(":lock:")
                else:
                    st.markdown(":lock:")
            else:
                st.markdown(":lock:")
            
        with col2:
            st.button(stages[1], on_click=locals()[stages[0] + "_click_button"])

        with col3:
            if prj_id in project_stage_status:
                if stages[0] in project_stage_status[prj_id]:
                    if project_stage_status[prj_id][stages[0]][0] == 'Complete':
                        st.markdown(":green[Stage complete {" + 
                                    project_stage_status[prj_id][stages[0]][1] + "}]")
                    if project_stage_status[prj_id][stages[0]][0] == 'Inprogress':
                        st.markdown(":orange[In progress {" +
                                    project_stage_status[prj_id][stages[0]][1] + "}]")
                    if project_stage_status[prj_id][stages[0]][0] == 'Notstarted':
                        st.markdown(":grey[Not started]")
                else:
                    st.markdown(":grey[Not started]")
            else:
                st.markdown(":grey[Not started]")

    st.divider()
    
    st.button('Take me to App Home', on_click=prj_click_button)

    for stages in project_stages:
        if prj_id in project_stage_status:
            if stages[0] in project_stage_status[prj_id]:
                if project_stage_status[prj_id][stages[0]][0] == 'Complete':
                    ChangeButtonColour(stages[1], '#000000', color_map['button-green'])
                if project_stage_status[prj_id][stages[0]][0] == 'Inprogress':
                    ChangeButtonColour(stages[1], '#000000', color_map['button-yellow'])
                if project_stage_status[prj_id][stages[0]][0] == 'Notstarted':
                    ChangeButtonColour(stages[1], '#000000', color_map['button-grey'])
            else:
                ChangeButtonColour(stages[1], '#000000', color_map['button-grey'])
        else:
            ChangeButtonColour(stages[1], '#000000', color_map['button-grey']) 

    ChangeButtonColour('Take me to App Home', 'white', 'orange') # button txt to find, colour to assign
    
