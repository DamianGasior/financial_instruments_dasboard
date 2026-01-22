import streamlit as st
from pathlib import Path
import xml.etree.ElementTree as ET
from src.session_init import init_session_state


init_session_state()


BPMN_PATH = Path(__file__).parent.parent / "diagrams" / "diagram_BMPN_svg.svg"
svg = BPMN_PATH.read_text(encoding="utf-8")  # reading the file as a text

README_PATH = Path(__file__).parent.parent / "README.md"


tab1, tab2, tab3 = st.tabs(["About the author", "ReadMe", "BMPN"])


@st.cache_data
def load_bpmn():
    bmpn_image = BPMN_PATH
    return bmpn_image


@st.cache_data
def load_readme():
    readme = README_PATH
    with readme.open(encoding="utf-8") as f:
        readme_text = f.read()
    return readme_text


with tab1:
    st.markdown(
        """
    # About the Author
    
    I have over 15 years of experience in finance, banking, and capital markets.
    Since mid-2018, I have been working in IT, initially as a Business Analyst and currently as a Product Manager.

    In recent years, I have been expanding my technical skill set, focusing on Python development and gradually moving toward data analysis and AI/ML-related topics.
    This project was created as a hands-on, educational initiative to better understand the technical aspects of financial data processing, analytics implementation, and the developer’s perspective on building data-driven applications.
    
    linkedin : https://www.linkedin.com/in/damian-piotr-gasior/

    github : https://github.com/DamianGasior
"""
    )

with tab2:
    read_me = load_readme()
    st.write(read_me)


with tab3:
    st.markdown(
        f"""
    <div style="
        background: white;
        display:inline-block;      
    ">
        {svg}
    
    """,
        unsafe_allow_html=True,  # allows tosee it as a diagram, not as text
    )
