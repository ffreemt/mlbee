"""Present info about st-mlbee."""
from textwrap import dedent

import streamlit as st

from st_mlbee import __version__

from st_mlbee.utils import msg


def info():
    """Prep info page."""

    st.subheader(f"st-mlbee {__version__}")

    st.markdown(msg, unsafe_allow_html=True)
