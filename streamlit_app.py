import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="AI Summarizer", layout="centered")
st.title("AI Text Summarizer")
st.markdown("Summarize long text or .txt files using Hugging Face model.")

tab1, tab2, tab3 = st.tabs(["📄 Text", "📂 File Upload", "📜 History"])

# --- Tab 1: Text Summarization ---
with tab1:
    user_input = st.text_area("Enter your text", height=200)
    if st.button("Summarize Text"):
        if len(user_input.strip()) < 50:
            st.error("Please enter at least 50 characters.")
        else:
            with st.spinner("Summarizing..."):
                try:
                    res = requests.post(f"{API_URL}/summarize", json={"text": user_input})
                    res.raise_for_status()
                    summary = res.json()["summary"]
                    st.success("Summary:")
                    st.write(summary)
                except Exception as e:
                    st.error(f"Error: {e}")

# --- Tab 2: File Upload ---
with tab2:
    uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])
    if uploaded_file and st.button("Summarize File"):
        with st.spinner("Uploading and summarizing..."):
            files = {"file": (uploaded_file.name, uploaded_file, "text/plain")}
            try:
                res = requests.post(f"{API_URL}/summarize-file", files=files)
                res.raise_for_status()
                summary = res.json()["summary"]
                st.success("Summary:")
                st.write(summary)
            except Exception as e:
                try:
                    error_msg = res.json().get("detail", str(e))
                except:
                    error_msg = str(e)
                st.error(f"Error: {error_msg}")
    elif not uploaded_file:
        st.warning("Please upload a file before clicking the button.")

# --- Tab 3: History ---
with tab3:
    if st.button("Fetch Summary History"):
        try:
            res = requests.get(f"{API_URL}/history")
            res.raise_for_status()
            data = res.json()
            for entry in reversed(data):
                st.write(f"📆 {entry['created_at']}")
                st.markdown(f"*Original:* {entry['text'][:100]}...")
                st.markdown(f"*Summary:* {entry['summary']}")
                st.markdown("---")
        except Exception as e:
            st.error(f"Error: {e}")
