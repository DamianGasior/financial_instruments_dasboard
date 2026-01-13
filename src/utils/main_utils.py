# import streamlit as st
# from src.session_init import init_session_state


# init_session_state()


# def combined_lists(symbols_from_user, benchmarks):
#     st.session_state.my_merged_list = symbols_from_user + benchmarks
#     return st.session_state.my_merged_list

benchmark='SPY'
symbols=['AEM','PHYS']
symbols_with_benchmark=symbols


symbols_with_benchmark.append(benchmark)

print(symbols_with_benchmark)