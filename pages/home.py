import streamlit as st

def run():

    with st.form("Text Input Form"):
        reference_text = st.text_area("Reference Text", value = st.session_state.reference_text)
        inference_text = st.text_area("Inference Text", value = st.session_state.inference_text)
        distance_threshold = st.slider("Distance Threshold", 0.0, 1.0, st.session_state.distance_threshold)
        submit = st.form_submit_button("Submit")

        if submit:
            st.session_state.reference_text = reference_text
            st.session_state.inference_text = inference_text
            st.session_state.distance_threshold = distance_threshold
            st.session_state.colors = None
            st.session_state.page = "dashboard"
            st.experimental_rerun()