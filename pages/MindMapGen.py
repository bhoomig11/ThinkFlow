import streamlit as st
import ollama
import json
import re
import pymongo

import streamlit as st
from streamlit_flow import streamlit_flow
from streamlit_flow.elements import StreamlitFlowNode, StreamlitFlowEdge
from streamlit_flow.state import StreamlitFlowState
from streamlit_flow.layouts import TreeLayout, RadialLayout
import random
from uuid import uuid4
import json
from pages.utils import adult_summary_generate, teen_summary_generate, child_summary_generate

st.set_page_config(
        page_title="Mind Map Generator", initial_sidebar_state="collapsed"
)


# MongoDB Connection (Use your actual connection string)
MONGO_URI = "mongodb+srv://ritika0204:ritikakumar@hack.6nemp.mongodb.net/?retryWrites=true&w=majority&appName=Hack"
client = pymongo.MongoClient(MONGO_URI)
db = client["mind_map_db"]  # Database Name
collection = db["Hack"]  # Collection Name
summary = db["summary"]

# Streamlit UI setup
st.title("🧠 MindMapGen")

# Get user input
user_input = st.text_input("Enter a topic for your mind map:", "")



def generate_nodes_edges(json_data):
    nodes = []
    edges = []

    root_id = "root"  # Static root ID for easy tracking
    nodes.append(StreamlitFlowNode(root_id, (0, 0), {'content': json_data["topic"]}, 'input', 'right'))

    for subtopic in json_data["subtopics"]:
        subtopic_id = str(uuid4())
        nodes.append(StreamlitFlowNode(subtopic_id, (1, 0), {'content': subtopic["name"]}, 'default', 'right', 'left'))
        edges.append(StreamlitFlowEdge(f"{root_id}-{subtopic_id}", root_id, subtopic_id, animated=True))

        for child in subtopic["children"]:
            child_id = str(uuid4())
            nodes.append(StreamlitFlowNode(child_id, (2, 0), {'content': child}, 'output', 'left'))
            edges.append(StreamlitFlowEdge(f"{subtopic_id}-{child_id}", subtopic_id, child_id, animated=True))

    return nodes, edges

def run_map(json_data):
    # 📌 Initialize session state for nodes and edges
    if "curr_state" not in st.session_state:
        nodes, edges = generate_nodes_edges(json_data)
        st.session_state.curr_state = StreamlitFlowState(nodes, edges)

    # 📌 Render Mind Map with Clickable Nodes
    st.session_state.curr_state = streamlit_flow(
        'mind_map_flow',
        st.session_state.curr_state,
        layout=TreeLayout(direction='right'),
        fit_view=True,
        height=500,
        enable_node_menu=True,
        enable_edge_menu=True,
        enable_pane_menu=True,
        get_node_on_click=True,  # ✅ Ensure clicks are captured
        show_minimap=False,
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
                st.switch_page("details.py")
                #st.experimental_rerun()


def adult_sum(user_input):
    existing_mind_map = summary.find_one({"user_input": user_input}, {"_id": 0})
    if existing_mind_map:
        s = existing_mind_map['summary']
        st.text(s)
    else:
        #### CODE TO GENERATE SUMMARY AND SAVE TO DB ###
        response = adult_summary_generate(user_input, summary)
        st.text(response)

        
def teen_sum(user_input):
    existing_mind_map = summary.find_one({"user_input": user_input}, {"_id": 0})
    if existing_mind_map:
        s = existing_mind_map['summary']
        st.text(s)
    else:
        #### CODE TO GENERATE SUMMARY AND SAVE TO DB ###
        response = teen_summary_generate(user_input, summary)
        st.text(response)

def child_sum(user_input):
    existing_mind_map = summary.find_one({"user_input": user_input}, {"_id": 0})
    if existing_mind_map:
        s = existing_mind_map['summary']
        st.text(s)
    else:
        #### CODE TO GENERATE SUMMARY AND SAVE TO DB ###
        response = child_summary_generate(user_input, summary)
        st.text(response)


    
def adult_map(user_input):
    existing_mind_map = collection.find_one({"topic": user_input}, {"_id": 0})
    if existing_mind_map:
        st.subheader("📂 Retrieved from Database (Existing Mind Map)")
        st.json(existing_mind_map["mind_map"])
        json_data = existing_mind_map["mind_map"]
        st.session_state["mind_map"] = existing_mind_map["mind_map"]
        #run_map(json_data)
        st.switch_page("pages/GenFlow.py") 
        st.success("This mind map was already generated and retrieved from the database. ✅")
        #st.components.v1.html(display_html('mindmap.html'), height=600, scrolling=True)
    else:

        with st.spinner("Generating mind map... ⏳"):
            # Define DeepSeek model
            model = "deepseek-r1:14b"

            # Define prompt
            prompt = f"""
                Generate a structured JSON mind map for the topic: {user_input}.
                The output should be a JSON structure with nodes and edges.
                Only output the JSON structure. Ensure there are exactly two children in each subtopic.

                Example output:
                {{
                    "topic": "{user_input}",
                    "subtopics": [
                        {{
                            "name": "Subtopic 1",
                            "children": ["Concept 1", "Concept 2"]
                        }},
                        {{
                            "name": "Subtopic 2",
                            "children": ["Concept A", "Concept B"]
                        }}
                    ]
                }}
            """

            # Define conversation messages
            messages = [
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_input}
            ]

            try:
                # Call Ollama's chat API
                response = ollama.chat(model=model, messages=messages)
                response_text = response["message"]["content"]
                print(response_text)
                final_answer = response_text.split('json')[1]
                extracted_json = json.loads(final_answer.split('```')[0].strip()) 


                # Display JSON output
                st.subheader("Generated Mind Map (JSON Output):")
                st.json(extracted_json)


                # Save JSON to file
                with open("mind_map.json", "w") as file:
                    json.dump(extracted_json, file, indent=4)

                data_to_store = {
                    "topic": user_input,
                    "mind_map": extracted_json
                }
                collection.insert_one(data_to_store)
                
                st.success("Mind map saved as `mind_map.json` 🎉")
            except json.JSONDecodeError as e:
                st.error(f"Error parsing JSON: {e}")


if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def click_button():
    st.session_state.clicked = True

if st.button("Let's Learn!"):
    click_button()
    if user_input.strip() == "":
        st.error("Please enter a valid topic.")
    else:
        if st.session_state["user_info"]['age'] == '8-12':
            child_sum(user_input)
        elif st.session_state["user_info"] ['age'] == '12-18':
            teen_sum(user_input)
        else:
            adult_sum(user_input)
if st.session_state.clicked == True:
    if st.button("Generate Mind Map"):
                adult_map(user_input)
        