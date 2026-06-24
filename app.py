import streamlit as st
from agent import run_agent

st.set_page_config(page_title="AI PR Code Review Agent", page_icon="assets/logo.png", layout="centered")

st.image("assets/logo.png", width=80)
st.markdown("<h1 style='color:#58a6ff;'>AI PR Code Review Agent</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#8b949e;'>Paste a GitHub Pull Request URL and get an instant AI-powered code review.</p>", unsafe_allow_html=True)
st.markdown("---")

pr_url = st.text_input("GitHub PR URL", placeholder="https://github.com/user/repo/pull/1")

if st.button("Run Review"):
    if pr_url:
        with st.spinner("Analyzing PR..."):
            try:
                review = run_agent(pr_url)
                st.success("Review complete.")
                st.markdown("### Review Results")
                st.write(review)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a GitHub PR URL.")

st.markdown("---")
st.markdown("<p style='text-align:center;color:#484f58;font-size:0.8rem;'>Built by Pradeep | Powered by Groq + Llama 3.3</p>", unsafe_allow_html=True)