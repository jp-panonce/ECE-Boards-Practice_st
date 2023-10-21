import streamlit as st
import base64

st.set_page_config(page_title="MUST KNOWS/TIPS",page_icon="📃",layout="wide")

tab_boards, tab_Tips = st.tabs(["Board Exam Mechanics", "Passing Tips"])

with tab_boards:
    pass

with st.sidebar:
    st.sidebar.markdown(
        """<a href="https://www.buymeacoffee.com/jpanonce">
        <img src="data:image/png;base64,{}" width="125">
        </a>""".format(
            base64.b64encode(open("images/buymecoffee_default-yellow.png", "rb").read()).decode()
        ),
        unsafe_allow_html=True,
    )
