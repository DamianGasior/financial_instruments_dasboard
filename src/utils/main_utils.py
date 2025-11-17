import streamlit as st


if "my_merged_list" not in st.session_state:
    st.session_state.my_merged_list = []


@staticmethod
def combined_lists(symbols_from_user, benchmarks):
    st.session_state.my_merged_list = symbols_from_user + benchmarks
    return st.session_state.my_merged_list
