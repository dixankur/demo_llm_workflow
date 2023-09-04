import json
import streamlit as st

from webapp.utils import load_json

projects = load_json('./datamodel/projects.json')

project_stages = load_json('./datamodel/project_stages.json')

project_stage_status = load_json('./datamodel/project_stage_status.json')

project_feature_list = load_json('./datamodel/project_feature_list.json')

# List of projects
def update_data():
    global projects, project_stages, project_stage_status, project_feature_list

    projects = load_json('./datamodel/projects.json')
    project_stages = load_json('./datamodel/project_stages.json')
    project_stage_status = load_json('./datamodel/project_stage_status.json')
    project_feature_list = load_json('./datamodel/project_feature_list.json')
