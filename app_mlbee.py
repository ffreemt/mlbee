"""Prep for streamlit run app_mlbee.py.

Based on app.py in lit-bee

https://docs.streamlit.io/knowledge-base/using-streamlit/hide-row-indices-displaying-dataframe
    Hide row indices when displaying a dataframe
# CSS to inject contained in a string
hide_table_row_index = '''
            <style>
            tbody th {display:none}
            .blank {display:none}
            </style>
            '''
# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)

# Display a static table
st.table(df)

# Hide row indices with st.dataframe
# CSS to inject contained in a string
hide_dataframe_row_index = '''
            <style>
            .row_heading.level0 {display:none}
            .blank {display:none}
            </style>
           '''
# Inject CSS with Markdown
st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)

# Display an interactive table
st.dataframe(df)

https://medium.com/@avra42/streamlit-python-cool-tricks-to-make-your-web-application-look-better-8abfc3763a5b
hide_menu_style = '''
        <style>
        #MainMenu {visibility: hidden; }
        footer {visibility: hidden;}
        </style>
        '''
st.markdown(hide_menu_style, unsafe_allow_html=True)
"""
# pylint: disable=invalid-name
import os
import sys
import time
from pathlib import Path
from types import SimpleNamespace
from typing import Optional

import loguru
import logzero
import pandas as pd

import streamlit as st
from loguru import logger as loggu
from logzero import logger
from set_loglevel import set_loglevel
from streamlit import session_state as state

from st_mlbee import __version__
from st_mlbee.utils import menu_items
from st_mlbee.multipage import Multipage

from st_mlbee.home import home
from st_mlbee.settings import settings
from st_mlbee.info import info
from st_mlbee.utils import style_css

# curr_py = sys.version[:3]
# msg = f"Some packages st-mlbee depends on can only run with Python 3.8, current python is **{curr_py}**, sorry..."
# assert curr_py == "3.8", msg

os.environ["TZ"] = "Asia/Shanghai"
try:
    time.tzset()  # type: ignore
except Exception as _:
    logger.warning("time.tzset() error: %s. Probably running Windows, we let it pass.", _)

# uncomment this in dev oe set/export LOGLEVEL=10
# os.environ["LOGLEVEL"] = "10"

logzero.loglevel(set_loglevel())

loggu.remove()
_ = (
    "<green>{time:YY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <5}</level> | <level>{message}</level> "
    "<cyan>{module}.{name}</cyan>:<cyan>{line}</cyan>"
)
loggu.add(
    sys.stderr,
    format=_,
    level=set_loglevel(),
    colorize=True,
)

# from PIL import Image
# page_icon=Image.open("icon.ico"),
st.set_page_config(  # type: ignore
    page_title=f"st-mlbee v{__version__}",
    # page_icon="🧊",
    page_icon="🐝",
    # layout="wide",
    initial_sidebar_state="auto",  # "auto" or "expanded" or "collapsed",
    menu_items=menu_items,
)

# pd.set_option("precision", 2)
pd.set_option("display.precision", 2)
pd.options.display.float_format = "{:,.2f}".format

beetype = "mlbee"
sourcetype = "upload"
if set_loglevel() <= 10:
    sourcetype = "urls"

_ = dict(
    beetype=beetype,
    sourcetype=sourcetype,
    sourcecount=2,
    sentali=None,
    src_filename="",
    tgt_filename="",
    src_fileio=b"",
    tgt_fileio=b"",
    src_file="",
    tgt_file="",
    list1=[""],
    list2=[""],
    df=None,
    df_a=None,
    df_s_a=None,
    count=1,
    updated=False,
)
if "ns" not in state:
    state.ns = SimpleNamespace(**_)
state.ns.list = [*_]


def main():
    """Bootstrap."""
    # options()

    st.markdown(f"<style>{style_css}</style>", unsafe_allow_html=True)

    app = Multipage()

    app.add_page("Home", "house", home)
    # app.add_page("Settings", "gear", settings)
    # app.add_page("Setup", "gear", settings)
    app.add_page("Config", "gear", settings)
    app.add_page("Info", "info", info)

    app.run()

    if set_loglevel() <= 10:
        st.markdown(state.ns.count)
    logger.debug(" run: %s", state.ns.count)
    state.ns.count += 1
    state.ns.updated = False


main()
