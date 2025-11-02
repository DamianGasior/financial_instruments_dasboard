import pdb
import streamlit as st
import sys # allows to access to  information used by interpreter , in this case will be used to  point out to the src folder
import os # allows to interact with the operating system , like checking the paths , catalogs and so on 
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))


# Dodaj folder główny projektu do sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from src.api_request_alphavantage import Underlying_request_details
from src.main import main
from src import pipeline

# os.path.dirname(__file__) - location of the folder where the streamlit_app.py file is , in this case its : app/
# os.path.join(..., '..', 'src') - moving one level higher and pointing out to 'src'
# (os.path.abspath(...) - changing that a full path 
# sys.path.append(...) - adding this  folder to places where python needs to search for modules
if "submit_button" not in st.session_state:
    st.session_state.submit_button = False
if "selected_symbols" not in st.session_state:
    st.session_state.selected_symbols = []


st.set_page_config(layout="wide")

st.title("💻Welcome to the financial dashboard")


# Initialize the list in session state if it doesn't exist

if "my_list" not in st.session_state:
    st.session_state.my_list = []

with st.form("add_item_form",clear_on_submit=True):
    new_item = st.text_input("Enter a specfic stock symbol")
    submitted = st.form_submit_button("Add symbol")
    new_item_upper=new_item.upper()
if submitted and new_item_upper:
    if new_item_upper in  st.session_state.my_list :
        pass
    else:
         st.session_state.my_list.append(new_item_upper)




with st.sidebar:
    st.title("🔣:small[Your symbols ]")
    # st.session_state.my_list
    st.markdown("Chosen symbols are : ")
    for symbol in st.session_state.my_list:
        st.markdown(f'- {symbol}')
    # selected_symbols=st.multiselect(
    #     'Select your symbols',st.session_state.my_list)

st.markdown("Once you are completed , please  hit **Submit button**")


# button=st.button("Submit button") # create a button to start the whole flow 


if st.session_state.my_list :
    if st.button("Submit button",key="submit_btn"):
        # print("tutaj",st.session_state.my_list)
        st.session_state.submit_button=True
        main()

if st.session_state.submit_button : #checking if submit button exists
    # pdb.set_trace()
    with st.sidebar:
        st.session_state.selected_symbols = st.multiselect(
                'Select your symbols',
                st.session_state.my_list,
                default=st.session_state.selected_symbols,
                key="symbols_multiselect")
    
print('st.session_state.selected_symbols',st.session_state.selected_symbols)
print('st.multiselect',st.multiselect)
                
if len(st.session_state.selected_symbols) ==1 :
    for symbol in st.session_state.selected_symbols:
        symbol=st.session_state.selected_symbols[0]
        df=pipeline.multiple_data_frame.get_the_right_df(symbol)
        st.dataframe(df,use_container_width=True)
elif len(st.session_state.selected_symbols) >1 :
        for symbol in st.session_state.selected_symbols:
            df=pipeline.multiple_data_frame.get_the_right_df(symbol)       #multiple_data_frame_creator(symbol)
            st.dataframe(df,use_container_width=True)

else:
    pass
        # st.data_editor(df, use_container_width=True, disabled=True)


# https://docs.streamlit.io/develop/api-reference/text/st.markdown

# https://emojipedia.org/laptop
