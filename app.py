import datetime
import sys

import streamlit as st
from langchain_core.messages import HumanMessage

from dotenv import load_dotenv

from database.clean_memory import reset_memory
from interface.AppProperties import AppProperties
from utils import strip_markdown_markings
from workflow.app_state_helpers import get_all_writes_messages, is_human_node_next, has_started, has_itinerary, \
    has_bookings, has_finished, get_next_node, get_writes

load_dotenv()

from country_data_parser import country_df, filter_for_population_in_between
from workflow.TripPlannerState import TripPlannerState
from workflow.graph_definition import app, Nodes


def reload_config(country: str):
    st.session_state.chat_config = {'configurable': {'thread_id': country}}


_ss = st.session_state

if 'selected_user' not in st.session_state:
    st.title("Traveller - select user first!")
else:
    st.title(f"Hello, {st.session_state.selected_user.name}!")
    st.write(f"{st.session_state.selected_user.get_traveler_intro_message()}")


# App initialization
if 'app_properties' not in st.session_state:
    _ss.app_properties = AppProperties()
_ap = st.session_state.app_properties
if 'chat_config' not in st.session_state:
    # Initialize chat config
    st.session_state.chat_config = None
if 'load_count' not in st.session_state:
    _ss.load_count = 0

with st.sidebar:
    st.header("Filters")
    min_pop = 10 ** 6 * st.number_input("Minimum population [M]", value=0, step=100)
    max_pop = 10 ** 6 * st.number_input("Maximum population [M]", value=100, step=10)
    region = st.selectbox("Select a region", country_df['Region'].unique())

    # Country selection - it needs to refresh when the region and population range changes
    filtered_countries = country_df[filter_for_population_in_between(min_pop, max_pop)]
    filtered_countries = filtered_countries[filtered_countries['Region'] == region]
    _ap.origin_country = st.text_input("Origin country", value="Singapore")

    with st.form("TARE Form"):
        __countries = st.multiselect("Select a country", filtered_countries['Country'].tolist())
        __start_date = st.date_input("Start date", value=datetime.date.today())
        __end_date = st.date_input("End date", value=datetime.date.today() + datetime.timedelta(days=7))

        _time_diff = (__end_date - __start_date).days
        st.write(f"Duration: {_time_diff} days")

        # Every form must have a submit button.
        load_button = st.form_submit_button("Load TARE", disabled=not bool(st.session_state.get('selected_user')))
        if load_button:
            _ap.country = ",".join(__countries).strip()
            _ap.start_date = __start_date
            _ap.end_date = __end_date
            reload_config(_ap.country)



def run_chain():
    """
    Run the chain.
    :return:
    """
    reload_config(_ap.country)
    app_state = app.get_state(_ss.chat_config)
    if is_human_node_next(app_state) or has_finished(app_state):
        # The app is waiting for the user input.
        return None
    else:
        # Initial Run
        input_ = TripPlannerState(messages=[],
                                  start_date=_ap.start_date.strftime('%Y-%m-%d'),
                                  end_date=_ap.end_date.strftime('%Y-%m-%d'),
                                  origin_country=_ap.origin_country,
                                  destination_country=_ap.country,
                                  traveler_info=_ss.selected_user.get_traveler_intro_message()) \
            if not has_started(app_state) else None

    # Continue running the chain until it gets interrupted.
    st.session_state.buttons = []
    for event in app.stream(input=input_,
                            config=_ss.chat_config,
                            stream_mode='values'):
        # Update the messages list right after the execution.
        app_state = app.get_state(_ss.chat_config)
        with st.spinner(f'Loading messages... {get_next_node(app_state)}'):
            writes = get_writes(app_state)
            if isinstance(writes, dict):
                for node, writes_info in writes.items():
                    if 'messages' in writes_info:
                        for msg in writes_info['messages']:
                            with st.chat_message("ai"):
                                st.markdown(msg.content)
                    if 'potential_answers' in writes_info:
                        for potential_answer in writes_info['potential_answers']:
                            st.session_state.buttons = potential_answer

    load_app_state()
    st.rerun()


def handle_user_answer(config, user_input: str, as_node: str = Nodes.human_input):
    app.update_state(config, {"messages": [HumanMessage(user_input)]},
                     as_node=as_node)


def load_app_state():
    _ss.app_state = app.get_state(config=st.session_state.chat_config)
    _ap.messages = _ss.app_state.values.get('messages', [])


if not _ap.country:
    sys.exit()


col1, col2 = st.columns([1, 2])
with col1:
    if st.button("Refresh"):
        reload_config(_ap.country)

with col2:
    if st.button(f"Reset thread for {_ss.chat_config['configurable']['thread_id']}"):
        reset_memory(_ss.chat_config['configurable']['thread_id'])
        with st.spinner('Resetting chat...'):
            _ss.app_properties = AppProperties()
            reload_config(_ap.country)
            run_chain()
            st.rerun()

## TOP MENU
load_app_state()
st.subheader(f"Country: {str(_ss.app_state.values.get('destination_country'))} : from {_ss.app_state.values.get('start_date')} to {_ss.app_state.values.get('end_date')}")
# show the next stage.
_ss.load_count += 1

with st.expander("Debug"):
    st.write(f"Config: {_ss.chat_config})")
    # st.write(f"Session state: {st.session_state})")
    for key, value in _ss.items():
        st.write(f"{key}: {str(value)[:300]}")
    for key, value in _ss.app_state.values.items():
        st.write(f"{key}: {str(value)[:300]}")
    st.write(f"Message count: {len(_ap.messages)})")
    if has_started(_ss.app_state):
        st.write(f"next state: {str(_ss.app_state.next)})")
        st.write(f"Load count: {str(_ss.load_count)}")
    else:
        with st.spinner('Running initial...'):
            run_chain()
        st.write(f"next state: {str(_ss.app_state.next)})")
        st.write(
            f"Country: {str(_ss.app_state.values['destination_country'])} : from {_ss.app_state.values['start_date']} to {_ss.app_state.values['end_date']}")
        st.write(f"Load count: {str(_ss.load_count)}")

if not is_human_node_next(_ss.app_state) and not has_finished(_ss.app_state):
    with st.spinner(f'Running step {_ss.app_state.next} ...'):
        run_chain()
        st.rerun()

# Contents
_ap.chat_open = has_started(_ss.app_state)
_ap.writing_mode = is_human_node_next(_ss.app_state)

tabs_list = ['Chat']
if has_itinerary(_ss.app_state):
    tabs_list.append("Itinerary")
if has_bookings(_ss.app_state):
    tabs_list.append("Bookings")
tabs = st.tabs(tabs_list)

with tabs[0]:
    if _ap.chat_open:
        # Produce a chat interface
        for message in _ap.messages:
            with st.chat_message(message.type):
                st.markdown(message.content)

        if prompt := st.chat_input("tell me...", disabled=not _ap.writing_mode):
            with st.chat_message("user"):
                st.markdown(prompt)
            # Populating the user answer in the chain
            handle_user_answer(_ss.chat_config, prompt)
            with st.spinner('Generating response...'):
                # Generating a response...
                run_chain()

if has_itinerary(_ss.app_state):
    with tabs[1]:
        # Print a summary from the app state
        if 'itinerary' in _ss.app_state.values:
            if trip_plan := _ss.app_state.values['itinerary']:
                st.write(strip_markdown_markings(trip_plan))
        else:
            st.write("No trip details available yet!")

if has_bookings(_ss.app_state):
    with tabs[2]:
        if 'bookings' in _ss.app_state.values:
            if bookings := _ss.app_state.values['bookings']:
                st.write(strip_markdown_markings(bookings))
        else:
            st.write("No bookings available yet!")
