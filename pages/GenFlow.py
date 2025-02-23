import streamlit as st
from streamlit_flow import streamlit_flow
from streamlit_flow.elements import StreamlitFlowNode, StreamlitFlowEdge
from streamlit_flow.state import StreamlitFlowState
from streamlit_flow.layouts import TreeLayout, RadialLayout
import random
from uuid import uuid4
import json

st.set_page_config("Streamlit Flow Example", layout="wide", initial_sidebar_state="collapsed")

st.title("Generated Mind Map")

json_data = st.session_state["mind_map"]

# 📌 Function to Generate Nodes & Edges
def generate_nodes_edges(json_data):
    nodes = []
    edges = []

    root_id = "root"  # Static root ID for easy tracking
    nodes.append(StreamlitFlowNode(root_id, (0, 0), {'content': json_data["topic"]}, 'input', 'bottom'))

    for subtopic in json_data["subtopics"]:
        subtopic_id = str(uuid4())
        nodes.append(StreamlitFlowNode(subtopic_id, (1, 0), {'content': subtopic["name"]}, 'default', 'bottom', 'top'))
        edges.append(StreamlitFlowEdge(f"{root_id}-{subtopic_id}", root_id, subtopic_id, animated=True))

        for child in subtopic["children"]:
            child_id = str(uuid4())
            nodes.append(StreamlitFlowNode(child_id, (2, 0), {'content': child}, 'output', 'bottom'))
            edges.append(StreamlitFlowEdge(f"{subtopic_id}-{child_id}", subtopic_id, child_id, animated=True))

    return nodes, edges

def run_map(json_data):
    #st.set_page_config(initial_sidebar_state="collapsed")
    # 📌 Initialize session state for nodes and edges
    if "curr_state" not in st.session_state:
        nodes, edges = generate_nodes_edges(json_data)
        st.session_state.curr_state = StreamlitFlowState(nodes, edges)

    # 📌 Render Mind Map with Clickable Nodes
    st.session_state.curr_state = streamlit_flow(
        'mind_map_flow',
        st.session_state.curr_state,
        layout=TreeLayout(direction='down'),
        fit_view=True,
        height=500,
        enable_node_menu=True,
        enable_edge_menu=True,
        enable_pane_menu=True,
        get_node_on_click=True,  # ✅ Ensure clicks are captured
        show_minimap=True,
        hide_watermark=True
    )

    # 📌 Detect Node Click
    if hasattr(st.session_state.curr_state, "selected_id") and st.session_state.curr_state.selected_id:
        clicked_node_id = st.session_state.curr_state.selected_id

        # Find the clicked node content
        for node in st.session_state.curr_state.nodes:
            if node.id == clicked_node_id:
                st.session_state["selected_node"] = node.data['content']
                st.success(f"✅ Node Clicked: {node.data['content']}")

                # ✅ Redirect to details.py (Next Page)
                st.switch_page("pages/NodeDetails.py")
                st.experimental_rerun()

run_map(json_data)