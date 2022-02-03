import streamlit as st

def run():

    with st.form("Text Input Form"):
        reference_text = st.text_area("Reference Text", value = st.session_state.reference_text)
        inference_text = st.text_area("Inference Text", value = st.session_state.inference_text)
        submit = st.form_submit_button("Submit")

        if submit:
            st.session_state.reference_text = reference_text
            st.session_state.inference_text = inference_text
            st.session_state.page = "dashboard"
            st.experimental_rerun()