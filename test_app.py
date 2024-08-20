import streamlit as st

st.set_page_config(layout="wide")

# Define the list of travel interests
travel_interests = [
    "Beach", "Mountain", "City", "Historical Sites", "Cultural Events",
    "Adventure Sports", "Nature", "Wildlife", "Food and Dining",
    "Shopping", "Museums", "Art Galleries", "Music Festivals",
    "Nightlife", "Road Trips", "Cruises", "Hiking", "Photography",
    "Religious Sites", "Spiritual Retreats", "Wellness & Spa",
    "Cycling", "Diving", "Snorkeling", "Camping", "Skiing",
    "Snowboarding", "Deserts", "Rainforests", "Islands"
]

# Number of columns
n_columns = 5
# Split the travel interests into columns
columns = st.columns(n_columns)

# Store selected interests
selected_interests = []

st.write("### Select Your Travel Interests:")

# Create a grid of checkboxes using columns
for i, interest in enumerate(travel_interests):
    col = columns[i % n_columns]
    if col.checkbox(interest):
        selected_interests.append(interest)

# Show selected interests
if selected_interests:
    st.write("You have selected:")
    st.write(", ".join(selected_interests))
else:
    st.write("No interests selected")

