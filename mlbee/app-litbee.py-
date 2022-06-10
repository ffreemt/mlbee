"""Prep __main__.py.

https://share.streamlit.io/deploy
    Advanced settings...
        Python version
            3.7
            3.8
            3.9*
            3.10

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
import ezbee
import dzbee
import debee

import streamlit as st
from loguru import logger as loggu
from logzero import logger
from set_loglevel import set_loglevel
from streamlit import session_state as state

from litbee import __version__
# from litbee.options import options

# from litbee.files2df import files2df
# from litbee.utils import sb_front_cover, instructions, menu_items
# from litbee.ezbee_page import ezbee_page
# from litbee.dzbee_page import dzbee_page
# from litbee.xbee_page import xbee_page
from litbee.utils import menu_items

from litbee.multipage import Multipage

# from litbee.fetch_upload import fetch_upload
# from litbee.fetch_paste import fetch_paste
# from litbee.fetch_urls import fetch_urls

from litbee.home import home
from litbee.settings import settings
from litbee.info import info
from litbee.utils import style_css

# from ezbee import ezbee

curr_py = sys.version[:3]
msg = f"Some packages litbee depends on can only run with Python 3.8, current python is **{curr_py}**, sorry..."
assert curr_py == "3.8", msg

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
    page_title=f"litbee v{__version__}",
    # page_icon="🧊",
    page_icon="🐝",
    # layout="wide",
    initial_sidebar_state="auto",  # "auto" or "expanded" or "collapsed",
    menu_items=menu_items,
)

# pd.set_option("precision", 2)
pd.set_option("display.precision", 2)
pd.options.display.float_format = "{:,.2f}".format

sourcetype = "upload"
if set_loglevel() <= 10:
    sourcetype = "urls"

_ = dict(
    beetype="ezbee",
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

logger.info(
    "versions ezbee dzbee debee: %s, %s, %s",
    ezbee.__version__,
    dzbee.__version__,
    debee.__version__,
)


def main():
    """Bootstrap."""
    # options()

    st.markdown(f"<style>{style_css}</style>", unsafe_allow_html=True)

    app = Multipage()

    # app.add_page("Home", "house", ask.app)
    # app.add_page("Settings", "gear", settings.app)
    # app.add_page("Info", "info", info.app)

    # app.add_page("Home", "house", fetch_upload)
    app.add_page("Home", "house", home)
    app.add_page("Settings", "gear", settings)
    app.add_page("Info", "info", info)

    # The main app
    app.run()

    # st.markdown(f"""<div class="text"> run: {state.ns.count}</div>""", unsafe_allow_html=True)

    if set_loglevel() <= 10:
        st.markdown(state.ns.count)
    loggu.debug(f" run: {state.ns.count}")
    logger.debug(f" run: {state.ns.count}")
    state.ns.count += 1
    state.ns.updated = False


main()
