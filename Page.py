import streamlit as st
import requests

# URL for your FastAPI endpoint
API_URL = "https://pythonproject0-yiqs.onrender.com/predict_next_action"

# Streamlit UI setup
st.set_page_config(page_title="Action Sequence Predictor", page_icon="🤖", layout="wide")

st.title("Action Sequence Predictor")
st.markdown(
    """
    Welcome to the Action Sequence Predictor API.
    You can predict the next possible actions based on historical data.
    """
)

# Action sequence prediction form
st.header("Predict Next Action")
with st.form(key="predict_form"):
    current_action = st.text_input("Current Action", "reply")
    predict_button = st.form_submit_button("Predict Next Action")

    if predict_button:
        if current_action:
            try:
                # Sending POST request to the FastAPI endpoint
                response = requests.post(
                    API_URL,
                    json={"current_action": current_action}
                )
                result = response.json()

                # Handling the response
                if "detail" in result:
                    st.error(result["detail"])
                else:
                    st.success("Prediction Results:")
                    st.write(f"**Current Action**: {result['current_action']}")
                    st.write(f"**Total Occurrences**: {result['total_occurrences']}")

                    # Display only the first sequence in the list
                    for i in range(3):
                        first_sequence = result['sequences'][i]
                        st.write(f"**Next Action**: {first_sequence['next_action']}")
                        st.write(f"**Frequency**: {first_sequence['frequency']}")
                        st.write(f"**Probability**: {first_sequence['probability']}%")
                        if(i==0):
                            st.write("Other most frequent actions")

            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.error("Current Action is required!")
