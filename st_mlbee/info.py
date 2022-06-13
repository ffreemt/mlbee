"""Present info about mlbee."""
from textwrap import dedent

import streamlit as st

from mlbee import __version__

from mlbee.utils import msg


def info():
    """Prep info page."""

    st.subheader(f"mlbee {__version__}")

    st.markdown(msg, unsafe_allow_html=True)
