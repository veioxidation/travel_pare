import streamlit as st

from constants import travel_interests, physical_activity_labels, personality_labels
from workflow.TravellerProfile import load_users_from_pkl, TravellerProfile, save_users_to_pkl

st.set_page_config(layout="wide")

users_pkl_filename = r"workflow/test_users.pkl"


class AppModes:
    user_selection = 'user_selection'
    new_user_creation = 'new_user_creation'
    edit_user = 'edit_user'
    preferences_selection = 'preferences_creation'
    show_user = 'show_user'


if 'selected_user' not in st.session_state:
    st.session_state.selected_user = None
if 'app_mode' not in st.session_state:
    st.session_state.app_mode = AppModes.user_selection
if 'users_list' not in st.session_state:
    st.session_state.users_list = load_users_from_pkl(users_pkl_filename)

if st.session_state.selected_user:
    st.write(st.session_state.selected_user.get_traveller_description())

if st.session_state.app_mode != AppModes.user_selection:
    if st.button('Change user...'):
        st.session_state.app_mode = AppModes.user_selection
        st.session_state.selected_user = None
        st.rerun()

# Initial stage: select either an existing user, or introduce a new one.
if st.session_state.app_mode == AppModes.user_selection:
    st.write("### Select a user or create a new one:")
    col1, col2 = st.columns([1, 2])
    with col1:
        users_list_names = [user.name for user in st.session_state.users_list]
        selected_user_name = st.selectbox("Select a user", options=users_list_names)
        if st.button("Load Existing..."):
            # program
            st.session_state.app_mode = AppModes.show_user
            selected_user = [user for user in st.session_state.users_list if user.name == selected_user_name][0]
            st.session_state.selected_user = selected_user
            st.rerun()

    with col2:
        if st.button("Create New..."):
            # program
            st.session_state.app_mode = AppModes.new_user_creation
            st.rerun()

if st.session_state.app_mode == AppModes.new_user_creation or st.session_state.app_mode == AppModes.edit_user:
    _user = st.session_state.selected_user
    if not _user:
        st.write("### Create a new user:")
        user_name = st.text_input("Name:", value="")
        physical_activity_level = st.selectbox("Physical Activity Level", options=physical_activity_labels)
        personality = st.selectbox("Physical Activity Level", options=personality_labels)
    else:
        st.write(f"### Edit user - {_user.name}:")
        user_name = st.text_input("Name:", value=_user.name)
        physical_activity_level = st.selectbox("Physical Activity Level",
                                               options=physical_activity_labels,
                                               index=physical_activity_labels.index(_user.physical_level))
        personality = st.selectbox("Physical Activity Level",
                                   options=personality_labels,
                                   index=personality_labels.index(_user.personality))

    # Define the list of travel interests
    # Number of columns
    N_COLS = 5
    # Split the travel interests into columns
    columns = st.columns(N_COLS)
    # Store selected interests

    st.write("### Select Travel Interests:")
    selected_interests = []
    # Create a grid of checkboxes using columns
    for i, interest in enumerate(travel_interests):
        col = columns[i % N_COLS]
        if col.checkbox(interest, value=interest in _user.interests if _user else False):
            selected_interests.append(interest)

    if st.session_state.app_mode == AppModes.new_user_creation:
        if st.button("Create User"):
            # program
            user = TravellerProfile(name=user_name,
                                    physical_level=physical_activity_level,
                                    personality=personality,
                                    interests=selected_interests)
            st.session_state.selected_user = user
            st.session_state.users_list.append(user)
            save_users_to_pkl(st.session_state.users_list, users_pkl_filename)
            st.session_state.app_mode = AppModes.show_user
            st.rerun()

    elif st.session_state.app_mode == AppModes.edit_user:
        if st.button("Save Changes"):
            # program
            _user = st.session_state.selected_user
            _user.name = user_name
            _user.physical_level = physical_activity_level
            _user.personality = personality
            _user.interests = selected_interests
            # save the changes
            st.session_state.users_list[st.session_state.users_list.index(_user)] = st.session_state.selected_user
            save_users_to_pkl(st.session_state.users_list, users_pkl_filename)
            st.session_state.app_mode = AppModes.show_user
            st.rerun()

if st.session_state.app_mode == AppModes.show_user and st.session_state.selected_user:
    # show all information about the user. Allow to change mode as well to perform edits.
    _user = st.session_state.selected_user
    st.header(f"User name: {_user.name}")
    st.subheader(f"Personality: {_user.personality}")
    st.subheader(f"Activity level: {_user.physical_level}")
    st.write(f"Interests: {', '.join(_user.interests)}")
    if st.button("Edit"):
        st.session_state.app_mode = AppModes.edit_user
        st.rerun()
