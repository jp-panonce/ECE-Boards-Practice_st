import streamlit as st
import base64

st.set_page_config(page_title="About the site",page_icon="📃",layout="wide")

#TODO: include what site is about
    # - open resources for everyone who can't affor review centers
    # - site is open source. everyone can submit questions through github

with st.sidebar:
    st.sidebar.markdown(
        """<a href="https://www.buymeacoffee.com/jpanonce">
        <img src="data:image/png;base64,{}" width="125">
        </a>""".format(
            base64.b64encode(open("images/buymecoffee_default-yellow.png", "rb").read()).decode()
        ),
        unsafe_allow_html=True,
    )
