import streamlit as st
import requests


# Function to fetch data from the API
def fetch_data_from_api(action_name):
    url = f"https://actionpred.onrender.com/custom-query?action_name={action_name}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error fetching data from API.")
        return []


# Streamlit app layout
st.title("Next Action Prediction")

# Create a textbox and button for user input
action_name = st.text_input("Enter action name", "")
submit_button = st.button("Submit")

# When button is clicked, fetch and display the data
if submit_button and action_name:
    # Fetch the data
    data = fetch_data_from_api(action_name)

    if data:
        # Show the first record as "Most Frequent Next Action"
        st.subheader("Most Frequent Next Action")
        st.write(f"Action Name: {data[0]['action_name']}")
        st.write(f"Next Action Name: {data[0]['next_action_name']}")
        st.write(f"Frequency: {data[0]['frequency']}")

        # Show remaining records in collapsible format
        for i, record in enumerate(data[1:], start=1):
            with st.expander(f"Next Action {i + 1}"):
                st.write(f"Action Name: {record['action_name']}")
                st.write(f"Next Action Name: {record['next_action_name']}")
                st.write(f"Frequency: {record['frequency']}")
