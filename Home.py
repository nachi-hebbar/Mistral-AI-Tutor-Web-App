import streamlit as st
from utils.st_utils import display_home_page

st.set_page_config(page_title="AI Study Buddy", layout="wide")
st.sidebar.info("Select a page to master your study material!")

# Display the Home Page
display_home_page()