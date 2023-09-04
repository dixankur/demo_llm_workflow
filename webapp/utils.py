# all common funtions related to streamlit web app
import json
import random
import time
import streamlit as st
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
from streamlit_star_rating import st_star_rating

def ChangeButtonColour(widget_label, font_color, background_color='transparent'):
    htmlstr = f"""
        <script>
            var elements = window.parent.document.querySelectorAll('button');
            for (var i = 0; i < elements.length; ++i) {{ 
                if (elements[i].innerText == '{widget_label}') {{ 
                    elements[i].style.color ='{font_color}';
                    elements[i].style.background = '{background_color}';
                    /*elements[i].style.height = 'fit-content';*/
                    elements[i].style.width = '250px';
                }}
            }}
        </script>
        """
    components.html(f"{htmlstr}")


def load_json(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
    return data


def save_json(json_dict, json_path):
    # Serializing json
    json_object = json.dumps(json_dict, indent=4)
    
    # Writing to sample.json
    with open(json_path, "w") as outfile:
        outfile.write(json_object)


def option_click_button(key):
    selection = st.session_state[key]

    if selection == "Ask me anything":
            st.session_state['current_page'] = 'amy_chat'

    if selection == "Home":
        if st.session_state['current_page'] == 'prj_home':
            st.session_state['current_page'] = 'app_home'
        else:
            st.session_state['current_page'] = 'prj_home'


def add_sidebar(header, prj_name, notes):
    # sidebar
    with st.sidebar:
        st.markdown("<h1 style='color:tomato;font-size:200%;font-family:verdana'>" + header + "</h1>",
             unsafe_allow_html=True)
        
        choice = option_menu(
            #"App Gallery",
            None,
            ["Menu", "Home", "Ask me anything"],
            icons=['menu-app', 'house', 'chat-dots'],
            menu_icon="app-indicator",
            default_index=0,
            on_change=option_click_button,
            key='option_choice',
            styles={
                "container": {"padding": "2!important", "background-color": "#fafafa"},
                "icon": {"color": "tomato", "font-size": "20px"}, 
                "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "tomato", "color": "white"},
            }
        )

        st.markdown("<h2 style='color:tomato;font-size:100%;font-family:verdana'>Project:</h2>",
             unsafe_allow_html=True)
        st.markdown("<h2 style='color:blue;font-size:150%;font-family:verdana'>" + prj_name + "</h2>",
             unsafe_allow_html=True)
        
        st.write(" ")
        for note in notes:
            st.write(note)
        


def provide_rating(prj_id, rating_id):

    rating_data = load_json('./datamodel/ratings.json')
    if prj_id not in rating_data:
        rating_data[prj_id] = {}

    prj_rating = rating_data[prj_id]

    init_rate = prj_rating.get(rating_id, 0)
    st.markdown(f"**Please rate your experience**")
    stars = st_star_rating(None, maxValue=10, defaultValue=init_rate, key="rating",
                    size=25, resetButton=True, resetLabel="Reset Rating")
    st.markdown(f":green[You rated: {stars} stars]")

    rating_data[prj_id][rating_id] = stars
    save_json(rating_data, './datamodel/ratings.json')


def chat_window(prj_id, chat_id):

    chat_data = load_json('./datamodel/chat_history.json')
    if prj_id in chat_data:
        prj_chat = chat_data[prj_id]
    else:
        chat_data[prj_id][chat_id] = []
        prj_chat= {}

    page_chat = prj_chat.get(chat_id, [])
    
    #st.subheader("Ask me anything:")
    #st.subheader(':blue[Ask me anything]', divider='rainbow')

    chat_container = st.container()

    with chat_container:

        # Display chat messages from history on app rerun
        for message in page_chat:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Accept user input
        if prompt := st.chat_input("Ask me anything here..."):
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)
            
            assistant_response = random.choice(
                [
                    "Hello there! Your answer comming soon",
                    "Hi, human! The answer is on its way!",
                    "You don't know even this?",
                ]
            )

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                
                # Simulate stream of response with milliseconds delay
                for chunk in assistant_response.split():
                    full_response += chunk + " "
                    time.sleep(0.05)
                    # Add a blinking cursor to simulate typing
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)

            # Add user and asistant message to chat history
            chat_data[prj_id][chat_id].append({"role": "user", "content": prompt})
            chat_data[prj_id][chat_id].append({"role": "assistant", "content": full_response})

            save_json(chat_data, './datamodel/chat_history.json')


def provide_appoval(prj_id, approval_id, button_text, **kw_args):

    approval_data = load_json('./datamodel/approvals.json')
    if prj_id not in approval_data:
        approval_data[prj_id] = {}

    prj_approvals = approval_data[prj_id]

    init_approval = prj_approvals.get(approval_id, None)
    apv_butt = st.button(button_text, **kw_args)
    if apv_butt:
        init_approval = time.time()
        approval_data[prj_id][approval_id] = init_approval

    if init_approval:
        st.markdown(f":green[Approval provided at: {time.ctime(init_approval)}]")
    else:
        st.markdown(":red[Approval not provided yet]")

    save_json(approval_data, './datamodel/approvals.json')
    return init_approval


def update_status_and_audit(prj_id, stage_id, status, status_text):

    status_data = load_json('./datamodel/project_stage_status.json')
    if prj_id not in status_data:
        status_data[prj_id] = {}

    status_data[prj_id][stage_id] = [status, status_text]

    save_json(status_data, './datamodel/project_stage_status.json')

