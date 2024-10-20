import streamlit as st
import numpy as np
import pandas as pd
from langchain_openai.chat_models import ChatOpenAI
import altair as alt
import time
from cgm import CGM
from chat_agent import ChatAgent
 
# st.title("🦜🔗 Quickstart App")
st.title("Prime Agent")

openai_api_key = st.secrets["OpenAI_key"]
# openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
llm_model_gpt_mini = "gpt-4o-mini"

def generate_response(input_text):
    model = ChatOpenAI(temperature=0.7,  model=llm_model_gpt_mini, api_key=openai_api_key)
    st.info(model.invoke(input_text))

# def call_remote_client():
#     client

## --------- Draft above ----------------------##

chatagent = ChatAgent(llm_api_key=openai_api_key, model_name=llm_model_gpt_mini)
chatagent.initialize_chat()

##-- i/p elements ------#
# Create a form
# Initialize session state for inputs if not already set
if 'option_select' not in st.session_state:
    st.session_state.option_select = None
if 'number_input' not in st.session_state:
    st.session_state.number_input = 0
if 'checkbox_input' not in st.session_state:
    st.session_state.checkbox_input = False

# Create a form
with st.form("form_inputs"):
    # Create 3 columns inside the form
    col1, col2, col3 = st.columns(3)

    # Add widgets to the first column
    with col1:
        st.header("Column 1")
        ip_option = st.selectbox("Select an option:", ["Option A", "Option B", "Option C"], key="option_select")
        st.write(f"You selected initial: {st.session_state.option_select}")
        st.write(f"You selected now: {ip_option}")

    # Add widgets to the second column
    with col2:
        st.header("Column 2")
        ip_number = st.number_input("Enter a number:", min_value=0, max_value=100, key="number_input")

    # Add widgets to the third column
    with col3:
        st.header("Column 3")
        ip_checkbox = st.checkbox("Check me!", value=False, key="checkbox_input")

    # Submit button for the form
    submit_button = st.form_submit_button("Submit", "input_button")

# Handle the form submission without losing state
if submit_button:
    # Display the selected values
    st.write(f"You selected: {st.session_state.option_select}")
    st.write(f"You entered: {st.session_state.number_input}")
    st.write(f"Checkbox is {'checked' if st.session_state.checkbox_input else 'unchecked'}")


# Initialize session state for the selected option
if "selected_option_activity" not in st.session_state:
    st.session_state.selected_option_activity = None

def update_selection():
    st.session_state.selected_option_activity = st.session_state.key_activity
    st.write(f"Updated session state: {st.session_state.selected_option_activity}")

@st.fragment
def frg_option():
    st.write("Please choose an frg option from the dropdown:")
    selected_option = st.selectbox(
        "Exercise:", 
        ['Cardio', 'Weight', 'Swimming'], 
        key="key_activity",
        on_change=update_selection
    )   
        # Display the selected option from session state
    if st.session_state.selected_option_activity:
        st.write(f"You selected: {st.session_state.selected_option_activity}")

frg_option()


# Step 1: Define the fragment function
def sidebar_fragment():
    # Add elements to the sidebar
    st.sidebar.write("### Sidebar Menu")
    
    # Create a selectbox
    option = st.sidebar.selectbox(
        "Choose an option:",
        ["Option 1", "Option 2", "Option 3"],
        key="sidebar_option"  # Unique key for the selectbox
    )

    # Create a checkbox
    checkbox_value = st.sidebar.checkbox("Check me!", key="sidebar_checkbox")

    # Display the selected values
    st.sidebar.write(f"You selected: {option}")
    st.sidebar.write(f"Checkbox is {'checked' if checkbox_value else 'unchecked'}")

# Step 2: Use the context manager for the sidebar
with st.sidebar:  # Start the sidebar context
    sidebar_fragment()  # Call the fragment function to write elements to the sidebar


# Initialize session state for the selected option
if "selected_option_activity" not in st.session_state:
    st.session_state.selected_option_activity = None

def update_selection_activity():
    st.session_state.selected_option_activity = st.session_state.key_activity_option
    st.write(f"Updated session state: {st.session_state.selected_option_activity}")

# Create a container inside the sidebar (fragment)
with st.sidebar.container():
    st.sidebar.write("Select an activity:")
    st.sidebar.selectbox(
        "Choose an option", 
        ['Running', 'Aerobics', 'Weights'], 
        key="key_activity_option",
        on_change=update_selection_activity
    )
    if st.session_state.selected_option_activity:
        st.write(f"You selected: {st.session_state.selected_option_activity}")

with st.sidebar:
    add_radio = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )

# for the fragment 
# if 'count' not in st.session_state:
#     st.session_state.count = 0

# @st.fragment(run_every="3s")
@st.fragment()
def frg_cgm_auto_update(glucose_chart, cg_data, cgm : CGM, duration_in_minutes : int):
    # Simulating dynamic data updates
    placeholder = st.empty()
    for i in range(20):  # Simulate 5 new data points coming in
        time.sleep(2)  # Simulating a time delay (can be removed for real-time updates)
        
        # Generate new data point
        new_time = pd.Timestamp.now() + pd.Timedelta(minutes=duration_in_minutes *(cgm.num_points+i))
        new_glucose_level = np.random.normal(loc=100, scale=10)
        
        # Add the new data
        cg_data = cgm.add_new_data(cg_data, new_time, new_glucose_level)
        
        # Re-render the chart (in a real environment, this would dynamically refresh)
        glucose_chart = alt.Chart(cg_data).mark_line(point=True).encode(
            x='Time:T',
            y='Glucose Level (mg/dL):Q',
            tooltip=['Time:T', 'Glucose Level (mg/dL):Q']
        ).properties(
            title='Continuous Glucose Monitoring (Dynamic Update)',
            width=600,
            height=300
        )
        with placeholder:
            st.altair_chart(glucose_chart, use_container_width=True)

cgm = CGM(start_time = pd.Timestamp.now(), num_points=1, duration_in_minutes=5)
cg_data = cgm.cg_data
glucose_chart = cgm.initiate_cgm_chart()
frg_cgm_auto_update(glucose_chart, cg_data, cgm, 5)

_LOREM_IPSUM = """
Lorem ipsum dolor sit amet, **consectetur adipiscing** elit, sed do eiusmod tempor
incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis
nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
"""


def stream_data():
    for word in _LOREM_IPSUM.split(" "):
        yield word + " "
        time.sleep(0.1)

    yield pd.DataFrame(
        np.random.randn(5, 10),
        columns=["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"],
    )

    for word in _LOREM_IPSUM.split(" "):
        yield word + " "
        time.sleep(0.5)


with st.form("data_stream_form"):   
    submitted = st.form_submit_button("Submit")

if st.button("Stream data"):
    st.write_stream(stream_data)

with st.form("my_form"):
    text = st.text_area(
        "Enter text:",
        "What are the three key pieces of advice for learning how to code?",
    )
    submitted = st.form_submit_button("Submit")
    if not openai_api_key.startswith("sk-"):
        st.warning("Please enter your OpenAI API key!", icon="⚠")
    if submitted and openai_api_key.startswith("sk-"):
        generate_response(text)

with st.chat_message("user"):
    st.write("Hello 👋")
    st.line_chart(np.random.randn(30, 3))

with st.form("data_form"):
    st.write(1234)
    st.write(
        pd.DataFrame(
            {
            "first column": [1, 2, 3, 4],
            "second column": [10, 20, 30, 40],
             }
        )
    )
