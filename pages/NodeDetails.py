import streamlit as st

st.set_page_config("Node Details", layout="wide", initial_sidebar_state="collapsed")
st.title("Node Details Page")

# 📌 Retrieve Selected Node
if "selected_node" in st.session_state:
    selected_node = st.session_state["selected_node"]
    st.header(f"Details for: {selected_node}")
    st.write("🔹 Additional information about this topic can go here.")

    # ✅ Button to return to the mind map
else:
    st.error("No node selected! Please go back and click a node.")

if st.button("🔙 Back to Mind Map"):
    del st.session_state["selected_node"]
    del st.session_state["curr_state"]
    print(st.session_state)
    st.switch_page("pages/GenFlow.py")
