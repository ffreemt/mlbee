"""Fetch pasted text and convert to state.ns.list1/list2."""
# pylint: disable=invalid-name
import streamlit as st
from logzero import logger
from streamlit import session_state as state


def fetch_paste():
    """Fetch from clipboard."""
    # st.write("Coming soon")
    text1 = ""
    text2 = ""
    with st.form(key="paste_in_form"):
        _ = st.expander(f"{state.ns.beetype}: Paste text", expanded=True)
        with _:
            col1, col2 = st.columns(2)
            with col1:
                text1 = st.text_area(
                    label="Paste your stuff here",
                    key="paste_text1",
                    # help=""
                    height=500,
                )

            with col2:
                text2 = st.text_area(
                    label="Paste your stuff here",
                    # help=""
                    key="paste_text2",
                    height=500,
                )

        submitted = st.form_submit_button("Submit")

    logger.debug("text1[:10]: %s, text2[:10]: %s", text1[:10], text2[:10])

    list1 = [_.strip() for _ in text1.splitlines() if _.strip()]
    list2 = [_.strip() for _ in text2.splitlines() if _.strip()]

    state.ns.list1 = list1[:]
    state.ns.list2 = list2[:]

    logger.debug("len(list1): %s, len(list2): %s", len(list1), len(list2))

    logger.debug("state.ns.updated: %s", state.ns.updated)

    state.ns.src_filename = ""
    state.ns.updated = True
