import streamlit as st
import requests
import os

API_URL = "http://127.0.0.1:8000/research"  # FastAPI backend

st.set_page_config(page_title="Smart Research Assistant", page_icon="🔍", layout="centered")

st.title(" Smart Research Assistant")
st.write("Enter your topic and generate a structured research summary with AI.")

query = st.text_input("Enter your research topic:")

if st.button("Generate Report"):
    if not query.strip():
        st.warning(" Please enter a valid topic.")
    else:
        with st.spinner("🔍 Processing your request... Please wait..."):
            try:
                response = requests.post(API_URL, json={"topic_query": query})
                
                if response.status_code == 200:
                    state = response.json()
                    st.success(" Research Completed!")

                    # --- Summary Section ---
                    st.subheader("Summary:")
                    st.write(state.get("final_summary", "No summary generated."))

                    # --- Analysis Section ---
                    st.subheader(" Analysis:")
                    st.json(state.get("analysis_result", {}))

                    # --- Source Documents ---
                    st.subheader(" Source Documents:")
                    for d in state.get("raw_documents", []):
                        st.markdown(f"- [{d['title']}]({d['url']}) ({d['source_domain']})")

                    # --- PDF Download Section ---
                    if "pdf_path" in state and os.path.exists(state["pdf_path"]):
                        with open(state["pdf_path"], "rb") as pdf_file:
                            st.download_button(
                                label="📥 Download Research Report (PDF)",
                                data=pdf_file,
                                file_name=os.path.basename(state["pdf_path"]),
                                mime="application/pdf"
                            )
                    else:
                        st.info(" PDF not generated yet.")
                
                else:
                    st.error(f" Failed to generate report. (Status: {response.status_code})")

            except requests.exceptions.ConnectionError:
                st.error(" Unable to connect to backend! Please start the FastAPI server first.")
